# Ensure the directory tests/test_projects exists
# YOU MUST RUN THIS FILE FROM WITHIN tests/

# Regular recurring project (like your monthly BPR metrics)
cat > test_projects/WVN.41.10-README.org << EOL
#+title: Monthly BPR Metrics
#+PROJECT_ID: WVN.41.10
#+STATUS: active
#+URGENCY: soon
#+INTEREST: engaged
#+ACCOUNTABILITY: looming
#+TIME_DISTORTION: linear
#+EFFORT: push
#+RECURRENCE_INTERVAL: 30
#+LAST_COMPLETED: 2024-02-20
#+RECURRENCE_TYPE: monthly
#+LOCATION_REQUIRED: home_office
#+TECH_REQUIRED: work-laptop
#+TAGS: reporting, metrics
EOL

# Overdue recurring project
cat > test_projects/SYS.03.01-README.org << EOL
#+title: Weekly System Backup
#+PROJECT_ID: SYS.03.01
#+STATUS: active
#+URGENCY: now
#+INTEREST: avoiding
#+ACCOUNTABILITY: imminent
#+TIME_DISTORTION: blink
#+EFFORT: push
#+RECURRENCE_INTERVAL: 7
#+LAST_COMPLETED: 2024-02-01
#+RECURRENCE_TYPE: weekly
#+LOCATION_REQUIRED: home_office
#+TECH_REQUIRED: asus-endeavour
#+TAGS: maintenance, backup
EOL

# One-time project (like your analytics dashboard)
cat > test_projects/WVN.62.08-README.org << EOL
#+title: Analytics Dashboard
#+PROJECT_ID: WVN.62.08
#+STATUS: stuck
#+URGENCY: now
#+INTEREST: avoiding
#+ACCOUNTABILITY: imminent
#+TIME_DISTORTION: balloon
#+EFFORT: resist
#+LOCATION_REQUIRED: home_office
#+TECH_REQUIRED: asus-endeavour
#+DEPENDENCIES: WVN.62.07
#+TAGS: analytics, visualization
EOL
