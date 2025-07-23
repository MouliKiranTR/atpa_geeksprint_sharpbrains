# High Level Background
**Asset ID:** a203669

CUAS is used to do entitlement for multiple applications, with it being a middleman for Proview purchases. When an order is placed in the Tax and Accounting eStore for a Proview title, the order gets submitted to CUAS and to the order management system (Unison). When the order gets submitted to CUAS it is for immediate fulfillment, as the order management system takes a day for it to take place through the nightly process.

In the CUAS Product Management area you will find products with a type of Checkpoint or eReader. The eReader products correspond to Proview titles. These eReader products can have ODSs added to them. In this case is is more like a Combo Checkpoint and eReader. They might do this to give the customer access to special materials referenced in the Proview content. This is usually not the case but it does happen occasionally.

So at a high level the flow is (eStore title purchased -> CUAS configures the product code for that user -> eReader Batch Jobs pick up the configured orders and communicates the entitlement to Boomi and OnePass).

# eReader Assign/De-assign Batch Job
When a user purchases an eReader product the information has to be recorded in the CUAS DB ext_app_tran table. This can be done through multiple ways (i.e triggers) with one of them being through the eReader Assign/De-assign Batch Job.

The eReader Assign/De-assign Batch Job invokes a stored procedure to gather the orders from CUAS and inserts them as new records into the ext_app_tran table. It selects orders based on the below criteria -
- **Package Type** = 17 (this means it is an eReader type of product)
- **Change Date** = yesterday (this means it picks up orders made the day before)
- **End Date** = today or in the future
- **Order Status** = must be in active, future cancel, trial, or complimentary (1, 3, 4, 6)

For each order that meets the criteria above it inserts a record into the ext_app_tran table with status set to 'INITIAL' and action set to 'ASSIGN_USR_ORDER'.

# eReader Batch Job
The eReader Batch Job in a way picks up where the eReader Assign/De-assign Batch Job leaves off. In the ext_app_tran table it picks all of the records with status 'INITIAL' and starts processing them. For records with the action 'ASSING_USR_ORDER", the eReader Batch Job communicate out to Boomi for sending out the entitlement mails to the end customer.

This job is currently scheduled using CronJob to run every 5 minutes.

# Repos
https://github.com/tr/cuas-ereader
https://github.com/tr/cp_cuas-ereader-assign-deassign-batch

# Reference Images
![Proview Entitlement via Token.png](/.attachments/Proview%20Entitlement%20via%20Token-db919b7b-8e27-41f1-853c-311dd1eede16.png)

---
_All information courtesy of Sam Lewis and Vishal Rana_
