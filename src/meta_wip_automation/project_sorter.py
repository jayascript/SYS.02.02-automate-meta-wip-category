"""
Project sorting module for neurodivergent-friendly task prioritization.
Implements priority calculation based on frontmatter tags and factors
specific to a neurodivergent (ASD Level 1/ADHD) thinking style.
"""


from datetime import datetime, timedelta

# Score mappings for different frontmatter values
ACCOUNTABILITY_SCORES = {
    'imminent': 3,
    'looming': 2,
    'distant': 1,
    'off-radar': 0
}

STATUS_SCORES = {
    'stuck': 3,
    'waiting': 2,
    'active': 1,
    'done': 0
}
