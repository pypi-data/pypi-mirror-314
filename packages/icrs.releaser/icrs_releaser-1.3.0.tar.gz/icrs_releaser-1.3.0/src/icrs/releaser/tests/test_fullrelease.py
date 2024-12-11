# -*- coding: utf-8 -*-

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

import unittest

class TestFullrelease(unittest.TestCase):

    def test_import(self):
        from .. import fullrelease
        self.assertIsNotNone(fullrelease)


if __name__ == '__main__':
    unittest.main()
