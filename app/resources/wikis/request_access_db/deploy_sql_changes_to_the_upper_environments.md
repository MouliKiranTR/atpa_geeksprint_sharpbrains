[**Checkpoint Flyway Cumulus Project**]([tr/cp_web-app-dbchange: Checkpoint Research and Consolidated CUAS Shared DB Scripts](https://github.com/tr/cp_web-app-dbchange))  is utilized to execute SQL scripts (both DDL and DML) against relational databases such as AWS RDS and Aurora. The project leverages the Cumulus project's CLI to create a database change pipeline in specified environment accounts.

Here is the process to deploy DB changes to the upper environments:

- **CI** - automatic
- **DEMO** - Email request to promote changes in demo, including CM (thomson-platformgrpcm-cobalt@thomsonreuters.com) and CSS (thomson-cobalt-services-support@thomsonreuters.com) teams.
- **QED** - Official CR with 24-48 hours lead time
- **UAT** - Automatically goes after QED and
- **PROD** - Official CR with 4 days lead time

When we push any database changes to the ([cp_web-app-dbchange]([tr/cp_web-app-dbchange: Checkpoint Research and Consolidated CUAS Shared DB Scripts](https://github.com/tr/cp_web-app-dbchange)) repository, the changes are automatically deployed to the CI environment. The same changes would go to upper environments by approving the Cumulus CodePipeline in upper environments.

To promote the changes to the DEMO environment, please send an email to Platform CM, Cobalt Services Support, and West DBA teams (west-west-devdba@thomsonreuters.com). Here is an example email:

_could you please promote/approve the latest changes in our Flyway pipeline from CI to Demo?
[https://us-east-1.console.aws.amazon.com/codesuite/codepipeline/pipelines/a203669-trtadb-cumulus-db-flyway-pipeline/view?region=us-east-1#](https://us-east-1.console.aws.amazon.com/codesuite/codepipeline/pipelines/a203669-trtadb-cumulus-db-flyway-pipeline/view?region=us-east-1# "https://us-east-1.console.aws.amazon.com/codesuite/codepipeline/pipelines/a203669-trtadb-cumulus-db-flyway-pipeline/view?region=us-east-1#")_

The request could also be initiated through **CP Flyway Pipeline approvals/issues** Teams chat too. Please ask Miguel, Mostafijur, or Will to add you to the corresponding Teams chat.

Also, here is an example CR to promote the DB changes to the PROD environment - [Ticket Form - ServiceNow](https://thomsonreuters.service-now.com/sp?id=ticket&table=change_request&sys_id=44df3ffc1b529650cb8f0dc5604bcb77)
ServiceNow CR Template - [Change request - ServiceNow](https://thomsonreuters.service-now.com/sp?id=sc_cat_item&sys_id=eb707095136f7a40f05c7e276144b0ea)