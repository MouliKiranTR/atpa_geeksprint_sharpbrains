1. Description

>- Service that provides contextual summaries, charts, and enriched content for user searches, enhancing the presentation of results in the web application

2. Repository Link

>- [cp_snapshots-service](https://github.com/tr/cp_snapshots-service)

3. Libraries

4. Testing

>- [Swagger Links](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/1175/Swagger-links)

4.1 Automated and Functional Testing

*   **Exhaustive functional tests** were conducted after upgrading AWS dependencies (SDK 2.31.28, Kinesis, and Comprehend) to ensure:
    *   Correct functioning of snapshots (Overview, Related Tools)
    *   Correct rendering and behavior of charts in different modalities (State, Nexus Assistant, BNA State Tax Survey)
*   **Regression testing** is recommended for any application that consumes this service.

4.2 Observability and Logs

*   During testing, logs in **Datadog** confirmed the system’s expected behavior, including the automatic restart of Kinesis subscriptions (which does not impact end-user functionality).
*   For further analysis, use **Datadog Log Explorer**.

4.3 Manual & UI Testing

*   **UI Validation:**  
    we have 2 big parts in it - elasticsearch related and kinesis related. for kinesis we have to use html publisher. afaik it doesn`t work on ci so I asked qa team to verify it in qed. 

# for es I have several requests to test parts I need 

POST https://cp-dev-cp-snapshots-service.tr-tax-cp-preprod.aws-int.thomsonreuters.com/api/v1/snapshots?searchTerms=tax&practiceArea=1&maxResults=1
 Authorization: Bearer <token> Content-Type: application/json 
{ "additionalProp1": {}, "additionalProp2": {}, "additionalProp3": {} } 

POST http://localhost:9111/api/v1/snapshots?searchTerms=Can%20an%20accounting%20firm%20be%20engaged%20in%20compilation%20of%20the%20same%20set%20of%20financial%20statements?&practiceArea=7&lastCpReqId=153c9&cmpType=MAIN Authorization: Bearer <> content-type: application/json { "taxTypes": [] }

    Siarhei Barysiuk recommended deploying to the CI environment, then accessing [Checkpoint CI](https://checkpoint.ci.thomsonreuters.com/).  
    For example, searching for "kiddie tax" should display the snapshots frame in the UI.
![image.png](/.attachments/image-075af676-0024-4dd8-a733-0e0c583728cb.png)
![image (1).png](/.attachments/image%20(1)-f1c4ab8b-7b5f-4a09-88e8-bd33a847482d.png)

# for kinesis we have to use html publisher. afaik it doesn`t work on ci so I asked qa team to verify it in qed. 

*   For detailed testing instructions, **Flores Jefte (TR Technology)** provided Some guidance and step-by-step instructions. screenshots are provided below:
![Jefte 1.png](/.attachments/Jefte%201-36880f4a-bdd4-4f16-b08e-9ba96b14b297.png)
![Jefte 2.png](/.attachments/Jefte%202-6be7e1f4-a14a-4aef-837f-b89d98487bf3.png)![Jefte 4.png](/.attachments/Jefte%204-51bae283-d4d1-4537-b069-c2e5426c843e.png)

# This is the repository, you can search here for all Rajiv's queries:
[https://github.com/tr/cp_web-app/commits/main/etc/StoredProcs](https://github.com/tr/cp_web-app/commits/main/etc/StoredProcs "https://github.com/tr/cp_web-app/commits/main/etc/storedprocs")


5. Diagrams

>- [Architectural Diagram](https://lucid.app/lucidchart/9aeb4fc0-5c66-4039-b206-824c0a6d6ddd/edit?invitationId=inv_cd8a8f63-048d-47f2-a008-652ebb79f5ef&page=dpu9VFO5GJQf#)