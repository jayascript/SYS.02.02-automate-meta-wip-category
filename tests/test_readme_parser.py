#!/usr/bin/env python3

import pytest
from src.readme_parser import parse_readme, extract_frontmatter


def test_parse_readme():
    """
    Test that the parse_readme function correctly reads a README file.

    This test ensures that:
        1. The function returns a string.
        2. The returned string contains the title from the frontmatter.
        3. The returned string contains the main content of the README.

    The test uses a sample README string with a structure matching the
    actual project READMEs.
    """
    sample_readme = """
    #+title: Sample Project
    #+PROJECT_ID: SYS.00.00
    #+STATUS: active
    #+URGENCY: high
    #+INTEREST: high
    #+ENERGY_REQUIRED: medium
    #+LOCATION_REQUIRED: home_office
    #+TECH_REQUIRED: asus-endeavour
    #+ESTIMATED_TIME: 10 HOURS
    #+DIFFICULTY: medium
    #+DEPENDENCIES:
    #+TAGS: sample, test

    * SYS.00.00 Sample Project
    ** Project Overview
    This is a sample project for testing purposes.
    ** Goals
    1. Test README parsing
    2. Verify frontmatter extraction
    """

    result = parse_readme(sample_readme)
    assert isinstance(result, str)
    assert "Sample Project" in result
    assert "Project Overview" in results
    assert "Goals" in result
