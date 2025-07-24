# Description
The autosuggest service gives Checkpoint the capability to provide users with useful and common questions for search queries. 

![image.png](/.attachments/image-ca98fb62-61b3-411c-ab68-c5bf8d1da613.png)

# Repositories
This functionality is divided into three projects or repositories:
1. [autossugest-commons](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_git/autosuggest-commons): A common library that defines models and repository configurations for Opensearch (Elasticsearch) operations.
2. [autossugest-loader](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_git/autosuggest-loader): An Admin service that allows the population of new data to our autosuggest indices in Opensearch. The service could consume the data in two ways: 
   a. Directly uploading the file through a multipart request.
   a. Indicating the file name from a defined S3 bucket (currently unavailable).
3. [autossugest-recommender](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_git/autosuggest-recommender): Service used to consume the autosuggestions from the Application.

# Loading Questions
In order to upload new questions we will need a file with the set of questions in a format similar to the one you could find in the "Data Samples" section at the end of this document.

The original set of questions was generated with the help of the R&D team (C3 team - Taimur Javed). The Checkpoint team shared the app log files with queries to them and then they extracted and processed the questions. While processing questions, they added information such as variants of these questions, and the alpha, beta, gamma, and delta attributes based on their frequency. The SMEs then reviewed the list and gave their approval to upload them. If the questions need to be renewed based on current demand/necessities, a similar approach needs to be followed.

**Note:** We do not need to upload new questions with all the additional information (variants, alpha, beta, gamma, and delta attributes). The questions will be loaded and the application will show them. However, to properly generate new questions and influence the order in which the questions are displayed, we need the support of the R&D team. Unfortunately, they have little information about how this was done. The script may reside somewhere in their repositories.

Once the file is generated, the development team can help to upload the questions using the Autosuggest loader endpoints. Below you can find information about it.

## Autosuggest Loader
URL: https://cpa-dev-autosuggest-loader.tr-tax-cp-preprod.aws-int.thomsonreuters.com/api/docs/autosuggest-loader/swagger-ui/index.html
The Autosuggest Load service has endpoints to load new data, reindex the "incremental" index into the "live" index, and create a backup file with all the questions from the live index.

**Note:** Avoid using the PUT methods as they would replace all records from the live index. That is potentially dangerous if executed in Prod environment as it will impact the user directly.

![image.png](/.attachments/image-41fa7200-7162-4fa9-b5c1-8128cc53b12b.png)

# Pulling questions
Once the questions are uploaded to the Opensearch live index, the autosuggest recommender can read from the index and rank the results. The process is simple, the application (cp-web-app) calls the autosuggest recommender REST API to get suggestions, and the autosuggest recommender runs different queries to retrieve the best results from the Opensearch index.

## Autosuggest Recommender
URL: https://cpa-dev-autosuggest-recommender.tr-tax-cp-preprod.aws-int.thomsonreuters.com/swagger-ui.html

The Autosuggest Recommender has a single endpoint used to get suggestions from the Opensearch live index. This is the service used by the application to retrieve the questions.

![image.png](/.attachments/image-6141d4ee-edac-4f4d-898e-3c07d3728520.png)
# ElasticSearch clusters & indices:

Similar to many services in Checkpoint, this service has two data stages: the first stage, called **incremental**, is where the data is loaded when uploading a new data file, and the second stage, called **live**, is the one used by the application to show typeahead suggestions to the user. Once we want to move the incremental data into the live index, we need to reindex the incremental index using the autosuggest loader API or the Elastisearch cluster API.

The autosuggest loader has multiple endpoints to maintain the autosuggest questions. Each endpoint has the option to run the reindex from incremental to live right after the data is uploaded. However, we must be extra careful while using the PUT methods, as they would delete/replace the full data already stored in the Live index.


| Environment | Cluster | Incremental index | Live index |
|-------------|---------|------------|---------------|
| Dev     | https://vpc-a205159-cp-nonprod-ebaub3rtv44vfjrf7t476hnuka.us-east-1.es.amazonaws.com | autosuggest_dev_typeahead_doc_idx_inc | autosuggest_dev_typeahead_doc_idx_live  |
| QA      | https://vpc-a205159-cp-nonprod-ebaub3rtv44vfjrf7t476hnuka.us-east-1.es.amazonaws.com | autosuggest_test_typeahead_doc_idx_inc | autosuggest_test_typeahead_doc_idx_live  |
| Preprod | https://vpc-a205159-cp-nonprod-ebaub3rtv44vfjrf7t476hnuka.us-east-1.es.amazonaws.com | autosuggest_qed_typeahead_doc_idx_inc | autosuggest_qed_typeahead_doc_idx_live  |
| Prod    | https://vpc-a205159-cp-prod-hlukxf43gprd6xxvtdjhrbkdrm.us-east-1.es.amazonaws.com    | autosuggest_typeahead_doc_idx_inc | autosuggest_typeahead_doc_idx_live |

# Snapshots & Backups
An Opensearch snapshot was created on 06/21/2023 to back up the autosuggest questions from the production environment.

_Details:_
- Bucket: a205159-es-autosuggest-snapshot
- Repository name: autosuggest-snapshot-repository
- Snapshot name: autosuggest-snapshot-20230621
- Opensearch domain version: 7.9.1
- Index: autosuggest_typeahead_doc_idx_live_v1
- Documents: 54,848
- Postman collection: [ES Autosuggest PROD Snapshot.postman_collection.json](/.attachments/ES%20Autosuggest%20PROD%20Snapshot.postman_collection-d068e352-01d7-4011-9581-6186355c38a2.json). This was used to create the snapshot, but also have an endpoint to restore a snapshot from the repository.

Besides, here is a JSON file created also on 06/21/2023 that contains all questions from the production environment.
[suggestions_1687389897754.json](/.attachments/suggestions_1687389897754-4605d52f-96cd-4fc0-85cb-b2658013630f.json)

There are some differences with the file used in the `/load` endpoints though. A few changes are needed to prepare this file for that endpoint:
1. Replace commas with new line breaks. The file used by the `load` endpoint is not a JSON file format. Instead, each record is a JSON and is in a single line.
2. Remove the brackets '[', ']' at the start and end of file.

Take a look at the samples below to have a better idea of how the data should be prepared.
# Data samples
Here you can find two data samples for testing purposes:
1. [typeahead_docs_sample_1.json](/.attachments/typeahead_docs_sample_1-364351ce-1d26-4928-bc7c-85b5228fefdd.json)
2. [typeahead_docs_sample_2.json](/.attachments/typeahead_docs_sample_2-0bec4243-7c17-4285-b73f-7f951fb34ecf.json)