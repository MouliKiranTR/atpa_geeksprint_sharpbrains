# What is WCMS?
WCMS (Web Content Management System) is an internal publishing tool which publishes container data to Novus. What is container data you might ask?  container data is a set of XPATH expressions for extracting the data from the existing NOVUS document.

WCMS is used by Editorial Associates to curate Editor's picks and other widgets 

# Setup product code in WCMS for Checkpoint Edge
## Request New Product Group
To request a new product group in WCMS, you can sent request to Thomson-Co-WCMS-Tech@thomsonreuters.com  In the email, you need to mention product group information, for Checkpoint it is Checkpoint Edge.  Below is a sample email for requesting a new product in WCMS.
![image.png](/.attachments/image-37746d82-1fc6-47ea-bd23-34268c0d2d42.png)

# Define artifact for the Checkpoint Edge Product Code
You can think of Artifact Type as an XML document structure in WCMS.

Below is a sample of CPEDGE artifact type we created for Checkpoint Topic Pages.
![image.png](/.attachments/image-e19a652f-32d3-4f07-a117-577ca862b4a3.png)

#User's guide to add/update/delete containers
Once you have all the above items completed, you can start adding containers to publish contents to NOVUS.  We have a created a user's guide on how to add/update/delete containers in WCMS.  Here is the [document](https://trten.sharepoint.com/:b:/r/sites/TRTAKSCheckpointAnswers/Shared%20Documents/General/01%20Projects/Topic%20Pages/Documentations/WCMS%20Container%20Creation%20Guide%20for%20Checkpoint%20Edge.pdf?csf=1&web=1&e=pn1UCJ) on the Sharepoint.

# NOVUS collection name for the published containers
Once the containers are published, the information can be found in NOVUS using the following NOVUS collection information.
## Novus collection set names
#### Production Environment: w_cb_wcms_cs
#### Test Environment: w_cb_wcmstst_cs

# Integrating WCMS collection set to Checkpoint Web App
After we have setup the product code in WCMS, we would need to integrate the WCMS collection set into cp-web-app's appEnvironmentData.xml so that we have the NOVUS source information.

## add WCMS non-prod and prod source


```
<!-- Sources for Topics page work -->
    <source id="wcms-nonprod">
        <environment>novusaws:prod</environment>
        <machine/>
        <summary-field/>
        <nl-query-set/>
        <guid-restriction-set/>
        <guid-restriction-field/>
        <docLocId>0</docLocId>
        <collection name="w_cb_wcmstst_cs" type="wcms_containers" is-collection-set="true"/>
    </source>
    <source id="wcms-prod">
        <environment>novusaws:prod</environment>
        <machine/>
        <summary-field/>
        <nl-query-set/>
        <guid-restriction-set/>
        <guid-restriction-field/>
        <docLocId>0</docLocId>
        <collection name="w_cb_wcms_cs" type="wcms_containers" is-collection-set="true"/>
    </source>
```


## Attach the source to the app-environment

    
```
<app-environment id="prod">
        <data-source idref="trta-prod"/>
        <data-source idref="legal-prod"/>
        <data-source idref="wcms-prod"/>
        <db-source idref="prod-db"/>
    </app-environment>
```

