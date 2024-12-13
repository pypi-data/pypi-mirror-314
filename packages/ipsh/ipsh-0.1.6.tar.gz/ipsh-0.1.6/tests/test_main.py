# -*- coding: utf-8 -*-

"""
test the ipsh.main module
"""

import io

from unittest import TestCase

from unittest.mock import patch

from ipsh import main as pkg_main


class Run(TestCase):
    """Test the run() function"""

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_version(self, mock_stdout: io.StringIO) -> None:
        """execute() method, version output"""
        with self.assertRaises(SystemExit) as cmgr:
            pkg_main.run("--version", test_context=True)
        #
        self.assertEqual(cmgr.exception.code, 0)
        self.assertEqual(
            mock_stdout.getvalue().strip(),
            pkg_main.__version__,
        )
