#!/usr/bin/env python3

import os
import pytest

def test_readme_exists():
    assert os.path.isfile('README.org'), "README file does not exist"

def test_readme_content():
    with open('README.org', 'r') as f:
        content = f.read()
    assert "Automate Meta WIP Category" in content, "README does not contain expected project title"
    assert "Project Overview" in content, "README does not contain Project Overview section"
    # Add more assertions as needed to check for key sections
