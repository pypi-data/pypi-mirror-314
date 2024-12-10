=======================
NEWS for lazr.lifecycle
=======================

1.2.2 (2024-12-09)
==================

- Add support for Python 3.9, 3.10, 3.11, 3.12 and 3.13.
- Remove support for Python 3.7 and below.
- Add basic pre-commit configuration.
- Publish documentation on Read the Docs.
- Switch to declarative ``setuptools`` configuration.

1.2.1 (2021-09-13)
==================

- Adjust versioning strategy to avoid importing pkg_resources, which is slow
  in large environments.

1.2 (2019-11-04)
================

- Import IObjectEvent from zope.interface rather than zope.component.
- Add ObjectModifiedEvent.descriptions property, for compatibility with
  zope.lifecycleevent >= 4.2.0.
- Switch from buildout to tox.
- Add Python 3 support.

1.1 (2009-12-03)
================

- Add IDoNotSnapshot and doNotSnapshot to allow the exclusion of
  certain fields.

1.0 (2009-08-31)
================

- Remove build dependencies on bzr and egg_info

- remove sys.path hack in setup.py for __version__

0.1 (2009-03-24)
================

- Initial release
