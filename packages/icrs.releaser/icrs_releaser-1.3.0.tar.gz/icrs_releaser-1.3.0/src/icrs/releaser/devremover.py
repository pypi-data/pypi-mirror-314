# -*- coding: utf-8 -*-
"""
See `prereleaser_before`.

"""

import re
import sys

from pathlib import Path

class DevelopmentDependency(Exception):
    """
    Raised when a development dependency is detected.
    """

# An expression that matches dependency specification lines that have
# ".dev" versions.
#
# TODO: The ``packaging`` library
# (https://packaging.pypa.io/en/stable/index.html) has support to
# actually parse all of these complicated specifiers; the problem is
# extracting which lines need to be parsed like that. We're just
# matching the entire file
_SETUP_PY_DEV_REQUIREMENT_MATCHER = re.compile(
    # open single or double quote
    br"['\"]"
    # one or more alphanumeric characters, underscores, periods
    # commas, spaces or square brackets (for extras)
    # and zero or more spaces
    br"[\w.,\[\] ]+\s*"
    # followed by an operator.
    # (recall that 'foo < 3, >2, !=2.1' is valid syntax; the clauses can come in
    # any order). See https://peps.python.org/pep-0508/
    br"[>=<!~]"
    # followed by any number of characters of any sort, but with at least one number.
    br".*\d+.*"
    # followed by the ".dev" sequence
    br"\.dev"
    # followed by any number of characters
    br".*"
    # ended with the closing string quote
    # (if we wanted to be super smart, we would use a capture group to match
    # the actual opening quote)
    br"['\"]"
)

def prereleaser_before(data):
    """
    Checks for development dependencies and raise an error
    if found.

    A non-released dependency is something in setup.py that has a version number
    containing ".dev". An exception is raised if this is found.

    This is a "prereleaser before" hook so that it runs before anything
    tries to commit to the project (e.g., to update the version number).

    .. todo::

       This only supports traditional setuptools-style
       projects and only supports setup.py. Ideally, it would
       support pyproject.toml, setup.cfg and generic build backends.
       We'd need to be able to get the project metadata (``.egg-info`` in setuptools,
       or part of the records recorded in the wheel file) to make that
       work reliably, though, and I'm not sure how to do that.
    """
    report = data.get('icrs.releaser:report', print)
    report('Checking for the existence of development dependencies.')
    root_dir = Path(data['reporoot'])

    for p in (
        root_dir / 'setup.py',
    ):
        if not p.is_file():
            report('Project file', p, "does not exist; not checking for development deps.",
                   file=sys.stderr)
            continue

        contents = p.read_bytes()
        if (match := _SETUP_PY_DEV_REQUIREMENT_MATCHER.search(contents)):
            raise DevelopmentDependency(
                "Project file %s had development dependency: %s" % (
                    p, match.group().decode('utf-8', errors='ignore')
                )
            )
