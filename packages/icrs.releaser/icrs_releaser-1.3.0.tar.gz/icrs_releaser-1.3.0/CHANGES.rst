=========
 Changes
=========

1.3.0 (2024-12-10)
==================

- Use native ``pkgutil`` style namespace package.
- Add support for Python 3.13.


1.2.0 (2024-01-30)
==================

- Add support for Python 3.11 and 3.12.
- Drop support for Python 3.8. The minimum supported version is now 3.9.
- Depend on newer ``zest.releaser >= 9.1.1``.
- Remove dependency on setuptools; now uses the so-called
  "native" namespace packages.
- Add a new release check that forbids having development dependencies
  (e.g., "icrs.releaser >= 3.0.dev0" would be forbidden). This only
  works for ``setuptools`` projects that have dependencies listed in setup.py.


1.1.0 (2022-03-03)
==================

- Fix handling the case where the project name is a namespace
  (``icrs.releaser``), but the source directory on disk doesn't
  include the namespace (``src/releaser``). This is a legacy case,
  supported for projects that are transitioning to a standard layout.


1.0.1 (2022-02-25)
==================

- Add the 'recommended' extra for installing the same things that
  ``zest.releaser[recommended]`` does.


1.0.0 (2022-02-25)
==================

- Initial PyPI release.
