# -*- coding: utf-8 -*-

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

import unittest
import os
import sys

from .. import removecflags

class TestFuncs(unittest.TestCase):

    def setUp(self):
        self.old_env = dict(os.environ)

    def tearDown(self):
        os.environ.clear()
        os.environ.update(self.old_env)

    def test_remove(self):
        FLAGS = (
            'CFLAGS',
            'CPPFLAGS',
            # Leave one out for branch coverage
            # 'CXXFLAGS',
            'LDFLAGS',
        )
        # Make sure it doesn't pre-exist
        os.environ.pop('CXXFLAGS', None)

        for k in FLAGS:
            os.environ[k] = k

        reports = []
        def report(msg, key, val, file):
            reports.append((msg, key, val, file))

        removecflags.prereleaser_before({'icrs.releaser:report': report})

        for k in FLAGS:
            self.assertIn(
                ("Removing potentially dangerous env setting",
                 k,
                 k,
                 sys.stderr),
                reports)
            self.assertNotIn(k, os.environ)

if __name__ == '__main__':
    unittest.main()
