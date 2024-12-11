===============
 icrs.releaser
===============

.. image:: https://github.com/jamadden/icrs.releaser/workflows/tests/badge.svg
   :target: https://github.com/jamadden/icrs.releaser/actions?query=workflow%3Atests

.. image:: https://coveralls.io/repos/github/jamadden/icrs.releaser/badge.svg?branch=master
   :target: https://coveralls.io/github/jamadden/icrs.releaser?branch=master

.. image:: https://readthedocs.org/projects/icrsreleaser/badge/?version=latest
   :target: https://icrsreleaser.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status


This package provides support for releasing projects using
`zest.releaser <https://zestreleaser.readthedocs.io>`_, especially in
combination with `setuptools_scm
<https://pypi.org/project/setuptools-scm/>`_.

This package does three things:

* Insert the correct version number in source files.

  It's helpful for readers of the source code and the documentation
  when object docstrings contain abbreviated change logs. Sphinx
  supports this with `the special directives
  <https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-versionadded>`_
  ``versionadded``, ``versionchanged``, and ``deprecated``. For
  example, a docstring might contain::

    .. versionchanged:: 2.0.1
       Now frob the frizzle correctly when *frob_frizzle* is true.

  But the author of the docstring doesn't always know what the version
  number that contains the change will ultimately be. In a scheme like
  `CalVer <https://calver.org>`_, that will depend on when the release is made, and in a
  scheme like `SemVer <https://semver.org>`_, that will depend on what other changes are
  part of the release. In either case, it can't be determined until
  the release is actually made.

  To solve this, this package has a plugin that lets you write your
  docstrings like so::

    .. deprecated:: NEXT
       Turns out frobbing the frizzle was a bad idea.

  When a release is made, all ``.py`` files that are found in the ``src/<PROJECT>/``
  directory are examined for those three directives with an argument
  of ``NEXT``, and the ``NEXT`` value is replaced with the version
  number the user selected.

  The user will be presented a diff of the changes made and asked
  whether to commit them before continuing.
* Removes C compiler flags from the environment.

  You may have custom C compiler flags in your environment
  (``CFLAGS``, etc). These may contain non-portable options such as
  ``-ffast-math`` or ``-march=native`` that would prevent binary
  wheels built on your machine from working on other machines.

  This package removes those flags from the environment that builds
  binary wheels.
* Makes ``setuptools_scm`` respect the version number the user entered.

  ``zest.releaser`` asks ``setuptools`` what version to use when it
  tags the repository. It expects to get back the version that the
  user entered, and which it wrote to disk (typically in
  ``setup.py``).

  But because ``setuptools_scm`` overrides the value stored in
  ``setup.py`` based on the last tag in the repository, this doesn't
  work: it would only work if the tag was already made! Instead of
  getting the correct tag like ``0.0.2``, ``zest.releaser`` wants to
  create a tag like ``0.0.1.dev11+gbeb8b20``.

  This package forces ``setuptools_scm`` to respect the version that
  the user entered so that the tag is correct.

Installation And Usage
======================

This package registers certain entry points with ``zest.releaser``
when it is installed, so it is only necessary to ``pip install
icrs.releaser`` and then invoke ``icrs_release`` to use the plugins
mentioned above.

This package provides the ``recommended`` extra to install the same
things that ``zest.releaser[recommended]`` does.

.. code-block:: console

   $ pip install 'icrs.releaser[recommended]'

.. important::

   This package assumes that your project uses the standard ``src/``
   layout. That is, for a package named ``foo``, there will be a
   directory next to ``setup.py``, ``src/foo/``, containing the Python
   source. Likewise, for a namespace package ``foo.bar``, the code
   will be in ``src/foo/bar/``.

.. important::

   Because this package is a plugin to ``zest.releaser``, the two
   packages must be installed in the same environment (same Python
   path). The easiest way to ensure this is to just install this
   package, and then use the command from the next point.

.. important::

   For this package to work, you must use the ``icrs_release``
   command.

   This is a simple wrapper for the ``fullrelease`` command provided
   by ``zest.releaser``. It's use is necessitated by the fact that
   this package works in part by setting and unsetting environment
   variables.
