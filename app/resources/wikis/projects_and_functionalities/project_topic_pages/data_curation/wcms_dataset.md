# WCMS Dataset
WCMS data are created by WCMS container feeders, each container can have multiple feeders.  The feeders are responsible for curating the contents based on NOVUS queries and collection sets.

## WCMS Container
A WCMS container contains a list of feeders, the feeder is responsible to generate the list of artifacts if there's a match with NOVUS query and XML parser configuratio using the XPath expression.

Here is an example of WCMS container, the fields denoted with * are required fields.
![image.png](/.attachments/image-386ba223-60aa-4abd-9d9b-8a76df679f6a.png)

## Feeder
A feeder requires a feeder name, Novus collection set, NOVUS Query, and Parser configuration information

See an example below:
![image.png](/.attachments/image-00c3a880-0254-414b-a64d-43b8fd2be0fe.png)

## Parser Configuration
A parser configuration requires XPATH expression to extract the values from the XML document based on the NOVUS Query results.

See an example below:
![image.png](/.attachments/image-b99f87e0-d5d8-4f92-9fd6-de738cdc36e8.png)

## Publish to Novus
The documents that matches the conditions defined in the feeder will show up in the artifacts list window.  The documents listed on the "Active" canvas are the documents published to NOVUS.
### Artifact list
![image.png](/.attachments/image-bd4c6aee-56ca-4b6e-940f-1db8915ec41e.png)

### Active canvas
The artifacts listed under the "Active canvas" are the artifacts already published to NOVUS.

![image.png](/.attachments/image-1f4c752f-b88a-4234-be53-28bc82b9d7e1.png)

## Example of published artifacts in NOVUS

### Use Easel to query the published documents.
You can use Easel to view what is published for a specific container. 

#### Easel URLs:
##### Production: https://easel-prod.1667.aws-int.thomsonreuters.com/easel/
##### Client: https://easel-client.1667.aws-int.thomsonreuters.com/easel

#### WCMS Collection set names
##### Production: w_cb_wcms_cs
##### Test: w_cb_wcmstst_cs

Here is an example of querying the artifacts for container GrossIncome-LMATT-State

`=wcms.md.container.id("GrossIncome-LMATT-State")`

Here is an example of query the artifact with product code, topic code, container type and container name.

`=artifact.product.code("CPEDGE") AND =artifact.container.type("LMATT") AND 
 =artifact.topic.code("GROSS_INCOME") AND =wcms.md.container.id("GrossIncome-LMATT-State")`

![image.png](/.attachments/image-6dbd2cd7-7a61-4d25-8c3c-78a17c9b2418.png)


