# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
# Copyright (C) 2024 Graz University of Technology.
#
# Invenio-Jobs is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Service results."""
import json
from collections.abc import Iterable, Sized

from invenio_records_resources.services.records.results import (
    ExpandableField,
    RecordItem,
    RecordList,
)

try:
    # flask_sqlalchemy<3.0.0
    from flask_sqlalchemy import Pagination
except ImportError:
    # flask_sqlalchemy>=3.0.0
    from flask_sqlalchemy.pagination import Pagination


class AttrDict(dict):
    """Helper class to fake API layer."""

    def __init__(self, *args, **kwargs):
        """Constructor."""
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


class Item(RecordItem):
    """Single item result."""

    @property
    def id(self):
        """Get the result id."""
        return str(self._record.id)


class JobItem(Item):
    """Single Job result."""

    @property
    def data(self):
        """Data representation of job result item."""
        if self._data:
            return self._data

        job_dict = self._obj.dump()
        if self._obj.last_run:
            job_dict["last_run"] = self._obj.last_run.dump()
            job_dict["last_runs"] = self._obj.last_runs
        job_dict["default_args"] = json.dumps(
            self._obj.default_args, indent=4, sort_keys=True, default=str
        )
        job_record = AttrDict(job_dict)

        self._data = self._schema.dump(
            job_record,
            context={
                "identity": self._identity,
                "record": self._record,
            },
        )

        if self._links_tpl:
            self._data["links"] = self.links
        return self._data


class List(RecordList):
    """List result."""

    @property
    def items(self):
        """Iterator over the items."""
        if isinstance(self._results, Pagination):
            return self._results.items
        elif isinstance(self._results, Iterable):
            return self._results
        return self._results

    @property
    def total(self):
        """Get total number of hits."""
        if hasattr(self._results, "hits"):
            return self._results.hits.total["value"]
        if isinstance(self._results, Pagination):
            return self._results.total
        elif isinstance(self._results, Sized):
            return len(self._results)
        else:
            return None

    # TODO: See if we need to override this
    @property
    def aggregations(self):
        """Get the search result aggregations."""
        try:
            return self._results.labelled_facets.to_dict()
        except AttributeError:
            return None

    @property
    def hits(self):
        """Iterator over the hits."""
        for hit in self.items:
            # Project the hit
            hit_dict = hit.dump()
            hit_record = AttrDict(hit_dict)
            projection = self._schema.dump(
                hit_record,
                context=dict(identity=self._identity, record=hit),
            )
            if self._links_item_tpl:
                projection["links"] = self._links_item_tpl.expand(self._identity, hit)
            if self._nested_links_item:
                for link in self._nested_links_item:
                    link.expand(self._identity, hit, projection)

            yield projection


class JobList(List):
    """List result."""

    @property
    def hits(self):
        """Iterator over the hits."""
        for hit in self.items:
            # Project the hit
            job_dict = hit.dump()
            job_dict["last_run"] = hit.last_run
            job_dict["last_runs"] = hit.last_runs
            job_dict["default_args"] = json.dumps(
                hit.default_args, indent=4, sort_keys=True, default=str
            )
            job_record = AttrDict(job_dict)
            projection = self._schema.dump(
                job_record,
                context=dict(identity=self._identity, record=hit),
            )
            if self._links_item_tpl:
                projection["links"] = self._links_item_tpl.expand(self._identity, hit)
            if self._nested_links_item:
                for link in self._nested_links_item:
                    link.expand(self._identity, hit, projection)

            yield projection


class ModelExpandableField(ExpandableField):
    """Expandable entity resolver field.

    It will use the Entity resolver registry to retrieve the service to
    use to fetch records and the fields to return when serializing
    the referenced record.
    """

    entity_proxy = None

    def ghost_record(self, value):
        """Return ghost representation of not resolved value."""
        return self.entity_proxy.ghost_record(value)

    def system_record(self):
        """Return the representation of a system user."""
        return self.entity_proxy.system_record()

    def get_value_service(self, value):
        """Return the value and the service via entity resolvers."""
        self.entity_proxy = ResolverRegistry.resolve_entity_proxy(value)
        v = self.entity_proxy._parse_ref_dict_id()
        _resolver = self.entity_proxy.get_resolver()
        service = _resolver.get_service()
        return v, service

    def pick(self, identity, resolved_rec):
        """Pick fields defined in the entity resolver."""
        return self.entity_proxy.pick_resolved_fields(identity, resolved_rec)
