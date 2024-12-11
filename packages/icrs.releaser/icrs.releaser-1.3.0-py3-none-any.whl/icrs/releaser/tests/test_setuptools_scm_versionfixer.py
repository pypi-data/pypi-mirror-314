# -*- coding: utf-8 -*-

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

import os
import sys
import unittest

from .. import setuptools_scm_versionfixer

class TestFuncs(unittest.TestCase):

    def setUp(self):
        self.old_env = dict(os.environ)

    def tearDown(self):
        os.environ.clear()
        os.environ.update(self.old_env)

    def test_always_sets(self):
        os.environ['SETUPTOOLS_SCM_PRETEND_VERSION'] = 'foo.bar'

        reports = []
        def report(msg, ver, file):
            reports.append((msg, ver, file))

        setuptools_scm_versionfixer.prereleaser_middle({
            'new_version': '1.0.0',
            'icrs.releaser:report': report,
        })

        self.assertEqual(reports, [
            ('Setting SETUPTOOLS_SCM_PRETEND_VERSION to', "'1.0.0'", sys.stderr)
        ])

if __name__ == '__main__':
    unittest.main()
