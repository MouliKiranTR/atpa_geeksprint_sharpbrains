[[_TOC_]]
# General Reminders
- Change status as you start work
- Always have a task for your work
- Always add QA tag (e.g. "QA: Emily")
- If you become blocked or otherwise stop work, change status to "blocked" and leave a comment on why

# New Feature Work (User Story)
Note: All development team stories should be "QA Ready" when assigned to testing.
1. Read any & all UAC to understand the new work
1. Change US status to "QA In Progress" and add QA tag for yourself (e.g. "QA: Emily")
1. Create child tasks following [task template](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/1168/QA-Task-Template) (e.g. manual, automation)
1. Go to CI and make sure Checkpoint has a recent build (Build is named yyyy MM dd without spacing). You can hover for a slightly more verbose version with "yyyy-MM-dd_hh_mm_ss":
![image.png](/.attachments/image-9f03157f-2fa7-43ab-b440-620237cc29ce.png)
1. Mark your manual task as "active"
1. Follow the UAC steps to validate functionality, check in multiple browsers
1. Using the UAC as a guide, perform negative testing -> no unexpected behavior occurs in other features due to this new work
1. If you notice anything odd during validation, check for any other user stories that may be overlapping / causing odd behavior. If there aren't any or you aren't sure if they should be impacting this functionality, raise it to the team. **NOTE**: Depending on the team, you may send the story back to developer (switch to "Active" status and it should auto-populate) or open a new bug (be sure to link the US as related) for a new issue
1. Mark your manual task as "closed"
1. If you have an automation task, mark it "active"
   1. Create a Test Case following [test case template](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/1169/Test-Case-Template)
   1. Create a new branch following template: Name_Feature_UserStory# (e.g. Emily_NewsFilter_174623)
   1. Create the test following test code guidelines (link)
   1. Once complete, mark automation task "closed"
1. If everything looks good, change US status to "Resolved" and change assigned to Product Owner.


# Existing Feature Work (User Story)
Note: All development team stories should be "QA Ready" when assigned to testing.
1. Read any & all UAC to understand the new work
1. Change US status to "QA In Progress" and add QA tag for yourself (e.g. "QA: Emily")
1. Create child tasks following [task template](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/1168/QA-Task-Template) (e.g. manual, automation)
1. Go to CI and make sure Checkpoint has a recent build (Build is named yyyy MM dd without spacing). You can hover for a slightly more verbose version with "yyyy-MM-dd_hh_mm_ss":
![image.png](/.attachments/image-9f03157f-2fa7-43ab-b440-620237cc29ce.png)
1. Mark your manual task as "active"
1. Follow the UAC steps to validate functionality, check in multiple browsers
1. Using the UAC as a guide, perform negative testing -> no unexpected behavior occurs in other features due to this new work
1. If you notice anything odd during validation, check for any other user stories that may be overlapping / causing odd behavior. If there aren't any or you aren't sure if they should be impacting this functionality, raise it to the team. **NOTE**: Depending on the team, you may send the story back to developer (switch to "Active" status and it should auto-populate) or open a new bug (be sure to link the US as related) for a new issue
1. Mark your manual task as "closed"
1. If you have an automation task, mark it "active"
   1. Check for existing Test Case that overlaps the new work. If one exists, update the test steps to match new UAC
   1. Create a new branch following template: Name_Feature_UserStory# (e.g. Emily_NewsFilter_174623)
   1. Re-write the test following test code guidelines (or create new test as needed) (link)
   1. Make sure to run all tests that use any methods/tests that were changed to verify they are worked as expected after changes
   1. Once complete, mark automation task "closed"
1. If everything looks good, change US status to "Resolved" and change assigned to Product Owner.

# Bug fixes (Bug)
Note: Bugs should be "Resolved" when assigned to testing.
1. Read the steps to replicate the issue
1. Add QA tag for yourself (e.g. "QA: Emily")
1. Create child tasks following [task template](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/1168/QA-Task-Template) (e.g. manual, automation)
1. Go to CI and make sure Checkpoint has a recent build (Build is named yyyy MM dd without spacing). You can hover for a slightly more verbose version with "yyyy-MM-dd_hh_mm_ss":
![image.png](/.attachments/image-9f03157f-2fa7-43ab-b440-620237cc29ce.png)
1. Follow the test steps as laid out in the bug, verify the error/issue is no longer occurring and that the expected behavior is happening
1. Additionally, verify that other inputs are working as expected
1. If everything looks good, change bug status to "Closed"

# QA Enhancement (User Story)
Note: Story should be "New" when assigned to a team member.
1. If Story info has not been filled out, fill out using [QA enhancement user story template](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/1171/QA-Enhancement-User-Story-Template)
1. Mark the story as "Active" and add QA tag for yourself (e.g. "QA: Emily")
1. Under "Related Work" click Add link > New item NOTE: You MUST add at least one task for your work
   1. Set link type to "Child"
   1. Set work item type to "Task"
   1. Add title following template: [QA Enhancement] Enhancement Title - Task
   1. Click "Add link"
1. Set relevant task to "Active"
1. Do the work
1. When done, set task/US status to "Closed" 