### Publication Mapping Data
The publication mapping data information is stored in the TIGRE database, the database is CPTOPICSCFG.  This database contains configuration information we need for displaying the mapped publication names, the reason we need this information is because the publication information we extracted from the XML is not meaningful, in order to display an easy to understand publication name, we mapped the short publication name to a more descriptive publication name.  For instance, a publication name called "PPCTDB" is not meaningful to some users.  So in order to make the publication name easy to read for users, this PPCTDB is mapped to "1040 Deskbook (PPC)" and the displayed publication name will be called "1040 Deskbook (PPC)".  Here is an example of displaying the mapped publication name on Checkpoint Topic Pages.

![image.png](/.attachments/image-96aeccea-c131-4f56-863e-9d5eddc0db05.png)

#### Novus GUID for this configuration file is T0CPTPTopicsAndSubtopicsConfig
You can find the XML configuration by using Easel at [Easel FindBy GUID Search](https://easel-prod.1667.aws-int.thomsonreuters.com/easel/FindByGUIDSearch.do)

Here is the screenshot:
![image.png](/.attachments/image-adecc053-02ef-4df8-8a1e-b30d3e61081e.png)

Here is snippet of XML configuration:

```
<publication>
<code>PPCTDB</code>
<name>1040 Deskbook (PPC)</name>
</publication>
```

Here is a snippet of JSON response for the publication name in cryptic format before the API transformation.

##### Before the transformation:

```
{
                    "title": "Selected Other Income Items.",
                    "sourceGuid": "iPPCTDB:2023d8bc24209c1100d",
                    "date": "20231201000000",
                    "publication": "PPCTDB",
                    "jurisdiction": "FEDERAL"
}
```
##### After the transformation:

```
{
                    "title": "Selected Other Income Items.",
                    "sourceGuid": "iPPCTDB:2023d8bc24209c1100d",
                    "date": "20231201000000",
                    "publication": "1040 Deskbook (PPC)",
                    "jurisdiction": "FEDERAL"
}
```



#### The process of updating the XML configuration 
To update the XML Configuration file, this will involve the Editorial, TIGRE, and CPS.

#### Editorial Team
The Editorial team is responsible for developing the new mapping data. Once the mapping is finalized, this information is shared with the TIGRE team

#### TIGRE Team
The TIGRE team is tasked with updating the CPTOPICSCFG database using the mapping data provided by the Editorial team. After updating the database, they notify the CPS team to proceed with the next steps.

#### CPS Team
The CPS Team willextract the CPTOPICSCFG database and process it on CPS Box. After done processing it, it will load the file to NOVUS and promote it to Checkpoint.




