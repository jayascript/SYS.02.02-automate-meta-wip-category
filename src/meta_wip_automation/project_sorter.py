"""
Project sorting module for neurodivergent-friendly task prioritization.
Implements priority calculation based on frontmatter tags and factors
specific to a neurodivergent (ASD Level 1/ADHD) thinking style.
"""


from datetime import datetime, timedelta

# Score mappings for different frontmatter values
ACCOUNTABILITY_SCORES = {
    'imminent': 3, # someone is going to ask about it w/n 24h
    'looming': 2,  # someone will ask about it in a week or two
    'distant': 1,  # someone will ask eventuallyu
    'off-radar': 0 # no one is going to ask about it
}

STATUS_SCORES = {
    'stuck': 3,   # need to make a decision
    'waiting': 2, # need to check in with someone or can't proceed
    'active': 1,  # good to proceed
    'done': 0     # exclude from prioritization
}

TIME_DISTORTION_SCORES = {
    'blink': 3,   # highest weight due to quick wins
    'balloon': 2, # gonna take longer than thought so need to check in
    'linear': 1,  # time estimate should match linear time
    'warp': 0     # will get sucked into hyperfocus, don't need urging to start
}

# The following score dictionary is inversely related to ease because:
# - Tasks that feel impossible need active prompting
# - Flow state tasks will be engaged with naturally
# - Higher scores create counterbalance to avoidance

EFFORT_SCORES = {
    'impossible': 3,
    'resist': 2,
    'push': 1,
    'flow': 0
}

# The following score dictionary is inversely implemented because:
# - Avoided tasks need external prompting
# - Tasks easily engaged with naturally receive attention
# - Deprioritization prevents hyperfocus on highly engaging but less "important" tasks

INTEREST_SCORES = {
    'avoiding': 3,
    'sparking': 2,
    'engaged': 1
}

URGENCY_SCORES = {
    'now': 3,
    'soon': 2,
    'later': 1,
    'ignore': 0
}

def get_recurrence_score(last_completed: datetime, recurrence_interval: int) -> int:
    """Calculate recurrence priority score.

    Args:
        last_completed: Date of last completion
        recurrence_interval: Days between recurrences

    Returns:
        0: Recently completed
        2: Due soon (≥75% of interval elapsed)
        3: Overdue (≥100% of interval elapsed)
    """
    days_since_completed = (datetime.now() - last_completed).days

    if days_since_completed >= recurrence_interval:
        return 3  # Overdue
    elif days_since_completed >= (recurrence_interval * 0.75):
        return 2  # Due soon
    return 0  # Recently completed
