# -*- coding: utf-8 -*-
"""
Tests for devremover.py

"""
import sys
import tempfile
import unittest
from pathlib import Path
from importlib.resources import files


class TestRegex(unittest.TestCase):

    def _callFUT(self, s):
        from ..devremover import _SETUP_PY_DEV_REQUIREMENT_MATCHER
        s = s.encode('utf-8') if isinstance(s, str) else s
        return _SETUP_PY_DEV_REQUIREMENT_MATCHER.search(s)

    def _matches(self, s):
        self.assertTrue(self._callFUT(s))

    def test_simple_matches(self):
        m = self._matches
        for example in (
            # double quotes
            '"icrs.releaser >= 1.0.dev0"',
            # single quotes
            "'icrs.releaser >= 1.0.dev0'",
            # Complex requirement
            '"icrs.releaser != 2.0,>=1.0.dev0"',
            # From PEP 508
            '\'requests [security,tests] >= 2.8.1.dev0, == 2.8.* ; python_version < "2.7"\'',
        ):
            with self.subTest(example):
                m(example)

                example = f"""
                install_requires = [
                    {example},
                ]
                """
                m(example)

    def _no_match(self, s):
        self.assertFalse(self._callFUT(s))

    def test_simple_non_matches(self):
        m = self._no_match
        for example in (
            # double quotes
            '"icrs.releaser >= 1.0"',
            # single quotes
            "'icrs.releaser >= 1.0'",
            # Complex requirement
            '"icrs.releaser != 2.0,>=1.0"',
            # From PEP 508
            '\'requests [security,tests] >= 2.8.1, == 2.8.* ; python_version < "2.7"\'',
            # A 'dev' substring in various places
            "'foo.dev'",
            "foo.dev.bar >= 1.0"
        ):
            with self.subTest(example):
                m(example)

                example = f"""
                install_requires = [
                    {example},
                ]
                """
                m(example)

class TestPrereleaser(unittest.TestCase):

    def setUp(self):
        super().setUp()
        self._reports = []

    def _report(self, *args, **_kw):
        self._reports.append(args)

    def _callFUT(self, data_dir):
        from ..devremover import prereleaser_before as fut
        data = {
            'reporoot': data_dir,
            'icrs.releaser:report': self._report,
        }
        return fut(data)

    def test_no_dev_dep(self):
        with tempfile.TemporaryDirectory(prefix='icrs_releaser_') as td:
            td = Path(td)
            setup = td / 'setup.py'

            example = files('icrs.releaser.tests') / 'example_setup.txt'
            setup.write_bytes(example.read_bytes())
            self._callFUT(td)
            self.assertTrue(self._reports)

    def test_found_dev_dep(self):
        from ..devremover import DevelopmentDependency
        with tempfile.TemporaryDirectory(prefix='icrs_releaser_') as td:
            td = Path(td)
            setup = td / 'setup.py'

            example = files('icrs.releaser.tests') / 'example_setup.txt'
            example = example.read_bytes()
            placeholder = b'# Placeholder'
            dev_dep = b"'icrs.releaser >= 1.0.dev0',"
            assert placeholder in example
            example = example.replace(placeholder, dev_dep)
            assert dev_dep in example

            setup.write_bytes(example)
            with self.assertRaisesRegex(DevelopmentDependency,
                                        '.*setup.py had development dependency: '
                                        + dev_dep.decode('utf-8')[:-2]):
                self._callFUT(td)

    def test_no_setup_file(self):
        with tempfile.TemporaryDirectory(prefix='icrs_releaser_') as td:
            self._callFUT(td)

        self.assertTrue(self._reports)
        self.assertEqual(2, len(self._reports))
        self.assertIn('does not exist', ' '.join(str(s) for s in self._reports[1]))

if __name__ == '__main__':
    unittest.main()
