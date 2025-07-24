       
**TrackIt Notifications**

How can we enable TrackIt for Documents?
========================================

When we open a document, you'll notice the TrackIt button, which allows us to enable notifications for that specific document.  
![Picture1.png](/.attachments/Picture1-c831f05c-9ca4-4905-a648-ad0e71932efe.png)

Where is the data for TrackIt documents stored?
===============================================

The data for TrackIt is stored in the **user_cite_alert** table, and you can search for your data by filtering based on your dbId.  
  
![Picture2.png](/.attachments/Picture2-b594b035-06be-4cfc-965e-f849a4d96fa5.png)

Where is the data for citated documents stored?
===============================================

The data for Citated document is stored in the **cite_link_web_app** table, and you can search for your document either by **citing_doc_pid** or **cited_doc_pid**.  
  
![Picture3.png](/.attachments/Picture3-e7b8b99e-dba4-4ce5-bacd-03ee0f59ff97.png)

  
How can we get the Notification Email for citated and expired documents?
===========================================================================

Prerequisite:
-------------

1) Make sure your username should be present in **nlTestMailList** of **appBase.properties**
![Picture4.png](/.attachments/Picture4-1d89d213-2750-4de8-81ac-08588f37b1a4.png) 
  
2) Make sure your email id is part of Checkpoint Development Team distribution group

Run Batch Process
-----------------

We need to execute the Batch Process from the admin portal using the following link:  
Dev: [https://dev.checkpoint.thomsonreuters.com/app/admin](https://dev.checkpoint.thomsonreuters.com/app/admin)
QA: [https://qa.checkpoint.thomsonreuters.com/app/admin](https://qa.checkpoint.thomsonreuters.com/app/admin)
PreProd: [https://preprod.checkpoint.thomsonreuters.com/app/admin](https://preprod.checkpoint.thomsonreuters.com/app/admin)

After logging in, we need to select Batch Process 30 and run that process  
  
![Picture5.png](/.attachments/Picture5-fb98f53f-54a8-4ac1-a632-88f553369498.png)
  
You can find the logs in Datadog: [Log Explorer | Datadog](https://trta-cp-prod.datadoghq.com/logs?query=source%3Acitealert%20env%3Aci-cp-use1&agg_m=count&agg_m_source=base&agg_t=count&cols=host%2Cservice&fromUser=true&messageDisplay=inline&refresh_mode=sliding&storage=hot&stream_sort=desc&viz=stream&from_ts=1731345903023&to_ts=1733937903023&live=true)

Emails:
-------

Once Batch Process is completed you can find the Notification in your email:  
  
![Picture6.jpg](/.attachments/Picture6-78236210-60ab-48ed-ba9f-8bbc286bac15.jpg)

![Picture7.jpg](/.attachments/Picture7-9ce68758-c644-469f-82d8-80949921ae55.jpg)

![Picture8.jpg](/.attachments/Picture8-73088122-ca00-4e15-97bc-e0a6f7456769.jpg)