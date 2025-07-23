For the last year or so, there has been several reports of some customers suddenly stopped receiving emails from checkpoint daily news. This reports were captured in the following user stories and few others:
1. https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_workitems/edit/165798
2. https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_workitems/edit/164583
3. https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_workitems/edit/164601
4. https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_workitems/edit/167373

The bugs are updated with the finding after we investigated the issue within checkpoint and the SMTP team. In the following section, we are going to explain the step-by-step process followed to analyze this issue.

**Steps followed**
1. Email logs may be found in [Datadog - Log Explorer](https://trta-cp-prod.datadoghq.com/logs?query=env%3Aprod-cp-use1%20service%3Awebapp%20&agg_m=count&agg_m_source=base&agg_q=filename&agg_q_source=base&agg_t=count&analyticsOptions=%5B%22bars%22%2C%22dog_classic%22%2Cnull%2Cnull%2C%22value%22%5D&cols=host%2Cservice&fromUser=true&messageDisplay=inline&refresh_mode=sliding&storage=hot&stream_sort=desc&top_n=100&top_o=top&viz=stream&x_missing=true&from_ts=1725894993672&to_ts=1728486993672&live=true):
    * Link already has filters for service webapp and env:prod-cp-use1
    * Set time filter for date when email was sent or wider
    * Add filter with email address for which emails are not delivered
    * Optionally specify filename filter in format newsEmailYY_MM_DD.log, but make sure that time filter includes all log items from log file
    * You may also try to filter by email subject using "Checkpoint Daily Updates" or "Week of ", here are several subject examples:
        * Checkpoint Daily Updates - 10/7/2024
        * Checkpoint State Tax Update 窶  Week of September 30, 2024
        * Checkpoint Payroll Update 窶  Week of September 30, 2024

2. Once we have the logs, we need to confirm that email was successfully sent for the specific user form checkpoint like this-
`"06:22:09:792 AM : info : CPEmailUserTask.doTaskImpl.sent, Message -  **e-mail sent to user**: i*****v - nlid: src:RIA - E-mail Address: i****v@yahoo.com - Source: src:RIA - Subject: Checkpoint Daily Updates - 8/14/2024  - sent # =79099 appId=1 - hash: ub9b4adbc"`
![image.png](/.attachments/image-7715afa2-9952-45b3-b263-fcf55ecdb58b.png)

3. Once, we see this confirmation from checkpoint logs, the next step would be to connect with DEVOPS team by creation of [DEVOPS request](https://devops.tr-tax-cp-preprod.aws-int.thomsonreuters.com/) asking for SMPT logs, and they will connect with the SMTP team by creating [Service Now request](https://thomsonreuters.service-now.com/sp?id=ticket&table=task&sys_id=35c4dec787819e54a88362cd0ebb3598).
DEVOPS will need the following information for the ticket for SMTP team:
    * Date and Time
    * Email address
    * From email address- For checkpoint it is Checkpointnews.Bounces@thomsonreuters.com 
Please note that, it is **not** "checkpoint.noreply@thomsonreuters.com"

4. Once all the information is provided DEVOPS will create a ticket for SMTP team and then the SMTP logs will be shared to us, based on which we can decide the next steps. For example, if the SMTP email sending failed because the receivers email provider was blocking checkpoints sender or it was sent successfully.

For reference, please see the comments in the aforementioned bugs that contains the details of the investigation. 

