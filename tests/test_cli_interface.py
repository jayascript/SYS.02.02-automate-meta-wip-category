#!/usr/bin/env python3

import unittest
from unittest.mock import patch
import sys
from io import StringIO


from src.main import main # Assuming your main CLI function is in src/main.py


class TestCLI(unittest.TestCase):
    """
    Test suite for the Command Line Interface (CLI) of the project sorting script.

    This suite ensures that the CLI correctly handles various input scenarios,
    including help requests and invalid options. It uses mock objects to simulate
    system output and input for testing purposes.
    """

    @patch('sys.stdout', new_callable=StringIO)
    def test_cli_help_option(self, mock_stdout):
        """
        Test that the CLI correctly handles the --help option.

        This test ensures that when the --help option is provided, the CLI
        prints out usage information including available options.

        Args:
            mock_stdout (StringIO): Mock object to capture system output.

        Raises:
            SystemExit: Expected when the --help option is provided.
        """
        # Simulate calling the script with the --help option
        with self.assertRaises(SystemExit) as cm:
            sys.argv = ['main.py', '--help']
            main()
        
        # Check that the help text is printed and contains expected information 
        output = mock_stdout.getvalue().lower()
        self.assertIn("usage:", output)
        self.assertIn("options:", output)
        self.assertIn("--help", output)

        # Check that SystemExit is called with exit code 0 (indicating success)
        self.assertEqual(cm.exception.code, 0)


if __name__ == '__main__':
    unittest.main()
