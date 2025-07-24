 [User Story 168639](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_workitems/edit/168639): [Discovery] SPIKE - Update CP GAIL to Pass Back Percent Complete

*Author:* @<DE58388A-475B-68F7-A222-1DD0000B6525> 
[[_TOC_]]

___

## References and Resources
- [Atrium: AALP - Search](https://trten.sharepoint.com/sites/CaRSOperations/SitePages/RAS/AALP%20Search.aspx)
- Lucid chart: [CP Gen AI Demo](https://lucid.app/lucidchart/1a3f7bbf-d46d-4322-9c17-2e211bd44ce4/edit?invitationId=inv_492f8c33-5f9c-4a9f-b801-ebfcddc399d5&page=9R-7exwcr6h5#)
- Lucid chart: [Checkpoint AI Assisted Research Architecture](https://lucid.app/lucidchart/ab069a25-3b5c-4625-bd32-3a2bae9d6c8e/edit?invitationId=inv_14b42940-c74a-4df1-9215-aeba9cb235c7&page=W9UhVlYBO5fD#)
- [TR Labs Python Documentation](https://python.labs.thomsonreuters.com/introduction/prerequisites/) (used by Python services like GAIL and RAS worker)
- [RAS docs](https://helix.thomsonreuters.com/static-sites/site-builds/ras_documentation/ras-documentation/intro.html)
- [GAIL docs](https://laughing-sniffle-mz6l64o.pages.github.io/index.html)

### Repos
- https://github.com/tr/cp-gail_service - the RESTful API repo for Checkpoint GAIL (Generative AI and LLM), aka CP RAG service
	- Contains all pre and post processing
	- Contains all RAG pipeline definitions
	- Handles communication with LLM and submitting question through the LLM router
- https://github.com/tr/ras-search_ai-rag-checkpoint - RAS worker for Checkpoint US conversational AI
	- Worker that listens for new tasks submitted to the queue
- https://github.com/tr/labs-aalp_service - the RESTful API repo for Westlaw AALP (AI Acceleration for Legal Professionals), the WL equivalent to GAIL service
- https://github.com/tr/ras-search_ai-rag-westlaw - RAS worker for Westlaw conversational AI
- https://github.com/tr/ras-search_ai-rag-westlaw-50-states-survey - RAS worker for Westlaw 50 states survey
- https://github.com/tr/labs-pl-aalp_service - the RESTful API repo for AALP in Practical Law (AI Acceleration for Legal Professionals), the PL equivalent to GAIL service
- https://github.com/tr/ras-search_ai-rag-practical-law - RAS worker for Practical Law conversational AI
- https://github.com/tr/ras_shared-python-utils - shared utilities
	- Includes RAS Shared Conversation Core components shared across different RAS projects processing conversations such as AI conversations and various AI RAG implementations
	- Includes profile definitions

___
## Flow Between RAS Conversation APIs, RAS Worker, and GAIL:
- High level: ![Pasted image 20241030142918.png](/.attachments/Pasted%20image%2020241030142918-ec31f8c2-2d08-45d6-a883-96a6bdb28523.png)
- With details: ![Checkpoint AI Assisted Research Architecture - Luke Scratch.png](/.attachments/Checkpoint%20AI%20Assisted%20Research%20Architecture%20-%20Luke%20Scratch-ae677083-c880-4cd5-a51b-fd11c83995f1.png)
### Initiate Conversation Flow
1. CP UI makes request to CP WebApp backend (`POST /v5/conversation/start`)
1. CP WebApp makes request to RAS conversation APIs with profile (`POST /v2/conversation/{user_id}/entry`)
	1. Profile defines as a CP request
	2. Profile also differentiates state and federal
2. RAS conversation API submits task onto Celery queue based on profile
3. CP RAS Worker listens to celery queue for Checkpoint profile and picks up the task with included task metadata
4. Through library call, it invokes CP GAIL (aka CP RAG service)
	1. Does this by calling into wheel file
5. CP GAIL performs all RAG pipeline actions
	1. Including pre-processing, calling of LLM through LLM proxy, etc.
6. Response is stored in S3 and Dynamo DB
7. Task is marked as complete, and any polling of status by RAS conversation API will return as complete and successful

### Conversation Retrieval Flow
1. CP UI requests a conversation from CP WebApp backend ( `GET /v5/conversation/{conversation_id}/{conversationEntryId}`)
1. CP WebApp polls the conversation endpoint which returns task metadata from S3 and Dynamo DB ( `GET /v2/conversation/{user_id}/{conversation_id}/{conversation_entry_id}`)
2. Once task is marked as complete and successful, it returns to CP UI and stops polling

### Calls from RAS Worker to GAIL
- In the `conversation_service_impl.py` of the RAS Worker (`ras-search_ai-rag-checkpoint`) there are imports from `ai_assistant.v2` which is the package for GAIL service (`cp-gail_service`)
- The `generate_answer` method of the `RAGRelatedServiceLG` class inside CP GAIL is then called: 
	```Python
	tasks = [RAGRelatedServiceLG.generate_answer(rag_service_input, rag_settings)]
	```
- This is the main method call to kick off the RAG pipeline, but there are other usages/imports of the GAIL project as well
- ***Note:*** there are 4 uses of `generate_answer` in the `conversation_service_impl.py` class of RAS worker (these are the only usages in the whole project):
  - `tasks = [RAGRelatedServiceLG.generate_answer(rag_service_input, rag_settings, related_resource_settings)]`
    - Triggers answer generation flow
    - Latest version, **must be updated for percent complete**
  - `tasks = [RAGService.generate_answer(rag_service_input, rag_settings)]`
    - Triggers answer generation flow
    - Will be removed in 24.12 release, so does not need to be updated for percent complete
  - `RelatedResourcesService.generate_answer(irc_service_input, irc_settings)`
    - Used to generate supporting material that's related to query
    - Does not need to be updated for percent complete
  - `RelatedResourcesService.generate_answer(tpac_service_input, tpac_settings)`
    - Used to generate supporting material that's related to query
    - Does not need to be updated for percent complete

___
## Changes required in GAIL service
- When making changes to GAIL service we have permissions to create a PR, but before making any changes inform Ravi and labs team (Jesse Roland) so they are aware of the planned modifications
	- This ensures the changes do not conflict or affect any of the work they are doing
	- Changes should also be backwards compatible

### Determining Percent Complete
- To determine % complete we need to base it off the stage of the RAG pipeline we are at
- The RAG pipelines are defined in `src/ai_assistant/v2/pipelines/definitions/rag/ci-rag-pipelines.yml`
- The file contains definitions of various components
	- These components are just Python classes elsewhere in the codebase
	- For example:
		```yaml
		- name: RelatedClassifierLLMInput-V2
		    fq_class_name: ai_assistant.v2.components.transformers.llm_requests.query_llm_input.QueryLLMInput
		    params:
		      prompt_id: "RELATED_CLASSIFIER_PROMPT_V2"
		      llm_model: "anthropic.claude-3-5-sonnet-20240620-v1:0"
		      max_response_token: 256
		      request_type: "related_classifier"
		```
- Then, these components are referenced in the RAG pipeline definition
	- There are various components and their inputs laid out
	- Some are grouped logically
	- For example:
		```yaml
		- component: RASNovusSearchRequest-doc-State
			inputs: [ IntentFilter, UserInputPreprocessor-State ]
		- component: RASNovusSearchRequest-docp-State
			inputs: [ IntentFilter, UserInputPreprocessor-State ]
		- component: OpenSearchGenericQuery-ANN-State
			inputs: [ IntentFilter, QueryVectorMapper ]
		- component: OpenSearchGenericQuery-keyword-State
			inputs: [ IntentFilter, UserInputPreprocessor-State ]
		# Execute Discovery Phase
		- group: discovery
			concurrency: coroutine
			nodes:
				- component: OpenSearchRetriever-ANN
					inputs: [ OpenSearchGenericQuery-ANN-State ]
				- component: OpenSearchRetriever-keyword
					inputs: [ OpenSearchGenericQuery-keyword-State ]
				- component: CheckpointSearch
					inputs: [ CheckpointSearchRequest-State ]
				- component: RASNovusRetriever-doc
					inputs: [ RASNovusSearchRequest-doc-State ]
				- component: RASNovusRetriever-docp
					inputs: [ RASNovusSearchRequest-docp-State ]
		- group: opensearch-pooling
			concurrency: coroutine
			nodes:
				- component: OpenSearchDocumentPooler-ann
					inputs: [ OpenSearchRetriever-ANN ]
				- component: OpenSearchDocumentPooler-keyword
					inputs: [ OpenSearchRetriever-keyword ]
		```
- For each component step, or for each logical chunk of components we need to update the percent complete
	- Need to determine what % complete to update after each step
	- Need to determine what steps or groups of steps to update % complete at
	- Component should update the percent complete using utility class

### Task Metadata
- Currently, GAIL is not supplied the task metadata
	- In `RAGRelatedServiceLG` class of GAIL service (located at `src/ai_assistant/v2/langgraph/services/services.py`), there is method `generate_answer` which is used to execute the RAG pipeline
	- Method definition: 
		```Python
	        async def generate_answer(cls, service_input: RAGServiceInput, rag_settings: RAGSettings, related_resources_settings: RelatedResourcesSettings) -> RAGRelatedServiceOutput:
		```
	- Takes in `RAGServiceInput` instance which contains input data such as query, conversation, practice area, sources, and state
	- Takes in `RAGSettings` instance which contains pipeline file, citation type, and other settings for the LLM
- When this method `generate_answer` is called from the RAS worker we need to pass the worker task in as well
	- `WorkerTask` is a class imported from `conversation_core.shared.worker.worker_task`
	- Conversation core package is from `ras_shared-python-utils` project
	- `WorkerTask` is a class that manages and updates the state and metadata of a Celery task
- Task object holds metadata of running task (CP RAG request creates task with metadata, percentage complete information would be part of the task metadata object)

### RAS Shared Conversation Core
- Repo: https://github.com/tr/ras_shared-python-utils/tree/main/conversation-core 
- Contains class `WorkerTask` which manages and updates the state/metadata of a Celery task
- Class has method [`worker_task.update_task_status_in_progress`](https://github.com/tr/ras_shared-python-utils/blob/cae1d42189574d5fabadc9f798946bcc87a31ed9/conversation-core/conversation_core/shared/worker/worker_task.py#L43) which is used to update percent complete

___
## Changes Needed in RAS Worker
- See [RAS Search AI RAG Template](https://helix.thomsonreuters.com/static-sites/site-builds/ras_documentation/ras-documentation/09_rag_workers_template/generic_functional.html) documentation for more info on the RAS worker structure and design
- RAS worker needs to be updated to consume the new version of CP GAIL service once the changes are made there to update the method signature of `generate_answer` is updated to support passing `WorkerTask` object in
- Method call to `generate_answer` must also be updated to pass in the `WorkerTask` to CP GAIL for it to update the percent complete
- Since the percent complete is already contained in task metadata and initialized to 0, there should be no other changes required besides passing it to GAIL and having it update the percentage at various points in the pipeline

___
## RAG Pipeline
- Lucid chart of RAG pipeline: https://lucid.app/lucidchart/1a3f7bbf-d46d-4322-9c17-2e211bd44ce4/edit?invitationId=inv_492f8c33-5f9c-4a9f-b801-ebfcddc399d5&page=.O-7zwurOpIZ#
- Updated architecture from GAIL docs: https://laughing-sniffle-mz6l64o.pages.github.io/architecture.html
- Pipeline definitions: https://github.com/tr/cp-gail_service/tree/development/src/ai_assistant/v2/pipelines/definitions/rag
- High-level (from Lucid): ![Pasted image 20241029151118.png](/.attachments/Pasted%20image%2020241029151118-0644de1b-2777-4598-9a68-2181e7413885.png)
- Detailed (from GAIL docs): ![image.png](/.attachments/image-8309cab2-3c68-47e7-a73a-4f65b99132e2.png)
- Detailed ([outdated after lang graph transition](https://laughing-sniffle-mz6l64o.pages.github.io/architecture.html#lang-graph-transition)): ![Checkpoint AI Assisted Research Architecture - Copy of Luke Scratch.png](/.attachments/Checkpoint%20AI%20Assisted%20Research%20Architecture%20-%20Copy%20of%20Luke%20Scratch-ac122a8a-cbca-4a54-8367-d2856ec90921.png)

### Overview of Steps, Phases, and Components
1. **Input Processing:**
	- The pipeline receives a user query and validates it (`InputValidator`).
	- It preprocesses the query, identifying user intent (`UserInputPreprocessor`, `UserInputPreprocessor-intent`, `UserInputPreprocessor-State`).
	- For conversational pipelines, the query may be reformulated or summarized based on previous interactions (`QueryReformulationLLMInput`, `ConversationSummaryLLMInput`, `ConversationSummaryLLMExecutor`, `QueryReformulationLLMExecutor`).
	- Based on the identified intent, irrelevant information may be filtered out (`IntentFilter`, `IntentFilter-FedFilter`).
2. **Content Retrieval (Discovery Phase):**
	- The query is used to search various knowledge sources concurrently for potentially relevant information:
	    - **OpenSearch:** Searches an index of passages using both keyword-based and ANN (Approximate Nearest Neighbor) search (`OpenSearchGenericQuery-keyword`, `OpenSearchGenericQuery-ANN`, `OpenSearchRetriever-keyword`, `OpenSearchRetriever-ANN`, `OpenSearchDocumentPooler-keyword`, `OpenSearchDocumentPooler-ann`).
	    - **Checkpoint:** Searches the CP knowledge base through external search APIs (`CheckpointSearchRequest`, `CheckpointSearch`).
	    - **RAS Novus:** Performs Novus search (`RASNovusSearchRequest-doc`, `RASNovusSearchRequest-docp`, `RASNovusRetriever-doc`, `RASNovusRetriever-docp`).
	- For state-specific pipelines, dedicated components are used to target state-level content (`...State`).
	- This phase retrieves a set of candidate passages/documents.
3. **Candidate Ranking and Selection:**
	- The retrieved passages are often further filtered and ranked based on their relevance to the query:
	    - `GUIDExtractor` identifies unique identifiers of potentially relevant passages.
	    - `OpenSearchGUIDQuery` retrieves the full content of these passages.
	    - `SelectionFilter`, `SelectionFilter-State` filter out any irrelevant passages.
	    - MiniLM model assigns scores to the passages, and `MiniLMScoreMapper` uses these scores for ranking.
	    - `PassageReranker-GDP`, `PassageReranker-OnlySort` reorder the passages based on factors like relevance and importance (GDP - General Document Promotion).
4. **Answer Generation:**
	- The top-ranked passages are assembled into a context (`ScoredOpenSearchLLMInputFormatter`).
	- This context, along with the initial query, is fed to a large language model (LLM) to generate a summarized answer (`SummaryGeneratorInput`, `SummaryGeneratorInput-Followup`, `LLMExecutor`).
5. **Response Post-processing:**
	- The LLM's response is further processed:
	    - `LLMSummaryExtractor`, `LLMSummaryExtractor-Keep-Citations` extracts the summary while managing citations.
	    - `MarkdownFormatterLLMInput`, `MarkdownFormatterLLMInput-V2`, `MarkdownFormatterLLMExecutor` formats the response into Markdown.
	    - `CitationInserter` adds citations from the retrieved passages.
	    - `CitationExtractor` extracts citations for further processing in some pipelines.
	    - `LLMMultiExecutor`, `LLMCitationCompiler` might be used for more complex citation processing.
	- Finally, `AnswerPostProcessor` refines the answer, and the `Result` component delivers the final output to the user.

### High-level Phases
1. **Input validation and pre-processing**
	1. Query validation
	2. Practice area and RAG pipeline validation
	3. Query reformulation & conversation summarizer
	4. Intent classification (Tax/No-tax, type, topic classifiers)
	5. Input preprocessor & discovery filter (user input processing/parsing, selection of Checkpoint sources, intent filter based on classifier results and practice area)
2. **Discovery**
	1. Content retrieval
		1. Checkpoint search via external APIs
		2. OpenSearch query
		3. Novus Search
		4. GUID extractor
	2. Content selection & filter
	3. Ranker (Passage ranking)
	4. Document assembly & context builder
		1. query generation
		2. LLM input formatter of ranked passages
4. **Answer generation**
	1. LLM executor
	2. Summary extractor
5. **Answer/Response post-processing**
	1. Markdown formatter
	2. Citation extraction and resolution
	3. Result


### Updating Percent Complete
- Below is diagram of where the percent complete value in task metadata should be updated
  - ![Checkpoint AI Assisted Research Architecture - RAG Pipeline (1).png](/.attachments/Checkpoint%20AI%20Assisted%20Research%20Architecture%20-%20RAG%20Pipeline%20(1)-bafd9e0a-623b-4e4f-ae71-57148085d776.png)
  - The top section of the diagram is showing the percent complete and description in the task metadata for that phase
  - The middle section is describing the various phases, with a user-friendly description, and rough execution time/percentage relative to overall answer generation
  - The bottom section is showing points at start/exit of a phase where we will update the percent complete and description inside the task metadata
- Since some of the transitions are large (jump from 15%-90%) to improve the user experience we can smooth the percent value between changes in response
- Need to determine if the status description is customer facing, or just for internal logging/tracking. If the description is seen by users, work with UX team to determine proper phrasing

___
## Example Implementation of Percent Complete For Westlaw
- Functionality to include updating percent complete in worker task metadata was completed for the legislation survey RAG pipeline (50 states survey)
- RAS worker: [ras-search_ai-rag-westlaw-50-states-survey](https://github.com/tr/ras-search_ai-rag-westlaw-50-states-survey)
- AALP (Westlaw GAIL equivalent): [labs-aalp_service](https://github.com/tr/labs-aalp_service)
- See details on AALP here: [Atrium: AALP - Search](https://trten.sharepoint.com/sites/CaRSOperations/SitePages/RAS/AALP%20Search.aspx)
- Story: [User Story 1910117](https://dev.azure.com/TR-Legal-Cobalt/Legal%20Cobalt%20Backlog/_workitems/edit/1910117): Labs: Option to batch jurisdictions that run in parallel
	- PR: https://github.com/tr/labs-aalp_service/pull/1027
- Story: [User Story 2047735](https://dev.azure.com/TR-Legal-Cobalt/Legal%20Cobalt%20Backlog/_workitems/edit/2047735): Rolling Batch Processing for Legislation Survey Pipeline
	- PR: https://github.com/tr/labs-aalp_service/pull/1264
- In their implementation they updated percent complete progress at the following events:
	- Before starting the pipeline execution
	- After pipeline components are executed for a batch
	- After the generated answers are aggregated
- They also updated based on the ratio of completed jurisdictions compared to total jurisdictions, and then cap it at a set percentage for that stage since there are other stages after

### Flow
- Worker `ras-search_ai-rag-westlaw-50-states-survey` is activates by a task
- `generate_answer` method in the `conversation_service.py` class is called
	- It first updates the worker task with percent complete as 1% indicating the task started running: 
		```Python
		worker_task.update_task_status_in_progress(percent_complete=1, status_desc="Legislation Survey task running")
		```
- It calls `LegislationSurveyService` in AALP service (imports `aalp_service.v2.legislation_survey.service`)
	- https://github.com/tr/ras-search_ai-rag-westlaw-50-states-survey/blob/1073830980a6d65748ee75e4a9a6fb6552fe842b/app/services/conversation_service.py#L190
		```Python
		generate_answer_task = loop.create_task(
			LegislationSurveyService.generate_answer(
				profile=answer_profile.rag_solution,
				settings=aalp_config,
				question=user_input,
				fermi_jurisdictions=jurisdictions,
				conversation_history=conversation_history,
				mock_open_ai_data=mock_open_ai_data,
				worker_task=worker_task
			)
		)
		```
	- Passes in profile, settings, question, jurisdictions, conversation history, AI data, and the worker task
- Then, inside the AALP service, at various points in the pipeline, the percent complete is calculated
	- There is then a method `update_task_status` to update the task status which takes `percent_complete` as argument. This method simply calls `update_task_status_in_progress` method of the `WorkerTask` object (mentioned above in [RAS Shared Conversation Core section](#ras-shared-conversation-core) to update the percent complete in the actual worker task
	- All usages: https://github.com/search?q=repo%3Atr%2Flabs-aalp_service%20update_task_status&type=code
	- Points where percent complete is updated:
		1. When generate answer is called, it is set to 1% to indicate the pipeline is being started
		2. As each jurisdiction is being processed, it updates the percent complete to be the ratio of jurisdictions completes to total jurisdictions capped at a certain percent to represent that portion of the pipeline
		3. When pipeline returns it updates to 100% to indicate the output generation is complete
- Once the task returns, the progress is then updated again to 100% indicating the task is complete:
	```Python
	worker_task.update_task_status_in_progress(percent_complete=100, status_desc="Legislation Survey task complete")
	```
- Result is returned

___
## Summary of Changes Required
1. Update CP GAIL to accept `WorkerTask` when initiating RAG pipeline
2. Update CP GAIL to update percent complete in task metadata at logical phases/steps of the RAG pipeline
3. Update RAS worker to use new version of CP GAIL
4. Update RAS worker to pass `WorkerTask` to CP GAIL

### Stories Needed
1. Story for changes in RAS worker
	- [User Story 168638](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_workitems/edit/168638): [Core API] Update CP RAS Worker to Consume New Version of CP GAIL
	- *Needs to be updated to include requirement of passing the task in as well as update version of GAIL*
2. Story for changes in CP GAIL
	1. *Story needed*
	2. Make utility in GAIL service to store and update percent complete