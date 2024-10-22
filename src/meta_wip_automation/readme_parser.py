#!/usr/bin/env python3

"""
README parser for Neurodivergent Project Management System

This module provides functionality to parse README files and extract frontmatter
information for a project management system tailored for neurodivergence,
with a focus on being useful to autistics and/or ADHDers.

Functions:
    parse_readme(file_path: str) -> str
    extract_frontmatter(content: str) -> dict

Frontmatter Fields and Values:
    The following fields use customized priority levels:

    1. URGENCY:
        - "now"        : Must be done today.
        - "soon"       : By the end of this week or next.
        - "later"      : It's coming up, but not an immediate focus.
        - "ignore"     : Over a month away, not in immediate focus.

    2. STATUS:
        - "active"     : Thinking about it or working on it.
        - "stuck"      : Blocked by external or internal factors.
        - "waiting"    : Handed off or waiting on input from others.
        - "done"       : Completed.

    3. INTEREST
        - "engaged"    : Hyperfocused and deeply into the task.
        - "sparking"   : Trying to make the task interesting enough to start.
        - "avoiding"   : Likely to put off due to tedium or lack of interest.

    4. ACCOUNTABILITY
        - "imminent"   : Someone's about to check in or hold you accountable.
        - "looming"    : Accountability is coming, but with some breathing room.
        - "distant"    : Eventually accountable but no one's checking right now.
        - "off-radar"  : No external accountability in sight.

    5. TIME_DISTORTION
        - "balloon"    : Likely to take much longer than initially thought.
        - "blink"      : Turns out to be much quicker than expected.
        - "warp"       : Likely to lose track of time and hyperfocus for hours.
        - "linear"     : Straightforward, time expectations likely accurate.

    6. EFFORT:
        - "flow"       : Will enter a state of flow easily; minimal resistance.
        - "push"       : Needs a bit of effort to start, but manageable.
        - "resist"     : High resistance; likely to procrastinate without help.
        - "impossible" : Feels like a brick wall; avoid until last possible sec.

For more detailed information on frontmatter fields and their usage,
please refer to the frontmatter_guide.md (#TODO) in the docs directory.
"""
import re
from collections import defaultdict

def parse_readme(file_path: str) -> str:
    """
    Parse a README file and return its contents as a string.

    Args:
        file_path (str): THe path to the README file.

    Returns:
        str: The contents of the README file.

    Raises:
        FileNotFoundError: If the specified file does not exist.
    """
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"README file not found: {file_path}")


def extract_frontmatter(content: str) -> dict:
    """
    Extract frontmatter from the given content.

    This function parses the content for frontmatter fields, including the
    neurodivergent-friendly priority levels described in the module docstring.

    Args:
        content (str): The content of the README file.

    Returns:
        dict: A dictionary containing the extracted fields and their values.
    """
    frontmatter = defaultdict(str)
    lines = content.strip().split('\n')
    for line in lines:
        line = line.strip() # Remove leading/trailing whitespace
        if line.startswith('#+'): # Locate frontmatter using org-mode properties
            key, value = line[2:].split(':', 1)
            frontmatter[key.strip()] = value.strip()
        elif line.startswith('*'): # Stop when we reach the main content
            break
    return dict(frontmatter)


# Additional helper functions can be added here as needed
