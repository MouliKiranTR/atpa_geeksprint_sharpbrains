# Batch

## Overview
- What is batch

## How Batch is Triggered
- SCHED_TYPE_ON_DEMAND- schedule type of not scheduling it
    - can run on server but will not run automatically.
        - text: Not Scheduled
- SCHED_TYPE_FIXED- schedule type of running at a fixed time each day
    - Run at next scheduled time
        - text: Next Sched
    - There is an error in the scheduled time.
        - text: Time Err=
    - There is an error in the scheduled time.
        - text: No time in config file.
    - which batch use this.... TODO
- SCHED_TYPE_PROMOTE- schedule type of running after a promote.
    - Runs on promote and should run now because data is different.
        - text: Do Promote
    - Runs on promote and data is different but its outside of promote window.
        - text: On Promote window
    - Runs on promote and does not need to run now.
        - text: Next Promote
- SCHED_TYPE_PROMOTE_MAX- schedule type of running once a day, at a promote or a the fixed time if the promote hasn't happened.
    - Runs on promote or schedule once a day and has already run so skip it.
        - text: On Promote skip (version has changed so run it & already run today, so run it so it will add a record not to run again)
        - text: On Promote window skip (on been promoted and window is less than next sched time. & already run today, so run it so it will add a record not to run again)
    - Runs on promote and should run now because data is different.
        - text: On Promote
    - Runs on promote and data is different but its outside of promote window.
        - text: On Promote window
    - Run at next scheduled time or promote which ever come 1st.
        - text: Next promote or Sched

### Determining Promote Events
- To find when a promote event occurred....

## Checking Batch Runs and Logs

