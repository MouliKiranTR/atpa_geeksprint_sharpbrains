[[_TOC_]] 

## **Overview**
TRTA Search is one of the core components that facilitates to perform the intuitive Search in Checkpoint. It was developed to provide meta data supported search results.  The service layers on top of Novus and leverages Rocks DB objects and additional Novus search data to score and rank documents based on an R&D search algorithm. The major components are as follows.

- **Checkpoint** – Checkpoint has a class called CPCobaltSearchService which is the main entry point for requests to the TRTA Cobalt Search Service.
- **Core Search** – Core search is the backbone of the search service.  It delegates requests to TRTA search but is responsible for all interactions with data sources and persistence mechanisms.
- **TRTA Search** – The Checkpoint team manages the TRTA Search code base.  We facilitate the Checkpoint specific algorithm application and interact with Core search to execute the searches, load the Rocks DB data, score and sort the response and return the ordered list of document guids.
- **Novus** – The search engine for documents.
- **Rocks DB** – is a high-performance, embeddable key-value store for last storage environments. It is developed by Facebook. It is a fork of Google’s LevelDB, optimized to exploit multi-core processors and make efficient use of fast storage like solid-state drive. 
- **Berkeley DB Objects (replaced by Rocks DB)** – These are simply .db files that are stored locally on a fusion IO card. The .db files contain (effectively) serialized classes of document metadata.
- **Coherence** – This is the caching component of the application.  Core search caches the search results to Coherence after the search is completed.  When Checkpoint clears its cache and the user requests the same search again, a retrieve request is executed, and Core search will look up the search result from the Coherence cache using a passed search handle. 

## **Data Flow**
Here is the high-level data flow diagram of TRTA Search components. Please note, that the diagram needs to be updated to replace the Berkeley DB-specific information using Rocks DB. Also, since we moved to the cloud environment, requests are not passing through Big IP network anymore.

![trta-search-data-flow.png](/.attachments/trta-search-data-flow-6e627cde-0c19-4d1d-9637-afa246e20ff2.png)

From a high level, a request is made from Checkpoint to what has commonly been referred to as the Cobalt search service. The request is processed within the Core Search and Core Search delegates the request to TRTA Search where TRTA Search does the following operations:

- Formulates the Checkpoint request into a TRTASearchRequestState object.
- Executes a Natural Language and Terms and Connectors search (via Core Search to Novus) to obtain a list of candidate documents.
- Executes an extended Natural Language Novus search to pick up other important documents to build out a list of “Source of Truth” documents.
- Executes several other searches for metadata and possible citation search candidate documents.
- Loads the Rocks Java objects for the candidate and source documents.
- Executes the features to calculate scores for each document by the algorithm type.
- Executes some Checkpoint logic for the exclusion and inclusion of additional documents.
- Passes off the results to be sorted and scored.

After that Core Search takes the results of the TRTA delegation which is a list of documents along with some additional metadata and returns it to Checkpoint in a JSON format. Core Search additionally persists this information to Novus and Coherence. Checkpoint parses the response and builds out search results.

## **Project Structure**
The TRTA Search project builds upon the base provided by the CoreSearch project. CoreSearch is owned by (as we have referred to them) the Core Search team.

The entire TRTA Search project is driven by the SPEAD framework. This framework provides a simple rules-based approach with annotations taking the place of rules. The framework handles the overall threading activities and provides the overall flow. At its base, the SPEAD framework operates off the activities that is required by the activities from other products. The wiring is provided by the following annotations:

`@Needs(Some String) – Translated as I need the output of some other activity whose product is identified by (Some String)`
`@Produces(Some String) – Translated as I produce a product that is identified by (Some String)`

Here is a simple example:

`…`
`public class SourceDocAgentSpeadActivity implements Callable<SourceDocPool<Integer, SessionCPSDocumentMetadata>>`
`…`
`public static final String RESULT = "SourceDocAgentSpeadActivity";`
`…`
    `@Needs(TRTASearchRequestStateSpeadActivity.RESULT)`
    `private TRTASearchRequestState trtaSearchRequestState;`
`…`
    `@Produces(SourceDocAgentSpeadActivity.RESULT)`
    `@Override`
    `public SourceDocPool<Integer, SessionCPSDocumentMetadata> call()`
    `{`
      `}`

In the above example, `SourceDocAgentSpeadActivity` produces a `SourceDocPool` identified by the String key of `SourceDocAgentSpeadActivity` and needs a `TRTASearchRequestState` object.   The `TRTASearchRequestState` when available is automatically populated and the `call()` method is invoked.  Any other activities that require the `SourceDocAgentSpeadActivity` result are simply blocked until it is available.

## **Data Flow**

![data-flow-trta-search-request.png](/.attachments/data-flow-trta-search-request-cbe58294-9e13-472c-b8a3-b5c8ca10e3f0.png)

- The core search framework processes requests.
- It identifies what type of request is being made and starts a SPEAD task branch to handle it.
- It produces a `SearchRequest` object.
- The search request object is the entry point for TRTASearch.  It is processed by `TRTASearchRequestStateSpeadActivity`. 
- This activity is needed by most other activities including the primary Novus search requests.
- The Novus search requests execute and produce their results.
- The `ProcessNovusSearchResultsSpeadActivity` uses the results of the Novus searches to retrieve the document metadata Rocks DB objects.
- This group of resulting objects is passed on to the candidate and source pool generators as well as the activities responsible for loading the other metadata (to, from ,and user action).
- This data is in turn used by the feature activities that are responsible for generating feature values for each of the candidate documents.
- The results are fed into the score and rank activities that apply weights to the features, total the sum value for the documents, and sort the result.
- This is in turn fed into the generated search result list activities.

## **TRTA Search API Integration in Checkpoint**
Checkpoint interacts with the TRTA Cobalt search service via an Https interaction and use it to perform intuitive search.  It leverages the existing CPHttpClient class to invoke the search given a Json request and response for the following transactions:

- **Search** – The replacement for a Novus search.
- **Retrieve** – Retrieval of the already executed search.
- **Document Recommendations** – Retrieval of document recommendations for given document guids.
- **Document Metadata** – Retrieval of metadata about the document for given document guids.
- **Termination/Cleanup** – On termination of a user’s session a cleanup request is sent to allow for the release of Novus and Coherence information.

Checkpoint search requests are executed given an algorithm type. The algorithm type is defined in the appTabsEdge.xml and appTabsMain.xml file.  Example:  `<property id="cobaltAlgorithm" value="federal"/>`. Also, Checkpoint application makes two TRTA Search API call to execute the search request and to display the results to the Search Results page:

- TRTA [SearchResult](https://trtacheckpointus-ci-use1.8101.aws-int.thomsonreuters.com/CheckpointUSSearch/v1/search/fermi/TRTAFermiSearch/SearchResult) endpoint to retrieve the reranked docGuids and
- TRTA [Search](https://trtacheckpointus-ci-use1.8101.aws-int.thomsonreuters.com/CheckpointUSSearch/v1/search) endpoint to retrieve the metadata of the returned docGuids from SearchResult endpoint.

Also, here is a high-level diagram that shows the execution flow of the Checkpoint Intuitive search.

![intuitive-search-execution-flow.png](/.attachments/intuitive-search-execution-flow-097b4169-7f3c-4fb4-8360-dd39104f1b3b.png)
  

## CMDB Properties
- CI: https://infratools-chkpnt-ci-use1.8101.aws-int.thomsonreuters.com/cmdb/verticals/attributes?targetName=CheckpointUSSearch
- DEMO: https://infratools-chkpnt-demo-use1.8101.aws-int.thomsonreuters.com/cmdb/verticals/attributes?targetName=CheckpointUSSearch
- QED: https://infratools-chkpnt-qed-use1.04032.aws-int.thomsonreuters.com/cmdb/verticals
- PROD: https://infratools-chkpnt-prod-use1.04032.aws-int.thomsonreuters.com/cmdb/verticals

## Important Contacts
Here are the contact points for the TRTA Search CI, DEMO, QED, and PROD environments.

- Platform CM (Thomson-PlatformGrpCM-Cobalt@Thomsonreuters.com) for the CI and DB environments of the TRTA application and
- Cobalt Services Support team ([thomson-cobalt-services-support@thomsonreuters.com](mailto:thomson-cobalt-services-support@thomsonreuters.com)) for the TRTA QED and PROD environments.


## Diagrams
- TRTA Search - [TRTA Search: Lucidchart](https://lucid.app/lucidchart/c7a3b8fa-77c5-46b7-ba22-0834e5dd33d8/edit?invitationId=inv_03c8e2e7-01f3-4564-ad1a-c29b46af2c21&page=l.WLRmX2WcoK#)
- TRTASearch Code Logic - [TRTASearch Code Logic: Lucidchart](https://lucid.app/lucidchart/88db4f21-accc-4824-8757-64ec5cc21fc2/edit?page=YGcM5DNywbTK&invitationId=inv_21879bbd-276f-4c62-85ff-4153fee78141#)

## Resources
- **TRTA Cobalt Search Service** - [Overview-Cobalt-TRTA-Search.docx](https://trten.sharepoint.com/:w:/r/sites/TRTAKSCheckpointAnswers/_layouts/15/Doc.aspx?sourcedoc=%7B77E752F7-7FCD-4738-AA1B-A64AD896CF13%7D&file=Overview-Cobalt-TRTA-Search.docx&action=default&mobileredirect=true)
- **NL:** [Natural Language Search.doc](/.attachments/Natural%20Language%20Search-1ecf319a-6b0a-4306-a4cd-1504d188225e.doc)
- **TNC:** [Boolean Search Quick Reference.docx](/.attachments/Boolean%20Search%20Quick%20Reference-27b80275-0885-48a1-955c-9c403432ef59.docx)