# -*- coding: utf-8 -*-
"""
See `prereleaser_middle`.

"""

import os
import sys

def prereleaser_middle(data):
    """
    Sets the ``SETUPTOOLS_SCM_PRETEND_VERSION`` environment variable
    to the value of ``new_version`` in the *data* dictionary.

    When run as part of a fullrelease, this will ensure that
    ``setuptools_scm`` does what the user wants. Otherwise, in the
    ``release`` step that follows this, ``zest.releaser`` will ask
    ``setuptools`` for the version to use, expecting to get back what
    it has stored in the ``setup.py`` file as part of the
    ``prerelease`` step. But ``setuptools_scm`` will ignore that.
    """
    report = data.get('icrs.releaser:report', print)
    report("Setting SETUPTOOLS_SCM_PRETEND_VERSION to", repr(data['new_version']),
           file=sys.stderr)
    os.environ['SETUPTOOLS_SCM_PRETEND_VERSION'] = data['new_version']
