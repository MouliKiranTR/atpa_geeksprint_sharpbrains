### Topic and Subtopic Data
The Topic and Subtopic data are extracted from GCS Taxonomy. Editorial manages this taxonomy of Topic and Subtopic for each Jurisdiction (such as Federal or State).  This location will be the source of truth for all topics and subtopics and any changes to the ITEM_CODE needs to be made here and the downstream processes (such as TIGRE, CPS) will process and changes.

### GCS - Global Content System - Content Console

Here is a screenshot of the Checkpoint Tax Topics in GCS
![image.png](/.attachments/image-ae0fcd6c-bd28-4a13-80cc-b250996e0856.png)

### TIGRE 
Tigre extract the Topic and Subtopics information from the GCS using their API endpoints.  Once the information is extract and the information is stored in TIGRE.

### OPUS
Opus is a tool to extract the Topic and Subtopic contents from the TIGRE and deliver the package to CPS for transformation and NOVUS loading

### CPS - Checkpoint Publishing System
CPS extract the CPTOPICS.pkg for transformation and Novus loading.

### NOVUS - topic and subtopic document
Here is the NOVUS GUID for the document: T0CPTPTopicsAndSubtopicsData

![image.png](/.attachments/image-516b16d2-85b4-4b1f-83b2-f5dab26474e0.png)

### Workflow diagram
Here is the workflow diagram how the Topic and Subtopics contents flow from the upstream (GCS) all the way to the downstream (NOVUS).
![image.png](/.attachments/image-1a9a561b-5b79-40a9-8f02-f26e4211355d.png)