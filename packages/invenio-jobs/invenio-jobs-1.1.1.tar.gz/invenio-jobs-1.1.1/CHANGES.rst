..
    Copyright (C) 2024 CERN.

    Invenio-Jobs is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.

Changes
=======

Version v1.1.1 (released 2024-12-09)

- tasks: use utcnow to avoid timezone issues with the Celery scheduler

Version v1.1.0 (released 2024-10-10)

- webpack: bump react-searchkit

Version v1.0.0 (released 2024-09-27)

- db: change tables names
- global: add jobs registry
- interface: add job types

Version v0.5.1 (released 2024-09-19)

- fix: add compatibility layer to move to flask>=3

Version v0.5.0 (released 2024-08-22)

- bump invenio-users-resources

Version v0.4.0 (released 2024-08-22)

- package: bump react-invenio-forms (#52)

Version v0.3.4 (released 2024-08-08)

- fix: pass args to task via run

Version v0.3.3 (released 2024-08-08)

- fix: utils: only eval strings

Version 0.3.2 (released 2024-07-24)

- UI: fix schedule save
- UI: fix default queue; don't error on empty args

Version 0.3.1 (released 2024-07-11)

- services: skip index rebuilding

Version 0.3.0 (released 2024-06-20)

- UI: Added create, edit and schedule options
- fix: only show stop button when task is running
- bug: fix display of durations
- global: support Jinja templating for job args
- config: rename enabled flag
- config: disable jobs view by default

Version 0.2.0 (released 2024-06-05)

- translations: added translations folder
- scheduler: filter jobs with a schedule
- service: pass run queue to task

Version 0.1.0 (released 2024-06-04)

- Initial public release.
