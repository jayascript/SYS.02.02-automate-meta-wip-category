# Project Recurrence Handling

This document explains how the system handles both recurring and one-time projects through frontmatter configuration.

## Frontmatter Fields

Add these optional fields to your project's [frontmatter](./frontmatter_guide.md) to specify recurrence:

```org
#+RECURRENCE_INTERVAL: 30
#+LAST_COMPLETED: 2024-10-01
#+RECURRENCE_TYPE: monthly
```

### Field Definitions

| Field | Purpose | Example | Required  |
|-------|---------|---------|---|
| `RECURRENCE_INTERVAL`       |    Days between recurrences     | `30` for monthly        | Only for recurring   |
| `LAST_COMPLETED`       | Date of last completion         | `2024-10-01`         |  Only for recurring |
|       `RECURRENCE_TYPE` |        Type of recurrence pattern |      `monthly`, `weekly`   |  Optional |

## Priority Calculation

The system determines recurrence priority as follows:

1. **For one-time projects:**

    - `get_recurrence_score()` is not called
    - No recurrence-based priority adjustment is made
    - Project is prioritized based on other factors only
    
2. **For recurring projects:**

    - System calculates days since last completion
    - Priority increases as next recurrence approaches:
        - 0 points: Recently completed (<75% of interval)
        - 2 points: Due soon (≥75% of interval)
        - 3 points: Overdue (≥100% of interval)

For more information on prioritization, see [Priority Factors](../priority/weights.md).

### Example: Monthly Report Project

```org
#+title: Monthly BPR Metrics
#+PROJECT_ID: WVN.41.10
#+STATUS: active
#+URGENCY: soon
#+RECURRENCE_INTERVAL: 30
#+LAST_COMPLETED: 2024-03-01
#+RECURRENCE_TYPE: monthly
```

- Recurs first Thursday/Friday monthly
- `RECURRENCE_INTERVAL: 30`
- Priority increases as month progresses
- Gets "due soon" boost at ~22 days (75% of interval)
- Marked overdue at 30 days

### Example: One-Time Project

```org
#+title: Analytics Report
#+PROJECT_ID: WVN.62.08
#+STATUS: active
#+URGENCY: soon

No recurrence fields needed for one-time project
```

- No recurrence fields
- Priority based solely on other factors
- No automatic time-based priority adjustments

## Implementation Details

The `get_recurrence_score()` function handles this logic:

```python3
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
```

### Integration with Priority Calculation

The recurrence score is weighted at 2 in the final priority calculation:

```python3
priority_score = (
    # ... other factors ...
    (2 * recurrence_score) +  # Recurrence weight: 2
    # ... other factors ...
)
```

## Future Enhancements

Possible improvements to consider:

1. Support for more complex recurrence patterns:

    - Specific days of week/month
    - Multiple times per month
    - Irregular intervals
    
2. Configuration options for:

    - Custom "due soon" threshold
    - Variable scoring based on recurrence type

3. Integration with calendar systems for:

    - Automatic last completion updates
    - Due date visualization
    - Schedule conflict detection
     
!!! note "Frontmatter Updates"
    When implementing a recurring project:
    
    1. Always update `LAST_COMPLETED` after completion
    2. Set appropriate `RECURRENCE_INTERVAL` for the project
    3. Consider adding `RECURRENCE_TYPE` for future enhancements
