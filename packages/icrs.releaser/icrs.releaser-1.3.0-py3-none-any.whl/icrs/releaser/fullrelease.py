# -*- coding: utf-8 -*-
"""
Provides the ``icrs_fullrelease`` command as a console script.

This is a simple wrapper around `zest.releaser.fullrelease.main`
intended to make it easier to use this package, since certain of its plugins
only work when the release is run from a single process.
"""

import sys

from zest.releaser.fullrelease import main

if __name__ == '__main__':
    sys.exit(main())
