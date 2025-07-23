To Request the access for Checkpoint Database, please follow the below steps :

DB related changes for Checkpoint databases will be handled by DCO team. If there is a request for user creation on databases, a Service Now ticket must be opened to “ORACLE-SUPPORT-TR” team.
•	Normal CR for DB user creation [ Reference(for lower environments) : CHG1226153 ]
•	For Production env : CHG1226192
Change Request Creation has different Phases:
Draft ->  Planning -> Assessment -> Approval -> Implementation  -> closed/cancelled
Please find the below guidelines to open a CR to ORACLE-SUPPORT team 
1.	Always raise a Normal change (we have 3 types of CRs. Normal, Standard and Emergency). Once you select the normal change, the CR will be opened in draft stage. Fill in the details required and click on save to move the CR to planning state. ( Please refer the screenshot in this document for more information) 
2.	Make sure there is enough lead time as per the below table.  ( Any user creation request falls under Minor risk level). Risk Level is determined based on the inputs we give in the risk and impact section in the assessment phase. ( Please refer the screenshot in this document for more information) 
Risk Level	Production	Non-production
Minor	4 business days	48 hours (2 days)
Moderate	7 business days	48 hours (2 days)
High	7business days	48 hours (2 days)

3.	Each host requires a separate CR. Please refer the below example

•	A request to execute a create user script in Checkpoint-INT, Checkpoint-QA and Checkpoint- Pre-prod can be done through single CR (as they are running from same host c276kzf). For prod, it’s always a separate CR(with the host c725jtw).
•	Any change raised for below configuration Items by default adds “ORACLE-SUPPORT” and “APP-SUPPORT-TRTA-CPS-SYS” to group approvals and the CR must be approved by these groups to move to implementation phase.
Environment  	Host ( Configuration Item)	Service name	Database
CP Prod 	c725jtw , c767bmf	ckpprod_appservice	ORP601A
CP Pre-prod	c276kzf, c403jme	ckppreprod_appservice	ORU601A
CP QA	c276kzf, c403jme	ckpqa_appservice	ORT601A
CP INT	c276kzf, c403jme	ckpint_appservice	ORD601A

ORACLE-SUPPORT-TR  will read the description and create the user and the mandatory access to the user.

1. Mention the DB name in the description in which the change needs to be executed.
2. We shouldn’t schedule the CR (start and end time) but can choose the CR Request by date  which satisfies the lead time. Please submit the change till assessment phase.
3. Once the change is approved by cp-devops and ORACLE-SUPPORT-TR teams, it moves into implementation phase. Upon the completion, ORACLE-SUPPORT-TR will send us a communication and move the CR into closed state.

SCREENSHOTS FOR REFERENCE:

 


 
 

Note : Please refer the Change ticket provided above as a reference for the respective environments.



[To Request the access for Checkpoint Database.docx](/.attachments/To%20Request%20the%20access%20for%20Checkpoint%20Database-577781e7-6036-42f7-bdf5-0549b7d71a3e.docx)