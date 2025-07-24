**The gist**
The recommender system combines two recommendations by:
- Elasticsearch: finding similar documents by content using the ["more like this"](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-mlt-query.html) functionality of Elasticsearch
- Word2Vec embedding of documents IDs viewed during the same session (think of IDs as words and sessions as sentences), thus catching users' behaviour regarding the current document by recommending other documents in the spirit of "users who viewed this document, also viewed..."

**Python Notebook with code and explanations**
[demo_doc_recommender_20200303_0256.html](/.attachments/demo_doc_recommender_20200303_0256-976f282c-717f-446e-a66a-40a58826b7c6.html)

**2-dimensional map (t-SNE) of 10,000 documents**
[demo_doc_recommender_20200302_0253_fig_tnse.html](/.attachments/demo_doc_recommender_20200302_0253_fig_tnse-379881fd-34b6-41d3-b5c6-dcda1ed28801.html)

**Sample of recommendations and evaluation**
[doc_recommender_examples_20200303_0259.xlsx](/.attachments/doc_recommender_examples_20200303_0259-ceb065e2-c534-435a-8406-37e3265ea563.xlsx)

**Video recording of the demo** (from 11:15)
EPAM: https://web.microsoftstream.com/video/7b293cc5-971d-4907-9608-0e48d3dd60d2
TR: https://trten.sharepoint.com/sites/TRTASearch262/Shared%20Documents/General/Search%20team%20demo-23.03.2020.mp4

**Code repository**
https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_git/cp-trcpml?path=%2Fdoc_recommender

**Data used in python notebook** 
(Account: tr-tax-cp-preprod)
https://a205159-trta-poc.s3.amazonaws.com/data_doc_recommender/data_doc_recommender.zip
