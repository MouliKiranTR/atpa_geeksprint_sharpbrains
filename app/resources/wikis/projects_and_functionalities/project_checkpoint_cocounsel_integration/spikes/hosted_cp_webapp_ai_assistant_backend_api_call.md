[User Story 167417](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_workitems/edit/167417): [FedTax Q&R] Spike - Defining the Inputs to the Hosted CP WebApp AI Assistant Backend API Call

___
*Author:* @<DE58388A-475B-68F7-A222-1DD0000B6525> 
[[_TOC_]]

___

## CoCounsel Skill Server API Endpoints
### Resources/References
- [AI Assistant Skill Integration Guide](https://github.com/tr/ai-assistant-doc/blob/update-skills-section/02_integration_guide/skills.md#skill-servers)
- [Developer Portal- CARI Skill API's](https://developerportal.thomsonreuters.com/node/18247)
- [Example skill server](https://github.com/tr/coco-skill-server-example)

### Skill Servers
- Skill Server is consumed by the AI Assistant in CoCounsel (CoCounsel AI Assistant is client of Skill server)
- Skill servers must implement the following routes:
	- `POST /skill-name`
	- `GET /flows/{id}/status`
	- `GET /flows/{id}`
- So far, two sets of REST API's in Developer Portal for CARI Skill API's:
	- AI Assisted Legal Research (AALR for Westlaw)
	- Ask Practical Law (AskPL)

#### 1. POST `/skill-name/v1/conversation`
**Request**\
Initiates a conversation
```json
{
  "query": "What is a law in Minnesota?"
}
```
**Response**\
The response must follow this schema.
```json
{
  "conversationId": "563a0b67-c30e-4a5b-b1c3-1731a51fb03c",
  "conversationEntryId": "a12db243-67e8-4729-ac6c-27bd27fbae9e"
}
```

#### 2. GET `skill-name/v1/flows/{id}/status`
**Input Parameters**
- (PATH) `id` - *required*, GUID identifying the conversation
- (QUERY) `entry_id` - *optional*, specifies the entry of the conversation to return. If left blank, show status of whole conversation

**Request**
Retrieves minimal status information about a conversation or conversation entry

**Response**
The response must follow this schema.
```json
{
  "id": "7d49a054-2254-4a44-b386-accd6b689b8a",
  "status": "PROCESSING", // INITIALIZED, PROCESSING, FAILED, or COMPLETE
  "progress": 0.6, // float between 0.0 and 1.0 representing skill progress
  "flow_type": "skill_name" // skill identifier
}
```

#### 3. GET `/skill-name/v1/flows/{id}`
**Input Parameters**
- (PATH) `id` - *required*, GUID identifying the conversation
- (QUERY) `entry_id` - *optional*, specifies the entry of the conversation to return. If left blank, show status of whole conversation

**Request**
Retrieves information about a conversation or conversation entry. Also used for polling status.

**Response**
```json
{
  "id": "7d49a054-2254-4a44-b386-accd6b689b8a",
  "type": "skill_name",
  "input": { // the skill request JSON payload
    "query": "What is law?",
    "jurisdictions": [
      "ALLCASES"
    ]
  },
  "output": { // the skill response JSON payload
    "progress": "RUNNING",
    "errorResponse": null,
    "qaPair": null,
    "rasConversationId": "4e1ddc26-dcd7-4350-a5cc-f60c4383de40"
  },
  "status": "SUCCESS",
  "progress": 1.0,
  "chat_id": "4a90c930-40cf-4858-ad2d-71df738e3b0a",
  "chat_summary": "Skill name results:\nInput: Hello world.\nOutput: Copy that, message received." // skill results, rendered as a string or array of strings, for AI assistant to include in chat history
}
```


## Checkpoint AI Assistant Endpoints
### Resources/References
- [Swagger UI for AI Assistant Controller](https://checkpoint.ci.thomsonreuters.com/app/api/swagger-ui.html#/AI_Assistant_Controller)

### V4 endpoints
- Will be cleaned up and removed soon
- Offers conversation history endpoint to retrieve entire conversation (not available in V5 endpoints but can provide reference of how to implement this functionality)

### V5 endpoints
#### 1. POST `/aiAssistant/v5/conversation/start`
**Request**
Start a new conversation with the AI Assistant.

**Response**
```json
{
  "jurisdictions": [
    "NY",
    "CA"
  ],
  "practiceArea": "federal",
  "userQuery": "Tax question?"
}
```

#### 2. PUT `/aiAssistant/v5/conversation/{conversationId}/continue`
**Input Parameters**
- `conversationId` - *required*, GUID of the conversation

**Request**
Continue an ongoing conversation with the AI Assistant.
```json
{
  "jurisdictions": [
    "NY",
    "CA"
  ],
  "practiceArea": "federal",
  "userQuery": "Tax question?"
}
```

#### 3. GET `/aiAssistant/v5/conversation/{conversationId}`
**Input Parameters**
- (PATH) `conversationId` - *required*, GUID for the conversation
- (PATH) `conversationEntryId` - *required*, GUID for a specific conversation entry

**Request**
Retrieve a conversation entry using its unique conversation ID and conversation entry ID.


## Connecting Checkpoint to CoCounsel Skill Server
- Endpoints needed for CoCounsel:
	- Initiate a conversation - POST `/skill-name/v1/conversation`
		- The existing POST `/aiAssistant/v5/conversation/start` endpoint will support this functionality
	- Retrieve status about a conversation or conversation entry- GET `skill-name/v1/flows/{id}/status`
		- There is no endpoint in CP that currently retrieves just the status and this will need to be added
	- Retrieve conversation entries- GET `/skill-name/v1/flows/{id}`
		- The existing GET `/aiAssistant/v5/conversation/{conversationId}/{conversationEntryId}` will support most of this functionality
		- However, the current CP endpoint does not return any status information
		- The current CP endpoint also does not support retrieving the whole conversation as the conversation entry ID is required and you can only retrieve a specific entry
			- *Note:* this was previously supported in the `/aiAssistant/v4/conversation/{conversationId}` endpoint used to retrieve a conversations history
			- However, it was removed in V5 and the old V4 endpoints will be removed/cleaned-up soon
			- The old implementation may provide reference to how this can be done
- RAS supports percentage complete, but not currently implemented. Need to add this, further discussion with Ravi required

### Next Steps & Stories Required
- Discuss with Ravi about adding support in RAS for percentage complete
	- Determine if we need a story for this and what team will implement this
- ***Story #1:*** Create endpoint to retrieve information about an entire conversation or specific conversation entry in addition to polling status in CP WebApp
	- This endpoint will support the `/v1/flows/{id}` endpoint in the Skill server
	- This endpoint will in the backend operate the same as the `/aiAssistant/v5/conversation/{conversationId}/{conversationEntryId}` endpoint in CP WebApp
	- However, it will need to add support for retrieving the entire conversation if only a conversation ID is provided (new functionality) in addition to a specific conversation entry if the entry ID is provided.
- ***Story #2:*** Create endpoint top retrieve status information about an entire conversation or specific conversation entry
	- This endpoint will support the `v1/flows/{id}` endpoint in the Skill server
	- This endpoint will provide the status and progress of a conversation and will require new functionality in CP WebApp