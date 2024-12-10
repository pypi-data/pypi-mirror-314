# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# Invenio-Jobs is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Jobs module."""

from abc import ABC, abstractmethod


class JobType(ABC):
    """Base class to register celery tasks available in the admin panel."""

    arguments_schema = None
    task = None
    id = None
    title = None
    description = None

    @classmethod
    def create(
        cls, job_cls_name, arguments_schema, id_, task, description, title, attrs=None
    ):
        """Create a new instance of a job."""
        if not attrs:
            attrs = {}
        return type(
            job_cls_name,
            (JobType,),
            dict(
                id=id_,
                arguments_schema=arguments_schema,
                task=task,
                description=description,
                title=title,
                **attrs
            ),
        )

    @abstractmethod
    def default_args(self, *args, **kwargs):
        """Abstract method to enforce implementing default arguments."""
        return {}

    @classmethod
    def build_task_arguments(cls, job_obj, custom_args=None, **kwargs):
        """Build arguments to be passed to the task.

        Custom arguments can be passed to overwrite the default arguments of a job.
        """
        if custom_args:
            return custom_args
        return cls.default_args(job_obj, **kwargs)
