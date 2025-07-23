Here is [the link](https://trten.sharepoint.com/:b:/r/sites/TRTAKSCheckpointAnswers/Shared%20Documents/General/01%20Projects/Topic%20Pages/Documentations/SPIKE%20-%20Topic%20Pages%20Search.pdf?csf=1&web=1&e=leJlMU) to the SPIKE document for Topic Pages Search functionality in PDF format.

___
# SPIKE - Topic Pages Search
*Author:* @<DE58388A-475B-68F7-A222-1DD0000B6525> 

[[_TOC_]]


## Goal & Objectives
### Background
In topic pages for Federal and State practice areas, each topic pages has a search box.  The search keyword should only target the content related to this current topic pages.

![Pasted image 20240318095557.png](/.attachments/Pasted%20image%2020240318095557-c11d188b-3715-4022-b2c9-fc05212673c6.png)
### SPIKE Objective
The purpose/objective/goal of this SPIKE user story is to document the research and discoveries during the SPIKE.  Understand how the existing Search for template works and how is the search query is constructed in Checkpoint.  How to reuse/reutilize the existing template search in Checkpoint application.  List the dependencies and technology stacks.

## Summary of SPIKE findings
- Completed POC for using the existing template search functionality to execute a TNC (terms & connectors) Novus search restricted to content element tagging, and display the results
	- This approach is already utilized and supported in the code
	- Only requires minimal updates and modifications to allow support for this functionality from the UI through API endpoints
	- Additional discussion needed for exact implementation details (using `combine` endpoint, more generic existing endpoint, or new one entirely)
	- Additional work needed to investigate how to support back to search, history, and auto-complete functionality
	- If we go this route, the elements using for search should be included in the index element set
- Alternatively we could utilize Novus views which would likely provide better search performance but also requires greater effort from content teams, and more configurations in the Checkpoint application
- See [Questions/Considerations](#Questions/Considerations) section for more details on outstanding questions regarding the POC

### Notes/Follow-up After POC Demo Meeting
- Outstanding questions around template searches and POC Demo
	- ***Which type of search to use***- TNC or Intuitive? This is something we would need to run experiments with SME's against the full dataset once it is loaded to determine. If TNC is adequate, this is what was demoed in the POC and would require minimal changes. We could potentially start with this approach to get search working, and then later if through experiments determine that intuitive search would be preferred we can do additional SPIKE and research into that approach.
	- ***Performance***- Novus searches are very performant, and TNC is essentially running a Novus search without much additional overhead so should not be a concern. Need full content loaded in order to test and compare.
	- ***Search Terms autocomplete***- is this functionality required?
	- ***Back to search***- additional investigation needed
	- ***Modifying search terms***- this is currently not working on the POC as well as existing template searches in production. If this is something we need working this will require further investigation and fixes.
	- ***Interactive Tools***- verified this functionality works within the POC: ![Pasted image 20240321135303.png](/.attachments/Pasted%20image%2020240321135303-a85bf412-ac6b-4ab7-bf20-498eea24b5fa.png)
- Outstanding questions and further discussion around Novus views
	- After some people dropped we discussed Novus views more. See [Shared Capability- Novus Views](#shared-capability--novus-views) section for more details
	- If we use views the "Global View Expression" would allow us to apply views through the Novus API at request time, meaning we would *not* need to create individual collection sets for each view expression mapping to a topic, and also would not need to configure any additional data collections in the app.
	- Views for each topic would still need to be created, but these would be applied with the search request
	- Changes would need to be made in web-app to support global view expression
	- Further discussion needed to determine what the benefit of using this approach is, and if it's worth the additional development effort over template searches which are already supported in the app and can be leveraged for topic pages search as shown in the POC.
- Questions for Novus team
	- Like Kurt mentioned, is there a benefit to putting the template query in the Global Query View Restriction, and not ANDing to the search terms?
	- What benefit would we get by using Novus views? If only a performance improvement would it be worth the additional code changes and setting up of views, compared to using the existing template search and Novus TNC functionality?

## Existing Capability
### Practice Area Search in Checkpoint (standard SMPA search)
#### CP UI
- When we click run search button we run the search first to get the search handle, and then redirect
	- This logic is here: `SearchBarMultiplePracticesComponent.runSearch` (line 311)
	- We send the request
	- Validate the response
	- Redirect to search handle
- Sample search request from CP-UI:
	- Federal PA with several sources
	- ![Pasted image 20240318094945.png](/.attachments/Pasted%20image%2020240318094945-9b00a850-1687-4db3-93f4-eb87e79f2d83.png)
	- ***Request:***
		```JSON
		{
		   "defaultPaId":"1",
		   "tocSearch":false,
		   "searchType":"cobalt",
		   "keywords":"kiddie tax",
		   "searchDetails":[
			  {
				 "paId":"1",
				 "categories":[
					"991", "580", "608", "609", "283", 
					"287", "306", "308", "315", "305", "26860"
				 ],
				 "externalCategories":[],
				 "tabLoc":"60"
			  }
		   ],
		   "saveHistory":true
		}
		```
		- POST Request URL: http://localhost:4200/app/api/v1/search/combine
		- Categories is a list generated by the sources we select to search
		- Search type is `cobalt` if using intuitive search, and `newtnc` if using terms & connectors
	- ***Response:***
		```JSON
		{
		    "documentCount": 277,
		    "combinedHandle": "9b307f6b-29bc-44db-b647-2a7076836b0a",
		    "searchResultUrl": null,
		    "keywordSearchSpellCheck": null,
		    "validateSearchTermResponse": null,
		    "searchHandles": {
		        "1": {
		            "documentCount": 277,
		            "searchHandle": "CMPST.2",
		            "searchResultUrl": null
		        }
		    }
		}
		```
		- In the response we get the `combinedHandle` and the `searchHandle` for each PA there are resulting documents in (if doing combined PA search)
		- These handles are then used to redirect, and display search results

#### CP Web App
- The `v1/search/combine` endpoint is called in the `SearchController`
	- ![Pasted image 20240318100239.png](/.attachments/Pasted%20image%2020240318100239-40877628-d607-455b-9d12-78fc5b1c084b.png)
	- This goes through the process of validating the search request, building up the Novus search query with the search criteria from the request, and then returning a search handle that can be used to pull up the response from Novus
	- The search is stored under the user search selection and sent to the cp-history service
- ***Selecting sources***
	- Sources are passed in a categories
	- The selected internal categories are mapped to ODSes
	- The method `MultiPASearchService#getSelectedOdsesInCategories` builds the set of ODSes from the selected categories using the user's Edge subscription (retrieved from `userAccess.getSearchHomeSearchSourcesPAUser` from the user's session)
	- These ODS ID's are then what is used to restrict the search
- ***Building Criteria***
	- Using the search request coming from the UI, and the sources ODS set the search criteria object is built up
	- The source field of the criteria object is built up
	- Using the string array of ODSes it creates the set of CP doc collection objects
	- Does this using the app data from req bean which contains list of all TOC's
	- Example of retrieving the TOC Node from the ODS ID:
		- ![Pasted image 20240318103240.png](/.attachments/Pasted%20image%2020240318103240-0189c559-118b-435d-86c1-2786c4c0eeb5.png)
- ***Creating the Query Formatter***
	- Creates the query formatter object for the search using parameters set on the search builder, and keywords
	- Determines the type of search (Cobalt, dictionary, natural language)
- ***Query Restriction***
	- Using the list of TOC ID's that were mapped from the ODSes, and originally the list of categories sent in request from CP UI, the query restriction is added to the criteria object
	- Ex: ![Pasted image 20240318103837.png](/.attachments/Pasted%20image%2020240318103837-3a4e591d-24cf-4696-80db-2c4604a57033.png)
	- This gets sent to Novus as the Global Query Restriction, and is what restricts our search to only the sources we selected
- ***Example of final query criteria:***
	- ![Pasted image 20240318104746.png](/.attachments/Pasted%20image%2020240318104746-931c3cb2-3fa3-491d-81bf-ec71604030fa.png)
	- In this case the query is simply "kiddie & tax"
	- The doc collection is `trtaintset`, the main CP doc collection

### Template Search in Checkpoint
- Example template search:
	- "FASB Codification" tab under "Citation and Other Search Tools" in the AACF PA
	- ![Pasted image 20240318105224.png](/.attachments/Pasted%20image%2020240318105224-be56689c-9afc-4f21-b6a1-dc66d72d16df.png)
	- This is an old JSP page, but it creates a web form that then executes a POST request when submitted, triggering a similar flow (just not entering through the combine endpoint)
	- Goes through the `CPSearchServlet#doNovusSmpaSearch` method
- ***Request:***
	```
	/app/main/srchTemplate
	
	FormName            = MainForm
	SearchBtn           = Search
	TEMPLATEQUERY       = (((=gaapsection:uid="260-**-***") OR (=gaapsection:uid="260-***-***")))
	code_topic          = 260
	displayquery        = Topics:~|260 Earnings Per ShareKeywords:~|kiddie tax
	feature             = taccounting
	keywords            = kiddie tax
	lastCpReqId         = 1bc
	ods                 = GAAPCODCODE
	practice            = 7
	searchType          = newtnc
	selAutoComplete     = 
	selAutoCompleteType = 
	srchTypSwitchable   = n
	tab                 = origPron
	tabLoc              = 966
	tmpl                = /v10/jsp/pageTmpl/srchFasbByTopicTitle.jsp
	```
	- Template query is provided as param on the request, in this case restricting based on the selection for desired topic in the form
	- Keywords also provided
	- ODS used to create sources/restriction is provided
	- PA is provided
	- Search time set to new terms and connectors
- ***Creating the Query Formatter***
	- In this case, since we provided a template query string, that is added to the query formatter
	- The query formatter takes the user keywords, and appends the template query with the `&` operator
- ***Example of final query criteria:***
	- Most of the rest of the flow remains the same
	- ![Pasted image 20240318110508.png](/.attachments/Pasted%20image%2020240318110508-44e2d136-75c0-418d-9d8b-106b448de130.png)
	- In this case the query is `kiddie & tax & ({{template_query}})`
	- The doc collection is `trtaintset`, the main CP doc collection

## Shared Capability- Novus Views

### Query View
- aka "Query view restriction"
- Logically partition a collection set by appending query terms to each user query
- Query view is assigned to collection in the collection set's CCI configuration
- The query terms are then appended to the users search query with AND operator
- ![Pasted image 20240314103236.png](/.attachments/Pasted%20image%2020240314103236-8d40ce94-6748-465b-8367-ebe11b131bbc.png)
### Global Query View
- Similar to query view, but NOT pre-configured in the CCI configuration for collection set
- Is a parameter of the actual search API request
- The query terms are then appended to the users search query with AND operator
- Supported in Easel: ![Pasted image 20240314102607.png](/.attachments/Pasted%20image%2020240314102607-6a03b154-d298-4463-ad31-f6dbcd2405d2.png)
### Objective View
- Define a specific element in the content that is used for grouping
- Typically use `<n-view>` element
- The element is pre-configured in the collection's Index Element Set
- Then view index files are generated when content is loaded based on the values set for the view element
- Objective Views can then be configured for the collection in a collection set’s CCI configuration via the View Expression
- ![Pasted image 20240314103906.png](/.attachments/Pasted%20image%2020240314103906-f3c1d5c7-fa15-4f31-a360-84b41566076a.png)
- Requires that the "Index View" attribute on the element you want to use for this partitioning is set to Y
- This requires full re-index
- After loading the documents, the content owners configure a collection set to include this (and any other) collections, and indicate that this collection set is limited to the documents that participate in one or more of the existing objective views
	- This is accomplished via a View Expression on the collection set configuration, or via a Global View Expression on the search request itself

### Subjective view
- Define a search query that is loaded to the collection
- The documents that match the query are ones that participate in this subjective view
- When new documents are loaded to collection they are compared against the Subjective Views loaded to the collection to determine if they should be included or not
- Subjective views configured for the collection in the collection set's CCI using view expression
- Once a subjective view is loaded to a collection, the content owners configure a collection set to include this (and any other) collections, and indicate that this collection set is limited to the documents that participate in one or more of the existing subjective views.  
	- This is accomplished via a View Expression on the collection set configuration, or via a Global View Expression on the search request itself

### View expression
- In collection set you define the view expression
- Specify the objective/subjective view to use for it or any combination of these
- Need collection sets

### Global View expression
- Same as view expression where you apply objective/subjective views
- However, it is provided through the Novus API request, and not configured on the collection
- This means we would only need to setup the views, and then when the app runs a Novus search it would specify the view expression at runtime
- Supported in Easel: ![Pasted image 20240321140152.png](/.attachments/Pasted%20image%2020240321140152-ad7b5688-b0fc-4058-a168-213f48c3db12.png)

### Comparison
- ![Pasted image 20240314133928.png](/.attachments/Pasted%20image%2020240314133928-4a7a6719-8548-4862-8953-3a0e570ea900.png)
- ***Query view***
	- Not an option, would not work on Cobalt platform
- ***Global Query View Restriction***
	- How template search currently works
	- Likely best option
	- Do we include the topic code in the global query view restriction, or just part of the query? Currently in CP we are just doing in the query, but would there be a benefit in speed or otherwise to include in global query view?
- ***Basic Query***
	- Could be an option, semantically similar to Global Query View
	- Need to understand differences better and if performance difference using global query view vs. including restriction in basic query
	- How template search currently works in CP application
- ***Subjective View***
	- Viable option
	- Would need collection sets for each topic, more content work
	- Could be better performance
- ***Objective View***
	- Possibly viable option, would need to make sure do NOT need full re-index, this is not an option if so
	- CANNOT do re-index, because would take almost a month and no other loads can happen at same time
	- If editorial is loading new documents anyway with the updated tagging, this should work to just re-index those not the whole collection (~17 million documents)
	- Would need collection sets for each topic, more content work
	- Could be better performance
	- May need specific required `n-view` elements

## Proof of Concept (POC) Template Search using Combined Search Endpoint
- In this approach we would use very similar method to the existing template searches in CP, such as the FASB Codification search
- Currently, all these template searches are located in old JSP code and not calling the new search endpoints directly
- All searches from UI go through the combine search endpoint (such as all PA searches)
- This method is simple, and would restrict the sources same as presently being done, with only difference being we pass in a template query (or required information to generate a template query) and then add this to the final query along with user's search terms
- Would require some updates
	- Need to allow current endpoint to accept template search query, ***or*** we need to create a new endpoint to support this
	- Need to modify logic slightly to allow template searches
	- Need to enable back functionality
	- Need to modify history functionality to add info on topic that was searched in addition to the terms
- Sample document with added tagging element: ![Pasted image 20240321092907.png](/.attachments/Pasted%20image%2020240321092907-d8b5fb56-43d0-4142-8dd2-41cdb1f50b7c.png)
	- The node-key for subtopic type is what we would use for the template query
### CP UI
- Can use very similar approach to `search-bar-multiple-practices.component.ts`
- When search button is clicked we call a function to run the search
- This creates a search request, and calls `searchService.getSmpaSearchHandle` which returns response shown in [CP UI](#cp-ui) section above, including search handle
- We can build up search request: ![Pasted image 20240318145832.png](/.attachments/Pasted%20image%2020240318145832-4c8964da-a914-4ed0-aafa-7512a3ea29f0.png)
- We can then simply redirect to the URL for search result given the handle like so: ![Pasted image 20240318145223.png](/.attachments/Pasted%20image%2020240318145223-c727f6aa-3f72-44dd-84df-86c564ccb07a.png)
### CP Web app
- Since the combined search endpoint, and its request model does not contain information for template search we would need to update the controller
- The POC modifies the existing endpoint and `MultipleSearchRequest` model to support template queries
- Once the property is present in the request, existing logic takes care of appending template query to the search terms
- Sample of changes needed: ![Pasted image 20240318151037.png](/.attachments/Pasted%20image%2020240318151037-0c163da0-47e4-403a-857c-cbc01601d2aa.png)

### Questions/Considerations
#### Endpoint/Controller
- Two main options:
	- Use existing `v1/search/combine` endpoint, but adding new field to the POST request body for additional information needed for template query
	- Create a new endpoint that supports this functionality, and leaving the existing endpoint as-is. This may allow greater control/customization but since most of the modifications happen later down the call stack it may not be needed
#### Constructing the template query
- Can pass in the exact template query string, and simply append to the user's query. This would require front-end having logic to construct this, and passing in with the endpoint request. This way it could be used in future for other template queries, and not limited to use for just topic pages
- Can just pass the topic code, and have the backend construct the actual template query string. This would be less flexible for uses other than topic pages, but more logical. Would also require more backend changes, and using new endpoint may make more sense.
- Do we include the topic code in the global query view restriction, or just part of the query? Currently in CP we are just doing in the query, but would there be a benefit in speed or otherwise to include in global query view?
-  If using Cobalt search, it skips over the logic adding template search query, so would need to override this functionality: ![Pasted image 20240319095027.png](/.attachments/Pasted%20image%2020240319095027-e621ad8a-1688-4363-b949-d170cc6e4222.png)
#### History
- If `saveHistory` field provided in body, will be saved to history
- Need to add template info, for example see FASB Codification search and how it includes info on the topic searched in addition to query terms: ![Pasted image 20240318111818.png](/.attachments/Pasted%20image%2020240318111818-31b9b824-70d9-4d5a-94a9-60324130de8a.png)
- changes will be required for this: ![Pasted image 20240318151436.png](/.attachments/Pasted%20image%2020240318151436-dabbc5ed-928c-490f-828c-88167317ad24.png)
	- `isFromTemplateSearch` needs to be set to true
	- `displayQuery` needs to be set to the string we want displayed for the query
- The existing template search passes what should be displayed in as a param on the request, see [Template Search in Checkpoint](#template-search-in-checkpoint) sample request
- Two methods in the `MultiPASearchService` take care of saving to history and session
	- `addSearchHandleInSession` - Create mapping of (practice area, search handle) and add it into `sessionData` with `combinedHandle` as key
	- `saveMultiPASearch` - Save multiple PA search request in history table.
#### Back to Search
- Need to determine how to set the back to URL in response so UI knows where to redirect back to and how this is happening
- Uses the `tabLoc` to determine where to go back to
	- this works fine if the page has one (all the JSP pages)
	- for Angular routing (which topic pages use right now) this will not work, in fact there is no direct URL to take you to topic pages, all done within Angular router

#### Type of Search
- Have below options:
	- ![Pasted image 20240320103727.png](/.attachments/Pasted%20image%2020240320103727-76672e3a-ffd9-401a-a9bb-9c28bae2babc.png)

#### Search Term Autocomplete
- Do we need this functionality?

#### Changing the Search Results Page Header to Include Topic Information
- Desired: ![Pasted image 20240320155523.png](/.attachments/Pasted%20image%2020240320155523-6a2439ef-e204-4ff5-9486-3f414e0cc08a.png)
- Current: ![Pasted image 20240320155554.png](/.attachments/Pasted%20image%2020240320155554-2fba8de1-3716-483f-8501-8436f5e82d9e.png)
- Because this page (`main-panel-multiple-practices.component.html` or `rsltDoc` in the URL) is derived from the search handle, this information needs to be associated with the search
- When the search request is submitted to the combine endpoint, and a search handle is returned this is then used to request metadata for the search
- ***Search metadata request:***
	- Request method: GET
	- Request URL: `/app/api/v1/searches/CMPST.9/metadata?lastCpReqId=28c&cmpType=MAIN`
- ***Search metadata response:***
	```json
	{
	    "searchHandle": "CMPST.9",
	    "primarySearchHandle": null,
	    "searchTerms": "tax",
	    "searchType": "NEWTNC",
	    "practiceArea": "1",
	    "backToSearchTemplateURL": "/app/main/srchModify?cmpType=MAIN&feature=tfederal&lastCpReqId=293&searchHandle=CMPST.9",
	    "analytics": {
	        "navigationProps": {
	            "eventName": "Navigation Event",
	            "userName": "luke.houge",
	            "accountId": "32042",
	            "webSessionId": "7d7a20fe-79ec-40fb-ab10-4d5fcf1f3905",
	            "userType": "Internal",
	            "appName": "Checkpoint",
	            "environment": "noBld Dev 24.03",
	            "viewName": "CheckpointEdge",
	            "sapCustomerNum": null,
	            "location": null,
	            "fromLocation": null
	        },
	        "eventType": "NAVIGATION",
	        "remainingLocation": null,
	        "eventProperties": {
	            "eventName": "Navigation Event",
	            "userName": "luke.houge",
	            "accountId": "32042",
	            "webSessionId": "7d7a20fe-79ec-40fb-ab10-4d5fcf1f3905",
	            "userType": "Internal",
	            "appName": "Checkpoint",
	            "environment": "noBld Dev 24.03",
	            "viewName": "CheckpointEdge",
	            "sapCustomerNum": null,
	            "location": "Federal|Federal|Back to Main Search|Federal Home",
	            "fromLocation": "Search Results"
	        }
	    },
	    "showDevView": false,
	    "subSearchMetadatas": {
	        "MAIN": {
	            "canModify": true,
	            "canNarrowSearch": true,
	            "narrowKeywords": null,
	            "canSortByRelevancy": true,
	            "hasConceptMarkers": false,
	            "hasCPError": false,
	            "canShowAllDocsList": true,
	            "canShowSourceListView": true,
	            "canShowSnippets": true,
	            "resultType": "SEARCH",
	            "viewToolsMap": {
	                "DOCS": [
	                    "PRINT",
	                    "EXPORT",
	                    "SAVE",
	                    "FLAG",
	                    "SNIPPETS"
	                ]
	            },
	            "relatedCoursesUrl": "https://qa1a-checkpointlearning.thomsonreuters.com/Courses/BasicSearch?Keywords=tax&cpType=Search",
	            "sourceId": null,
	            "currentTab": "DOCS",
	            "currentSortType": "RELEVANCE",
	            "totalDocCount": 10000,
	            "numCollections": 226,
	            "canSaveSearch": true,
	            "saveScheduleSearchURL": "/app/view/rsltDocListSavFs?cmpType=MAIN&feature=tfederal&lastCpReqId=293&searchHandle=CMPST.9&toolsFormToolId=Save&type=search",
	            "cpErrorDetail": null,
	            "taxTypes": null,
	            "hasCountriesCriteria": false
	        }
	    },
	    "topic": "Transfers of Partnership Interests",
	    "composite": true,
	    "intuitiveSearch": false
	}
	```
- For the purposes of this POC, I added the `topic` field to the response from search metadata request, which can then be used in the UI
- The `MultipleSearchRequest` model was also modified to accept a topic string
- Then, the topic originally received from the combined search request is added to the metadata response
	- ![Pasted image 20240320160434.png](/.attachments/Pasted%20image%2020240320160434-1d0a07c4-19ed-40cd-beef-d6c106a793af.png)
	- For the purposes of this POC this is just reading the original request params, but if we go this route we would want to modify the other objects and store this in a more sensible place
- The response of the metadata request is placed in an NGRX Store so the state can be shared
- We can read this, and retrieve the topic name: ![Pasted image 20240320160937.png](/.attachments/Pasted%20image%2020240320160937-04b9e2fa-42a3-4c47-8e9f-ee1297493433.png)
- ***Possible other approaches***
	- We could also store the topic name associated with a search handle in the UI and display that way
	- Modify the component to allow passing the topic name in (either directly in Angular or through URL params), and displaying that way
## Other Options
1. Could just redirect to the URL used when form is submitted on existing template searches
	- Works to just directly put this in: `/app/main/srchTemplate?FormName=MainForm&SearchBtn=Search&TEMPLATEQUERY=%28%28%28%3Dgaapsection%3Auid%3D%22260-**-***%22%29+OR+%28%3Dgaapsection%3Auid%3D%22260-***-***%22%29%29%29&keywords=taxation&practice=7&searchType=newtnc&ods=GAAPCODCODE`
	- Decoded version: `/app/main/srchTemplate?FormName=MainForm&SearchBtn=Search&TEMPLATEQUERY=(((=gaapsection:uid="260-**-***") OR (=gaapsection:uid="260-***-***")))&code_topic=260&displayquery=Topics:~|260 Earnings Per ShareKeywords:~|documents&feature=taccounting&keywords=documents&lastCpReqId=12a&ods=GAAPCODCODE&practice=7&searchType=newtnc&selAutoComplete=&selAutoCompleteType=&srchTypSwitchable=n&tab=origPron&tabLoc=966&tmpl=/v10/jsp/pageTmpl/srchFasbByTopicTitle.jsp;`
	- We can construct this URL by providing keywords, and template query
	- Not ideal way to handle this, preferred method is calling the proper endpoint from UI
2. Could use Novus views (see above section [Novus Views](#novus-views))
	- This would require no modification to the search/query flow on app side
	- Instead we would execute basic query against different collection set(s) that are associated with a subjective or objective query view and already restricted to only contain documents from a certain topic
	- This would require substantial amount of setup on content side, as well as setting up these new collections in the application code

## Possible Stories and Work Required
1. (front end) request and redirect to search handle
2. (front end) update search bar on topic page
3. (front end) return to search functionality
4. (front end) update header with topic name on search results
5. (back end) modify endpoint to accept template query (or new endpoint)
6. (back end) history functionality
7. (back end) return to search functionality
8. (SPIKE) comparing TNC/intuitive, as well as performance analysis and quality of responses
9. (SPIKE) using TNC vs. intuitive search

## Resources
- Checkpoint knowledge session on search: https://trten.sharepoint.com/sites/TRTAKSCheckpointAnswers/_layouts/15/stream.aspx?id=%2Fsites%2FTRTAKSCheckpointAnswers%2FShared%20Documents%2FGeneral%2F0%2E%20Knowledge%20Sharing%20%28KT%20session%29%2FCheckpoint%20%2D%20Knowledge%20Repo%2FRecordings%20from%20Hongtu%2Fintuitive%5Fsearch%2Emp4&referrer=StreamWebApp%2EWeb&referrerScenario=AddressBarCopied%2Eview
- TRTA search Lucid chart: https://lucid.app/lucidchart/c7a3b8fa-77c5-46b7-ba22-0834e5dd33d8/edit?invitationId=inv_03c8e2e7-01f3-4564-ad1a-c29b46af2c21&page=ECYA65N1BOTg#
- Checkpoint search overview Lucid chart: https://lucid.app/lucidchart/15dada5a-a93f-4372-9228-bc71f044378b/edit?invitationId=inv_4e0ece5d-55cd-48f6-9b59-6b29d25e9c20&page=Sf_t4H36EA8z#
- Checkpoint Answers Lucid chart: https://lucid.app/lucidchart/3c487ec5-1cc2-48d4-9beb-bd58f658b767/edit?invitationId=inv_a45dba6e-bbd4-4615-893f-3fad0609abb7&page=B4f7M4ifjVVR#
- Novus search overview document: https://trten.sharepoint.com/:w:/r/sites/novus/_layouts/15/Doc.aspx?sourcedoc=%7B76628E03-1A3A-4869-8868-6EC7B1CA74F6%7D&file=Novus%20Search%20Service%20Overview.docx&action=default&mobileredirect=true&DefaultItemOpen=1
- Novus search overview presentation: https://trten.sharepoint.com/:p:/r/sites/novus/_layouts/15/Doc.aspx?sourcedoc=%7B696B9F3B-3882-4E36-8C77-EEDCBF42DD7A%7D&file=Search%20Overview.ppt&action=edit&mobileredirect=true&DefaultItemOpen=1
- Novus views implementation guide: https://trten.sharepoint.com/:w:/r/sites/novus/_layouts/15/Doc.aspx?sourcedoc=%7B562b4176-eeac-4c03-9b74-635227b8ecc5%7D&action=view&wdAccPdf=0&wdparaid=6E43286
- Novus views presentation: https://trten.sharepoint.com/:p:/r/sites/novus/_layouts/15/Doc.aspx?sourcedoc=%7BA189EFFF-6D29-4E20-B475-81A6F8DE316F%7D&file=Views%20Presentation.ppt&action=edit&mobileredirect=true&DefaultItemOpen=1