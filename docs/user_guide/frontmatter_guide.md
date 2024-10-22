# Frontmatter Guide for Neurodivergent Project Management

This guide details the frontmatter fields used in project README files, their values, and how they affect project prioritization. The system is designed to accommodate autistic and ADHD traits, helping surface important tasks that might otherwise be overlooked while preventing hyperfocus on less critical items.

## Basic Format

Frontmatter uses org-mode syntax at the top of each README file:

```org
#+title: Project Name
#+PROJECT_ID: SYS.00.00
#+STATUS: active
#+URGENCY: soon
# ... other fields ...
```

## Required Fields

### Basic Project Information

| Field | Description | Example |
|-------|-------------|---------|
| `title` | Project name | `#+title: Automate Meta WIP Category` |
| `PROJECT_ID` | Unique identifier | `#+PROJECT_ID: SYS.02.02` |
| `STATUS` | Current project state | `#+STATUS: active` |

### Priority-Related Fields

These fields directly affect project prioritization calculations.

#### 1. ACCOUNTABILITY (Weight: 5)
How soon someone will check on this project's progress.

| Value | Score | Meaning |
|-------|-------|---------|
| `imminent` | 3 | Someone will ask about it within 24 hours |
| `looming` | 2 | Someone will ask in a week or two |
| `distant` | 1 | Someone will ask eventually |
| `off-radar` | 0 | No one is tracking this |

#### 2. STATUS (Weight: 4)
Current state of the project.

| Value | Score | Meaning |
|-------|-------|---------|
| `stuck` | 3 | Need to make a decision to proceed |
| `waiting` | 2 | Need to check in with someone |
| `active` | 1 | Currently in progress |
| `done` | 0 | Completed |

#### 3. TIME_DISTORTION (Weight: 3)
How time perception affects this project.

| Value | Score | Meaning |
|-------|-------|---------|
| `blink` | 3 | Quick win potential |
| `balloon` | 2 | Will take longer than expected |
| `linear` | 1 | Time estimate is accurate |
| `warp` | 0 | High hyperfocus risk |

#### 4. EFFORT (Weight: 3)
How much resistance you feel toward starting.

| Value | Score | Meaning |
|-------|-------|---------|
| `impossible` | 3 | Feels insurmountable |
| `resist` | 2 | High resistance to starting |
| `push` | 1 | Some resistance but manageable |
| `flow` | 0 | Easily enters flow state |

#### 5. INTEREST (Weight: 2)
Current engagement level with the project.

| Value | Score | Meaning |
|-------|-------|---------|
| `avoiding` | 3 | Actively avoiding |
| `sparking` | 2 | Building potential interest |
| `engaged` | 1 | Already interested |

#### 6. URGENCY (Weight: 1)
Time pressure for completion.

| Value | Score | Meaning |
|-------|-------|---------|
| `now` | 3 | Must be done today |
| `soon` | 2 | Due within weeks |
| `later` | 1 | Due eventually |
| `ignore` | 0 | Not time-sensitive |

## Optional Fields

### Recurrence Information

For [recurring projects](./recurrence_guide.md) (like monthly reports), include these fields:

| Field | Description | Required | Example |
|-------|-------------|----------|---------|
| `RECURRENCE_INTERVAL` | Days between recurrences | Yes | `#+RECURRENCE_INTERVAL: 30` |
| `LAST_COMPLETED` | Date of last completion | Yes | `#+LAST_COMPLETED: 2024-03-01` |
| `RECURRENCE_TYPE` | Pattern description | No | `#+RECURRENCE_TYPE: monthly` |

### Project Management Fields

Additional fields for project organization:

| Field | Description | Example |
|-------|-------------|---------|
| `LOCATION_REQUIRED` | Where work happens | `#+LOCATION_REQUIRED: home_office` |
| `TECH_REQUIRED` | Required technology | `#+TECH_REQUIRED: asus-endeavour` |
| `DEPENDENCIES` | Required prerequisites | `#+DEPENDENCIES: SYS.02.01` |
| `TAGS` | Categorization tags | `#+TAGS: automation, adhd` |

## Example READMEs

### Recurring Project Example
```org
#+title: Monthly BPR Metrics
#+PROJECT_ID: WVN.41.10
#+STATUS: active
#+URGENCY: soon
#+INTEREST: avoiding
#+ACCOUNTABILITY: looming
#+TIME_DISTORTION: linear
#+EFFORT: push
#+RECURRENCE_INTERVAL: 30
#+LAST_COMPLETED: 2024-10-01
#+RECURRENCE_TYPE: monthly
#+LOCATION_REQUIRED: home_office
#+TECH_REQUIRED: work-laptop
#+TAGS: reporting, metrics
```

### One-Time Project Example
```org
#+title: Analytics Report
#+PROJECT_ID: WVN.62.08
#+STATUS: active
#+URGENCY: soon
#+INTEREST: sparking
#+ACCOUNTABILITY: distant
#+TIME_DISTORTION: balloon
#+EFFORT: resist
#+LOCATION_REQUIRED: home_office
#+TECH_REQUIRED: work-laptop
#+DEPENDENCIES: WVN.62.07
#+TAGS: analytics, visualization
```

## Priority Calculation

The system calculates [priority scores](../priority/weights.md) using:

1. Base priority from weighted scores:
```python
priority_score = (
    (5 × Accountability Score) +
    (4 × Status Score) +
    (3 × Time Distortion Score) +
    (3 × Effort Score) +
    (2 × Interest Score) +
    (2 × Recurrence Score) +
    (1 × Urgency Score)
)
```

2. Additional boosts for specific combinations:

    - Stuck + High Accountability: +5 points
    - Quick + Hard to Start: +3 points
    - Avoided + External Check-in: +4 points

## Best Practices

1. **Update Regularly:**
    - Review and update status fields weekly
    - Update `LAST_COMPLETED` immediately after completing recurring tasks
    - Adjust effort/interest levels as they change

2. **Be Honest:**
    - Use `impossible` and `avoiding` when true
    - Mark tasks as `stuck` when decisions are needed
    - Acknowledge when tasks will `balloon`

3. **Monitor Patterns:**
    - Watch for tasks that stay `stuck` too long
    - Notice which `effort` levels correlate with completion
    - Track how accurate your `TIME_DISTORTION` estimates are

4. **Use Tags Effectively:**
    - Include relevant subsystem references
    - Tag common bottlenecks or patterns
    - Mark tasks that often pair well together
