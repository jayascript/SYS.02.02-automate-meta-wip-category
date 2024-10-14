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
    sample_content = """
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
    result = parse_readme(sample_content)
    assert isinstance(result, str)
    assert "Project Overview" in results
    assert "Goals" in result


def test_extract_frontmatter():
    """
    Test that the extract_frontmatter function correctly extracts data.

    This test verifies that:
        1. The function returns a dictionary.
        2. All expected frontmatter fields are present in the dictionary.
        3. The values of the extracted fields are of the correct type and format.

    The test allows for some flexibility in the exact format of certain fields,
    such as ESTIMATED_TIME, to account for variations in README structures.
    """
    sample_content = """
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
    frontmatter = extract_frontmatter(sample_content)
    assert isinstance(frontmatter, dict)
    assert frontmatter['title'] == 'Sample Project'
    assert frontmatter['PROJECT_ID'] == 'SYS.00.00'
    assert frontmatter['STATUS'] in ['active', 'stuck', 'waiting', 'done']
    assert frontmatter['URGENCY'] in ['now', 'soon', 'later', 'ignore']
    assert frontmatter['INTEREST'] in ['engaged', 'sparking', 'avoiding']
    assert frontmatter['ACCOUNTABILITY'] in ['imminent', 'looming', 'distant', 'off-radar']
    assert frontmatter['TIME_DISTORTION'] in ['balloon', 'blink', 'warp', 'linear']
    assert frontmatter['EFFORT'] in ['flow', 'push', 'resist', 'impossible']
    assert isinstance(frontmatter['LOCATION_REQUIRED'], str)
    assert isinstance(frontmatter['TECH_REQUIRED'], str)
    assert 'DEPENDENCIES' in frontmatter
    assert isinstance(frontmatter['TAGS'], str)


def test_extract_frontmatter_missing_fields():
    """
    Test that extract_frontmatter handles missing fields gracefully.

    This test ensures that:
        1. The function returns a dictionary even when some expected fields
           are missing.
        2. Present fields are correctly extracted.
        3. Missing fields are not included in the returned dictionary.

    The test uses sample README content with only some of the expected fields.
    """
    sample_content = """
    #+title: Sample Project
    #+PROJECT_ID: SYS.00.00
    #+STATUS: active

    * SYS.00.00 Sample Project
    ** Project Overview
    This is a sample project for testing purposes.
    """
    frontmatter = extract_frontmatter(sample_content)
    assert isinstance(frontmatter, dict)
    assert frontmatter['title'] == "Sample Project"
    assert frontmatter['PROJECT_ID'] == "SYS.00.00"
    assert frontmatter['STATUS'] == 'active'
    assert 'URGENCY' not in frontmatter
    assert 'INTEREST' not in frontmatter


def test_parse_readme_file_not_found():
    """
    Test that parse_readme raises a FileNotFoundError for non-existent files.

    This test verifies that:
        1. The function raises the appropriate error, given a non-existent path.
        2. The error handling is working as expected for invalid inputs.

    The test attempts to parse a file that doesn't exist.
    """
    with pytest.raises(FileNotFoundError):
        parse_readme('non_existent_file.md')
