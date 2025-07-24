## Topic and SubTopic Names
  
  ### Topic Pages Tree List View
The Topic Pages Tree List View is dynamically created from a NOVUS document. The selection of Topic Pages is managed by the Editorial team, which determines which Parent Topic and its subtopics are to be published.
#### The NOVUS document GUID
Below is the NOVUS GUID that contains the list of Topics and Subtopics
You can use Easel to find this XML document.  To find this document, point your browser to https://easel-client.1667.aws-int.thomsonreuters.com/easel/FindByGUID.do and click on “Find” tab and enter the following GUID in the text box: T0CPTPTopicsAndSubtopicsData
#### Tree List View Display Format
The Topics and SubTopics are organized into three evenly divided columns. For instance, with 10 Topics, we calculate the remainder by using modulus operation, which in this case is 1. This results in each column initially planned to display 3 topics, but the first column will include the extra one, leading to a distribution of 4-3-3. The same principle is applied if there are 20 SubTopics, where the remainder is 2. These two extra SubTopics are distributed to the first and second columns, resulting in a final arrangement of 7-7-6.
For those interested in coding, here is the code snippet:

```
<div
  class="topics-list"
  *ngFor="let topics of topicsResponse | split: 3:'LEFT'"
  role="group"
  attr.aria-label="{{ translations.labels.topics }}"
>
```


#### Expand/Collapse
The expand/collapse functionality is intended to display or conceal subtopics. When the user clicks the "+" icon, it reveals all subtopics under that topic. Clicking the "-" icon will hide these subtopics. Additionally, if a user opens a new topic by clicking the "+" icon while another is open, the application will automatically close the currently open topic and display the newly selected one.
  
### Here is list of systems involved to make the list possible

Content
  1. GCS - This is the place where the Tax taxonomy (Topics and Subtopics) are created.
  2. TIGRE/Opus - Once the Tax Taxonomy is created and published, the information is extracted from GCS side and store it in TIGRE.  The database for storing this information is called CPTOPICS
  3. DTD - A new DTD is required for TIGRE to store the XML document.
  
CPS
  1. Extract - CPS will extract the package CPTOPICS from TIGRE/OPUS for processing
  2. Processing - CPS processes the extracted package and load it to NOVUS for web-app to use.

NOVUS
  1. Easel - https://easel-client.1667.aws-int.thomsonreuters.com/easel
  2. GUID - T0CPTPTopicsAndSubtopicsData
### Topic and Subtopics are ordered by GCS
The arrangement of topics and subtopics is set by the GCS. The Checkpoint web app simply displays them in the order they are received.

![image.png](/.attachments/image-c7bbd76c-b147-4449-951b-94b9e3c6417e.png)
