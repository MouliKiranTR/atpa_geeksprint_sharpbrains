# OVERVIEW
We ran into a DEV+QA issue for the June release. In this document, I outlined the details problem statement, the root cause of the problem,
resolutions, troubleshooting steps.
 
**Problem statement** 
Concept Markers is currently broken, shows a blank page

**Recreate Steps:**
1. Login to Checkpoint Dev or QA
2. Click on the Federal tab
3. Select All Sources
4. Enter "kiddie tax rules" in the search box and click on the search button
5. At the Search Results page, click on the "Child subject to kiddie tax" concept marker
***Issue: No results display.
[![ca135952-9ca6-46e9-9855-8ad58a97f225.png](/.attachments/ca135952-9ca6-46e9-9855-8ad58a97f225-45290b0c-850b-41df-af0f-376b12d682a5.png)]()

**Root cause of the problem**

The root cause of this issue is failure of the TRTA Rerank endpoint in the DEV and QA environments.
When we select any concept marker from the Search Results page, it calls the faceDocument endpoint from the SearchResultsController.java file. This endpoint calls the TRTA Rerank endpoint at some point to get the reranked results for the selected concept marker. 

This TRTA Rerank endpoint is returning 500 error for the TRTA CI and DEMO endpoints. We tested out using the QED endpoint and it works fine . 
So when we hit the endpoint 
http://trtacheckpointus-ci.int.thomsonreuters.com it returned 500(with anybody).
![e509904c-1831-41e1-98b6-3478d4aad34d.png](/.attachments/e509904c-1831-41e1-98b6-3478d4aad34d-d132881a-c907-4d60-993e-3c44c6a87012.png)![aadownload.jpeg](/.attachments/aadownload-9e47f846-9976-4171-8bc1-255a3eb0f524.jpeg).

As we already found that issue is connected with TRTA Rerank endpoint, I have gone through the cp_trta-search project and looked for the latest changes that can cause this issue.
I have found this pull request which was merged 3 weeks ago https://github.com/tr/cp_trta-search/pull/42, where was direct changes to rerank endpoint. This change was connected to XSS vulnerability issue, the idea is to encode coming request body.

**How to fix**

After we identified that this change was causing the issue, it was decided to revert this change, which resolved the issue.

