# Introduction
Ingestion process is a process of retrieving the data from a source, transforming it to be usable for search, and storing it in an ElasticSearch index.

We can distinguish two types of ingestion process:
- Initial Ingestion and,
- Incremental Ingestion

![ingestion-pipeline.jpg](/.attachments/ingestion-pipeline-446e8f89-bb06-47d6-b956-64a65f55cf9d.jpg)

## Initial Ingestion
The initial Ingestion is a process of loading a full set of data to the ElasticSearch index. It is useful in case of initial load or re-indexation in case of a change in the index structure or document transformation rules. The data for the initial ingestion is stored directly in the _Read Index_.
The initial ingestion app is a spring boot application that runs from the command line on EC2 instance. The process uses a lot of CPU and network resources. The details on how to run the app can be found in the [git repository](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_git/cp-search-ingestion-initial?path=%2FREADME.md&_a=preview)

## Incremental ingestion
The incremental ingestion is an AWS lambda function processing Kinesis events that represent document content update. The kinesis event contains information about file location. The content is read and processed the same way as for initial ingestion and stored in the write index.
The incremental ingestion is a continuous process. The processed documents are not visible immediately in the search. In order to make them searchable, they have to be published.
The lambda requires access to s3 bucked and ElasticSearch domain.
The code is located in a [git repository](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_git/cp-search-ingestion-lambda)

# Publish event
In theory, document updates can happen at any time but the document should be visible in the system only after it is approved (promoted to live). Hence once a day the _promote event_ is emitted. The cp-search-service application handles the event and runs a sequence of operations:
- Create a snapshot of _Read_ and _Write_ indices
- Reindex new documents from _Write_ to _Read_ index
- Mark new documents in _Write_ index as promoted