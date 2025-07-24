### Intro
Occasionally developers will get tasked with gathering Product Insight info for the business to make decisions. Product Insight is another place where we track user analytics/info such as clicks, search info, etc. similar to Pendo. 

### Getting Started
In order to access Product Insight info, we will first need to gain access to Snowflake. Snowflake is a tool used to view the Enterprise Data Lake where the PI info is stored. [More info on Snowflake and the EDL here](https://trten.sharepoint.com/sites/intr-enterprise-data-lake/SitePages/AccessingEDL.aspx?xsdata=MDV8MDF8fDg0OGRlMTAzOWEwNTQyZGFmOTUzMDhkYjE5OWNkMzM4fDYyY2NiODY0NmExYTRiNWQ4ZTFjMzk3ZGVjMWE4MjU4fDB8MHw2MzgxMzE5MzM1NTIzNzYxNDd8VW5rbm93bnxWR1ZoYlhOVFpXTjFjbWwwZVZObGNuWnBZMlY4ZXlKV0lqb2lNQzR3TGpBd01EQWlMQ0pRSWpvaVYybHVNeklpTENKQlRpSTZJazkwYUdWeUlpd2lWMVFpT2pFeGZRPT18MXxNVFkzTnpVNU5qVTFOREl3TXpzeE5qYzNOVGsyTlRVME1qQXpPekU1T2pJd056QmlaVGd5TFRJMlpUY3ROR1JqT0MxaE1qQTBMVEF5TlRNeFlXTm1abVpqTTE5bVpEbGhPREkzTVMxaFpqWmpMVFF6WVRRdE9UazRNUzFsTmpFMVpUaGpNR1poWXpSQWRXNXhMbWRpYkM1emNHRmpaWE09fDk5YTU2ZGY0NGFhYTRiMDBmOTUzMDhkYjE5OWNkMzM4fGNjZDE0M2NlZmNhZDRjOWZhODkzNWQyZDQyNjM5ZWE3&sdata=bUFVdjJQUUFjVE1hQmFQZHRTKzdOWEtYRUxlVjdKRFVvZnh2QkhZczFFYz0%3D&ovuser=62ccb864-6a1a-4b5d-8e1c-397dec1a8258%2CA.Schultz%40thomsonreuters.com&OR=Teams-HL&CT=1677596574067&clickparams=eyJBcHBOYW1lIjoiVGVhbXMtRGVza3RvcCIsIkFwcFZlcnNpb24iOiIyNy8yMzAxMDEwMDkxMyIsIkhhc0ZlZGVyYXRlZFVzZXIiOmZhbHNlfQ%3D%3D)

The first thing that needs to done is getting access to the TR-DataAndAnalytics ADO project. Follow this [link](https://trten.sharepoint.com/sites/intr-enterprise-data-lake/sitepages/EDL-In-Take-Request.aspx#instructions-to-request-snowflake-access-%28click-to-expand-collapse%29), this is where all the high level info on filling out the ADO ticket is, but this wiki will go in depth to what we should be selecting as Checkpoint Devs. Not sharing links for the next two steps in case they change, please follow the links in the Atrium document. 

After heading to the atrium link from above, the underlined link is where you will go to request access to the ADO project. You should receive an email confirming you have been invited to the project. After you have been invited, please head back to this Atrium Instructions page. Here we will click the **ADO ticket** link.
![image.png](/.attachments/image-690825f8-8f9d-4e6f-8caa-45d80d359f3b.png)


### Filling Out the ADO Ticket
Now that you have gained access to the ADO project and have clicked the ADO ticket link, there will be several fields that need to be filled out. The first section is simple and is the requestors details. This includes your name, TR user id, and the manager you report to. **Please remember to included the necessary prefix before your TR user id.**

The next section pertains to a Data Impact Assessment. Ignore this section for now.

The following section is Access Request Details. Please select the following options as the screenshot below ![image.png](/.attachments/image-b6b65e5a-ef38-4739-b270-7abfc07a8133.png)

If for some reason there is an issue with the DIA ID#, you will probably be contacted to fill out a new one. Head back up to the Data Impact Assessment section above and follow the instructions there. There will be a form to fill out, add as many details as you can to each question to help make the process easier.

The last section will be describing what roles and access you are wanting. For our purposes we will be only needing one item added to the list (screenshot below) - **EDL_PROD_USAGE_ANALYST_READ_ROLE**

![image.png](/.attachments/image-87cacdb8-c3f9-424f-a263-4d05e1fe49af.png)

After you have added the role to the list, you may now click Save on the ticket. Please make sure to click the Follow button next to the Save button to get updates on your ticket. It may take up to 48 hours to process your request. Once it is in an approved state from their side - the "owner" of our data will be tagged in the story and need to approve. If asked for what data you want accessed, reply again with **EDL_PROD_USAGE_ANALYST_READ_ROLE** After that it is a matter of a few hours for access to sync up.

### Accessing Snowflake
[Access Snowflake here](https://a206448_prod.us-east-1.snowflakecomputing.com/console/login#/?returnUrl=internal%2Fworksheet) after receiving approval. Click on sign in using Ping.

TODO - Demo in Tech meeting and upload info here


### Useful links
- [Snowflake](https://a206448_prod.us-east-1.snowflakecomputing.com/console/login#/?returnUrl=internal%2Fworksheet)
- [Example ticket](https://dev.azure.com/TR-DataAndAnalytics/Enterprise%20Data%20Lake/_workitems/edit/49390)
- [Atrium Instructions on gaining TR-DataAndAnalytics ADO project access]()
- [TR-DataAndAnalytics ADO project](https://dev.azure.com/TR-DataAndAnalytics/Enterprise%20Data%20Lake)
- [Atrium Instructions on accessing the EDL](https://trten.sharepoint.com/sites/intr-enterprise-data-lake/SitePages/AccessingEDL.aspx?xsdata=MDV8MDF8fDg0OGRlMTAzOWEwNTQyZGFmOTUzMDhkYjE5OWNkMzM4fDYyY2NiODY0NmExYTRiNWQ4ZTFjMzk3ZGVjMWE4MjU4fDB8MHw2MzgxMzE5MzM1NTIzNzYxNDd8VW5rbm93bnxWR1ZoYlhOVFpXTjFjbWwwZVZObGNuWnBZMlY4ZXlKV0lqb2lNQzR3TGpBd01EQWlMQ0pRSWpvaVYybHVNeklpTENKQlRpSTZJazkwYUdWeUlpd2lWMVFpT2pFeGZRPT18MXxNVFkzTnpVNU5qVTFOREl3TXpzeE5qYzNOVGsyTlRVME1qQXpPekU1T2pJd056QmlaVGd5TFRJMlpUY3ROR1JqT0MxaE1qQTBMVEF5TlRNeFlXTm1abVpqTTE5bVpEbGhPREkzTVMxaFpqWmpMVFF6WVRRdE9UazRNUzFsTmpFMVpUaGpNR1poWXpSQWRXNXhMbWRpYkM1emNHRmpaWE09fDk5YTU2ZGY0NGFhYTRiMDBmOTUzMDhkYjE5OWNkMzM4fGNjZDE0M2NlZmNhZDRjOWZhODkzNWQyZDQyNjM5ZWE3&sdata=bUFVdjJQUUFjVE1hQmFQZHRTKzdOWEtYRUxlVjdKRFVvZnh2QkhZczFFYz0%3D&ovuser=62ccb864-6a1a-4b5d-8e1c-397dec1a8258%2CA.Schultz%40thomsonreuters.com&OR=Teams-HL&CT=1677596574067&clickparams=eyJBcHBOYW1lIjoiVGVhbXMtRGVza3RvcCIsIkFwcFZlcnNpb24iOiIyNy8yMzAxMDEwMDkxMyIsIkhhc0ZlZGVyYXRlZFVzZXIiOmZhbHNlfQ%3D%3D)
- [More info on Snowflake and how to navigate](https://trten.sharepoint.com/:w:/r/sites/intr-enterprise-data-lake/_layouts/15/Doc.aspx?sourcedoc=%7B3F266D66-1416-406E-A47E-875D6EC9D578%7D&file=Snowflake%20database%20access.docx&_DSL=1&action=default&mobileredirect=true&cid=e9106c4e-89ae-46fa-83a9-d3027aa20293)
