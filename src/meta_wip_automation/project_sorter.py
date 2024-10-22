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
    """
    Calculate recurrence score based on last completion time and interval.

    Args:
        last_completed: DateTime of last task completion
        recurrence_interval: Number of days between recurrences

    Returns:
        int: Score (3 for overdue, 2 for due soon, 0 for recently completed)
    """
    days_since_completed = (datetime.now() - last_completed).days
    if days_since_completed >= recurrence_interval:
        return 3  # Overdue
    elif days_since_completed >= (recurrence_interval * 0.75):
        return 2  # Due soon
    return 0  # Recently completed

def calculate_priority(frontmatter: dict, last_completed: datetime = None,
                     recurrence_interval: int = None) -> float:
    """
    Calculate priority score for a project based on its frontmatter.

    Args:
        frontmatter: Dictionary of project frontmatter
        last_completed: Optional datetime of last completion
        recurrence_interval: Optional interval for recurring tasks

    Returns:
        float: Priority score
    """
    # Return 0 priority for completed projects
    if frontmatter.get('STATUS') == 'done':
        return 0

    # Get base scores with defaults for missing values
    accountability_score = ACCOUNTABILITY_SCORES.get(
        frontmatter.get('ACCOUNTABILITY', 'off-radar'), 0)
    status_score = STATUS_SCORES.get(
        frontmatter.get('STATUS', 'active'), 0)
    time_distortion_score = TIME_DISTORTION_SCORES.get(
        frontmatter.get('TIME_DISTORTION', 'linear'), 0)
    effort_score = EFFORT_SCORES.get(
        frontmatter.get('EFFORT', 'push'), 0)
    interest_score = INTEREST_SCORES.get(
        frontmatter.get('INTEREST', 'sparking'), 0)
    urgency_score = URGENCY_SCORES.get(
        frontmatter.get('URGENCY', 'later'), 0)

    # Calculate recurrence score if applicable
    recurrence_score = 0
    if last_completed and recurrence_interval:
        recurrence_score = get_recurrence_score(last_completed, recurrence_interval)

    # Calculate base priority score using correct weights
    priority_score = (
        (5 * accountability_score) +    # Accountability weight: 5
        (4 * status_score) +           # Status weight: 4
        (3 * time_distortion_score) +  # Time distortion weight: 3
        (3 * effort_score) +           # Effort weight: 3
        (2 * interest_score) +         # Interest weight: 2
        (2 * recurrence_score) +       # Recurrence weight: 2
        (1 * urgency_score)            # Urgency weight: 1
    )

    # Apply interaction effect boosts
    if accountability_score >= 2 and status_score == 3:  # Stuck + High Accountability
        priority_score += 5

    if (time_distortion_score == 3 and  # Quick win (blink)
        effort_score >= 2):             # Hard to start (impossible/resist)
        priority_score += 3

    if (interest_score == 3 and         # Avoiding
        accountability_score >= 2):     # Imminent/Looming accountability
        priority_score += 4

    return priority_score

def sort_projects(projects: list) -> list:
    """
    Sort a list of projects based on their priority scores.

    Args:
        projects: List of tuples (frontmatter, last_completed, recurrence_interval)

    Returns:
        list: Sorted projects in descending priority order
    """
    def get_project_score(project):
        frontmatter, last_completed, recurrence_interval = project
        return calculate_priority(frontmatter, last_completed, recurrence_interval)

    return sorted(projects, key=get_project_score, reverse=True)
