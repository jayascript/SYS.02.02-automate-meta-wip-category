#!/usr/bin/env python3

import os
import sys
import tempfile
import unittest
from unittest.mock import patch, mock_open


from io import StringIO
from datetime import datetime


from meta_wip_automation.main import main


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


    def test_cli_invalid_option(self):
        """
        Test the CLI's handling of invalid options.

        This test verifies that the CLI correctly handles and reports errors
        when an invalid option is provided.

        Raises:
            SystemExit: Expected to be raised when an invalid option is provided
        """
        # Simulate calling the script with an invalid option
        with self.assertRaises(SystemExit) as cm:
            sys.argv = ['main.py', '--invalid-option']
            main()

        # Check that SystemExit is called with exit code 2 (command line syntax errors)
        self.assertEqual(cm.exception.code, 2)


    @patch('sys.stdout', new_callable=StringIO)
    def test_sort_with_files(self, mock_stdout):
        """Test sorting with specified README files."""
        # Create temporary test files
        with tempfile.NamedTemporaryFile(mode='w', suffix='.org', delete=False) as f1, \
             tempfile.NamedTemporaryFile(mode='w', suffix='.org', delete=False) as f2:

            # Write test content to files
            f1.write(
                """#+title: Project One
                #+PROJECT_ID: TST.00.01
                #+STATUS: active
                #+URGENCY: now
                """
            )

            f2.write(
                """#+title: Project Two
                #+PROJECT_ID: TST.00.02
                #+STATUS: stuck
                #+URGENCY: soon
                """
            )

            f1.flush()
            f2.flush()

            try:
                # Test sorting with files
                sys.argv = ['main.py', '--sort', f1.name, f2.name]
                main()

                output = mock_stdout.getvalue()
                # Check that both projects appear in output
                self.assertIn('Project One', output)
                self.assertIn('Project Two', output)
                self.assertIn('TST.00.01', output)
                self.assertIn('TST.00.02', output)

            finally:
                # Clean up temporary files
                os.unlink(f1.name)
                os.unlink(f2.name)


    @patch('sys.stderr', new_callable=StringIO) # Change from stdout to stderr
    def test_sort_with_nonexistent_file(self, mock_stderr):
        """Test sorting with a nonexistent file."""
        nonexistent_file = 'nonexistent.org'
        sys.argv = ['main.py', '--sort', nonexistent_file]
        main()
        error_output = mock_stderr.getvalue().lower()
        self.assertIn('readme file not found', error_output) # Check for specific error
        self.assertIn(nonexistent_file, error_output) # Check file name is in error

    @patch('sys.stderr', new_callable=StringIO) # Change from stdout from stderr
    def test_sort_with_invalid_content(self, mock_stderr):
        """Test sorting with invalid file content."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.org', delete=False) as f:
            f.write("Invalid content without proper frontmatter")
            f.flush()
            file_path = f.name

            try:
                sys.argv = ['main.py', '--sort', file_path]
                main()
                error_output = mock_stderr.getvalue()
                self.assertIn(f'Error processing {file_path}', error_output)
            finally:
                os.unlink(f.name)


if __name__ == '__main__':
    unittest.main()
