# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
# Copyright (C) 2024 University of Münster.
#
# Invenio-Jobs is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Service definitions."""

import uuid

import sqlalchemy as sa
from invenio_records_resources.services.base import LinksTemplate
from invenio_records_resources.services.base.utils import map_search_params
from invenio_records_resources.services.records import RecordService
from invenio_records_resources.services.uow import (
    ModelCommitOp,
    ModelDeleteOp,
    TaskOp,
    TaskRevokeOp,
    unit_of_work,
)

from invenio_jobs.tasks import execute_run

from ..api import AttrDict
from ..models import Job, Run, RunStatusEnum, Task
from ..proxies import current_jobs
from .errors import JobNotFoundError, RunNotFoundError, RunStatusChangeError


class BaseService(RecordService):
    """Base service class for DB-backed services.

    NOTE: See https://github.com/inveniosoftware/invenio-records-resources/issues/583
    for future directions.
    """

    def rebuild_index(self, identity, uow=None):
        """Raise error since services are not backed by search indices."""
        raise NotImplementedError()


class TasksService(BaseService):
    """Tasks service."""

    def read_registered_task_arguments(self, identity, registered_task_id):
        """Return arguments allowed for given task."""
        self.require_permission(identity, "read")

        task = Task.get(registered_task_id)
        if task.arguments_schema:
            return task.arguments_schema()


def get_job(job_id):
    """Get a job by id."""
    job = Job.query.get(job_id)
    if job is None:
        raise JobNotFoundError(job_id)
    return job


def get_run(run_id, job_id=None):
    """Get a job by id."""
    run = Run.query.get(run_id)
    if run is None or run.job_id != job_id:
        raise RunNotFoundError(run_id, job_id=job_id)
    return run


class JobsService(BaseService):
    """Jobs service."""

    @unit_of_work()
    def create(self, identity, data, uow=None):
        """Create a job."""
        self.require_permission(identity, "create")

        # TODO: See if we need extra validation (e.g. tasks, args, etc.)
        valid_data, errors = self.schema.load(
            data,
            context={"identity": identity},
            raise_errors=True,
        )

        job = Job(**valid_data)
        uow.register(ModelCommitOp(job))
        return self.result_item(self, identity, job, links_tpl=self.links_item_tpl)

    def search(self, identity, params):
        """Search for jobs."""
        self.require_permission(identity, "search")

        search_params = map_search_params(self.config.search, params)
        query_param = search_params["q"]
        filters = []
        if query_param:
            filters.extend(
                [
                    Job.title.ilike(f"%{query_param}%"),
                    Job.description.ilike(f"%{query_param}%"),
                ]
            )

        jobs = (
            Job.query.filter(sa.or_(*filters))
            .order_by(
                search_params["sort_direction"](
                    sa.text(",".join(search_params["sort"]))
                )
            )
            .paginate(
                page=search_params["page"],
                per_page=search_params["size"],
                error_out=False,
            )
        )

        return self.result_list(
            self,
            identity,
            jobs,
            params=search_params,
            links_tpl=LinksTemplate(self.config.links_search, context={"args": params}),
            links_item_tpl=self.links_item_tpl,
        )

    def read(self, identity, id_):
        """Retrieve a job."""
        self.require_permission(identity, "read")
        job = get_job(id_)
        return self.result_item(self, identity, job, links_tpl=self.links_item_tpl)

    @unit_of_work()
    def update(self, identity, id_, data, uow=None):
        """Update a job."""
        self.require_permission(identity, "update")

        job = get_job(id_)

        valid_data, errors = self.schema.load(
            data,
            context={"identity": identity, "job": job},
            raise_errors=True,
        )

        for key, value in valid_data.items():
            setattr(job, key, value)
        uow.register(ModelCommitOp(job))
        return self.result_item(self, identity, job, links_tpl=self.links_item_tpl)

    @unit_of_work()
    def delete(self, identity, id_, uow=None):
        """Delete a job."""
        self.require_permission(identity, "delete")
        job = get_job(id_)

        # TODO: Check if we can delete the job (e.g. if there are still active Runs).
        # That also depends on the FK constraints in the DB.
        uow.register(ModelDeleteOp(job))

        return True


class RunsService(BaseService):
    """Runs service."""

    def search(self, identity, job_id, params):
        """Search for runs."""
        self.require_permission(identity, "search")

        search_params = map_search_params(self.config.search, params)
        query_param = search_params["q"]
        base_query = Run.query.filter(Run.job_id == job_id)
        filters = []
        if query_param:
            filters.extend(
                [
                    Run.title.ilike(f"%{query_param}%"),
                    Run.message.ilike(f"%{query_param}%"),
                ]
            )

        runs = (
            base_query.filter(sa.or_(*filters))
            .order_by(
                search_params["sort_direction"](
                    sa.text(",".join(search_params["sort"]))
                )
            )
            .paginate(
                page=search_params["page"],
                per_page=search_params["size"],
                error_out=False,
            )
        )

        return self.result_list(
            self,
            identity,
            runs,
            params=search_params,
            links_tpl=LinksTemplate(self.config.links_search, context={"args": params}),
            links_item_tpl=self.links_item_tpl,
        )

    def read(self, identity, job_id, run_id):
        """Retrieve a run."""
        self.require_permission(identity, "read")
        run = get_run(job_id=job_id, run_id=run_id)
        run_dict = run.dump()
        run_record = AttrDict(run_dict)
        return self.result_item(
            self, identity, run_record, links_tpl=self.links_item_tpl
        )

    @unit_of_work()
    def create(self, identity, job_id, data, uow=None):
        """Create a run."""
        self.require_permission(identity, "create")

        job = get_job(job_id)
        # TODO: See if we need extra validation (e.g. tasks, args, etc.)
        valid_data, errors = self.schema.load(
            data,
            context={"identity": identity, "job": job},
            raise_errors=True,
        )

        run = Run.create(
            job=job,
            id=str(uuid.uuid4()),
            task_id=str(uuid.uuid4()),
            started_by_id=identity.id,
            status=RunStatusEnum.QUEUED,
            **valid_data,
        )
        uow.register(ModelCommitOp(run))
        uow.register(
            TaskOp.for_async_apply(
                execute_run,
                kwargs={"run_id": run.id},
                task_id=str(run.task_id),
                queue=run.queue,
            )
        )

        return self.result_item(self, identity, run, links_tpl=self.links_item_tpl)

    @unit_of_work()
    def update(self, identity, job_id, run_id, data, uow=None):
        """Update a run."""
        self.require_permission(identity, "update")

        run = get_run(job_id=job_id, run_id=run_id)

        valid_data, errors = self.schema.load(
            data,
            context={"identity": identity, "run": run, "job": run.job},
            raise_errors=True,
        )

        for key, value in valid_data.items():
            setattr(run, key, value)

        uow.register(ModelCommitOp(run))
        return self.result_item(self, identity, run, links_tpl=self.links_item_tpl)

    @unit_of_work()
    def delete(self, identity, job_id, run_id, uow=None):
        """Delete a run."""
        self.require_permission(identity, "delete")
        run = get_run(job_id=job_id, run_id=run_id)

        # TODO: Check if we can delete the run (e.g. if it's still running).
        uow.register(ModelDeleteOp(run))

        return True

    @unit_of_work()
    def stop(self, identity, job_id, run_id, uow=None):
        """Stop a run."""
        self.require_permission(identity, "stop")
        run = get_run(job_id=job_id, run_id=run_id)

        if run.status not in (RunStatusEnum.QUEUED, RunStatusEnum.RUNNING):
            raise RunStatusChangeError(run, RunStatusEnum.CANCELLING)

        run.status = RunStatusEnum.CANCELLING
        uow.register(ModelCommitOp(run))
        uow.register(TaskRevokeOp(str(run.task_id)))

        return self.result_item(self, identity, run, links_tpl=self.links_item_tpl)
