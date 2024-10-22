# Priority Factor Weights and Scoring

This document details the exact scoring system used for prioritizing tasks in our neurodivergent-friendly project management system. Each factor has been carefully weighted based on its impact on task completion and executive function management.

This scoring system is specifically designed to:

1. Prioritize tasks we might naturally avoid
2. Surface items needing decisions or follow-up
3. Leverage external accountability
4. Identify quick wins for momentum
5. Counterbalance hyperfocus tendencies
6. Reduce anxiety-driven prioritization

!!! warning
    **The weights and scores are fine-tuned for neurodivergent work patterns and should only be modified with careful consideration of their interdependencies.**

## Formula

The priority score is calculated using the following weighted formula:

```python
PRIORITY_SCORE = (
    (5 × Accountability Score) +  # Highest weight: external motivation
    (4 × Status Score) +          # Second highest: current state
    (3 × Time Distortion Score) + # Tied third: time perception
    (3 × Effort Score) +          # Tied third: resistance level
    (2 × Interest Score) +        # Tied fourth: engagement level
    (2 × Recurrence Score) +      # Tied fourth: repetition needs
    (1 × Urgency Score)           # Base weight: time pressure
)
```

### Accountability Scores (Weight: 5)

| Level | Score | Explanation |
| ------- | ------- | ------------- |
| `imminent` | 3 | Someone will ask about it within 24 hours |
| `looming` | 2 | Someone will ask about it in a week or two |
| `distant` | 1 | Someone will ask eventually |
| `off-radar` | 0 | No one is tracking this |

!!! note "Why Highest Weight?"
    External accountability is weighted highest (5) because it:

    - Creates concrete deadlines through social commitment
    - Provides external structure
    - Often indicates tasks that impact others
    - Helps overcome executive dysfunction through external motivation

### Status Scores (Weight: 4)

| Status | Score | Explanation |
| -------- | ------- | ------------- |
| `stuck` | 3 | Need to make a decision to proceed |
| `waiting` | 2 | Need to check in with someone or can't proceed |
| `active` | 1 | Good to proceed with work |
| `done` | 0 | Completed; excluded from prioritization |

!!! note "Why These Scores?"
    - `stuck` is highest because decisions often cause task paralysis
    - `waiting` is higher than `active` because it requires explicit follow-up
    - `active` tasks have momentum and need less prompting
    
!!! note "Why is `waiting` higher than `active`?"
    Tasks in `waiting` status are prioritized higher than `active` tasks because they:
    
    - Require explicit follow-up actions (checking in with others)
    - Can become blockers for other people
    - Are easy to forget about and let slip through the cracks
    - Often have external accountability

### Time Distortion Scores (Weight: 3)

| Perception | Score | Explanation |
| ------------ | ------- | ------------- |
| `blink` | 3 | Quick win potential; can be done faster than expected |
| `balloon` | 2 | Will take longer than initially estimated |
| `linear` | 1 | Time estimate is accurate |
| `warp` | 0 | High risk of hyperfocus; will naturally engage |

!!! note "Quick Wins Priority"
    - `blink` tasks are prioritized highest for momentum building
    - `balloon` tasks need attention before they expand too much
    - `warp` tasks are deprioritized as they'll naturally attract focus

!!! note "Why is `balloon` greater than `linear`?"
    Tasks marked as `balloon` are prioritized because:
    
    - They require more time than initially estimated
    - Starting them earlier prevents last-minute rushes
    - They may need to be broken down into smaller tasks
    - Time underestimation is common with ADHD
    
### Effort Scores (Weight: 3)

| Level | Score | Explanation |
| ------- | ------- | ------------- |
| `impossible` | 3 | Feels insurmountable; needs external push |
| `resist` | 2 | High resistance to starting |
| `push` | 1 | Some resistance but manageable |
| `flow` | 0 | Easily enters flow state |

!!! note "Inverse Effort Scoring"
    Scores are inversely related to ease because:

    - Tasks that feel impossible need active prompting
    - Flow state tasks will naturally be engaged with
    - Higher scores create counterbalance to avoidance

### Interest Scores (Weight: 2)

| Level | Score | Explanation |
| ------- | ------- | ------------- |
| `avoiding` | 3 | Actively avoiding engagement |
| `sparking` | 2 | Building potential interest |
| `engaged` | 1 | Already interested and engaging |

!!! note "Inverse Interest Scoring"
    Like effort, interest is scored inversely because:

    - Avoided tasks need system prompting
    - Engaged tasks will naturally receive attention
    - Prevents hyperfocus on highly engaging but less important tasks

### Urgency Scores (Weight: 1)

| Level | Score | Explanation |
| ------- | ------- | ------------- |
| `now` | 3 | Must be done today |
| `soon` | 2 | Due within a few weeks |
| `later` | 1 | Due eventually |
| `ignore` | 0 | Not time-sensitive |

!!! note "Base Weight"
    Urgency has lowest weight (1) because:

    - Pure time pressure is less effective for neurodivergent motivation
    - Other factors (accountability, status) better drive completion
    - Prevents anxiety-driven prioritization

## Implementation

!!! warning "Customization Needed"
    While these weights and scores are optimized for neurodivergent (AuDHD) workflows, you may need to adjust them based on:
    
    - Your specific executive dys/function patterns
    - Current support systems and tools
    - Workplace or project requirements
    - Life circumstances and energy levels
    - Success/failure patterns with different tasks types
    
### Interaction Effects

Some combinations of factors receive priority boosts:

1. **Stuck with Imminent Accountability:** +5 points

    - Prevents blocked tasks with impending check-ins from being forgotten
    - Creates urgency around decision-making
    - Encourages seeking help before accountability deadline
    
2. **Quick but Hard to Start:** +3 points

    - Combines `blink` time distortion with `impossible` or `resist` effort
    - Promotes tackling resistant tasks that are actually quick
    - Builds momentum through achievable victories
    - Helps overcome task paralysis with promise of quick completion
    
3. **Avoided with Looming Check-In:** +4 points

    - Combines `avoiding` interest with `imminent` or `looming` accountability
    - Prevents procrastination on tasks others are waiting for
    - Creates external structure for naturally avoided tasks

### Dynamic Adjustments

The system can support several types of adjustments:

- Weekly review and weight tweaking
- Temporary factor boosting for special circumstances
- Custom rules for specific project types
- Emergency priority overrides

!!! tip "Regular Reviews"
    Be sure to check in with the system to assess if the current weights are:
    
    - Helping you complete important tasks
    - Preventing excessive task avoidance
    - Supporting your executive function needs
    - Properly balancing external and internal motivation
    - Accurately reflecting your current capacity and circumstances
