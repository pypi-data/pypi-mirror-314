# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
# Copyright (C) 2024 Graz University of Technology.
#
# Invenio-Jobs is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""InvenioRDM module for jobs management."""

from .ext import InvenioJobs

__version__ = "1.1.1"

__all__ = ("__version__", "InvenioJobs")
