**Overview:**
Logging Interceptor is a component to capture and log specific information such as docGuid, score, and ranking within the TRTA Search process. 

It will be integrated into various classes to ensure that the information is consistently recorded during different stages of the search and ranking process for different practice areas within TRTA Search application.

As a part of this component, we will capture additional logs within Checkpoint WebApp to support the diagnosis process of the search problems too. This will help to diagnosis any Search related problem in the Checkpoint Search space.

Please look at the spike documentation to find detailed information about the Logging Interceptor.

- Overview - Logging Interceptor - [Logging Interceptor - Improve Logging Capabilities in Checkpoint Search Functionally.pptx](https://trten.sharepoint.com/:p:/r/sites/TRTAKSCheckpointAnswers/_layouts/15/Doc.aspx?sourcedoc=%7B820770DF-8185-4154-8BA5-E13F33352797%7D&file=Logging%20Interceptor%20-%20Improve%20Logging%20Capabilities%20in%20Checkpoint%20Search%20Functionally.pptx&action=edit&mobileredirect=true)
- Spike outcome - [Spike_Outcome_Improve_Logging_Capability_in_CP_Search_Functionality.docx](https://trten.sharepoint.com/:w:/r/sites/TRTAKSCheckpointAnswers/_layouts/15/Doc.aspx?sourcedoc=%7B7F936238-6CD6-4126-999B-959A0DF44C23%7D&file=Spike_Outcome_Improve_Logging_Capability_in_CP_Search_Functionality.docx&action=default&mobileredirect=true)

**Implementation:**
Logging Interceptor functionality is controlled by the value of [logging.interceptor.max.execution.time](https://github.com/tr/cp_trta-search/blob/main/resources/CheckpointUSSearchDevelopment.properties#L178) property available in the [CheckpointUSSearchDevelopment.properties](https://github.com/tr/cp_trta-search/blob/main/resources/CheckpointUSSearchDevelopment.properties) file. The value of the property represents the datetime in milliseconds until when the TRTA Search application captures the debug logs with the **SearchIdentifier** keyword in it and sends it to DataDog. Here is the pull request to capture additional debug logs for any Federal practice area specific search - https://github.com/tr/cp_trta-search/pull/77.

![image.png](/.attachments/image-a33cc1ca-0877-4da0-829b-d110fb955127.png)

**Submit CMDB Requests:**
We submit a CMDB request to the Platform CM team whenever we need to capture any additional debug logs from TRTA Search in the CI environment. Here is an example CMDB request - Update CMDB property (logging.interceptor.max.execution.time) value in the TRTA CI Environment - https://dev.azure.com/TR-Legal-Cobalt/Cobalt%20TFS%20Central/_workitems/edit/2121441. Please use the [epochconverter](https://www.epochconverter.com/ ) to get the desired local datetime value for the property. 

![image.png](/.attachments/image-01716331-5900-4bb1-b0dc-7ebca8a491a2.png)

Once you create a CMDB request to update the property value of logging.interceptor.max.execution.time, please email the respective team to execute the request:

- Platform CM ([Thomson-PlatformGrpCM-Cobalt@Thomsonreuters.com](mailto:Thomson-PlatformGrpCM-Cobalt@Thomsonreuters.com)) for the CI and DB environments of the TRTA application and
- Cobalt Services Support team (thomson-cobalt-services-support@thomsonreuters.com) for the TRTA QED and PROD environments.

One of the team members from Platform CM or the Cobalt Services Support team will notify you after the CMDB request is executed successfully.

**Testing & Validation:**
Here are the steps to test out the Logging Interceptor capabilities in any specific TRTA Search environment. Please note, right now the changes are available only in the TRTA Search CI environment.

1. Login to the Checkpoint CI environment and execute a search under the Federal practice area.
2. Use [this DataDog link]([Log Explorer | Datadog](https://tr-contentandresearch-prod.datadoghq.com/logs?query=service%3Acheckpointussearch%20status%3Adebug%20env%3Aci-trtacheckpoint-use1%20%221720022086452_0A87D6B7193D68A8E3B320251121FDF4%22&agg_m=count&agg_m_source=base&agg_t=count&cols=host%2Cservice&fromUser=true&messageDisplay=inline&refresh_mode=sliding&storage=hot&stream_sort=desc&viz=stream&from_ts=1738608391620&to_ts=1738867591620&live=true)) to review the additional debug logs from the TRTA Search application.
3. Please make sure to replace the value of the Search Identifier using the correct one. This will return all the additional debug logs for a specific search identifier.

![image.png](/.attachments/image-9cb62ad2-de11-4d16-863d-bbdc6d759a97.png)

4. The correct Search Identifier can be captured from [this DataDog link](https://trta-cp-prod.datadoghq.com/logs?query=service%3Awebapp%20tr_environment-name%3Aprod%20source%3Asearchinfo%20message%3A%22bad%20debt%22&agg_m=count&agg_m_source=base&agg_t=count&cols=host%2Cservice%2Cname%2Cenv&fromUser=true&messageDisplay=inline&refresh_mode=sliding&storage=hot&stream_sort=desc&viz=stream&from_ts=1732566333213&to_ts=1732569933213&live=true). Please make sure to update the TRTA Search environment to CI and the message to the corresponding search keyword you used to execute a search from the Checkpoint CI environment.

![image.png](/.attachments/image-84ae1852-ecd1-48bd-abcf-11849218bbc5.png)

5. Copy the value of the **identifier** property from the search request, and use it in the filter options of the DataDog link outlined in step 2.

![image.png](/.attachments/image-4786fb34-0c55-4cd8-9c6d-d05c6a66be85.png)








