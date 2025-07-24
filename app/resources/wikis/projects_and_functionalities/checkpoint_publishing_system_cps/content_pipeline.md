# Content Pipeline Architecture

The diagram below shows the content pipeline architecture. There you can find how the data flows through the different parts until the Kinesis streams receive the records and broadcast them to the different consumer microservices.

![image.png](/.attachments/image-6223afa0-beeb-49ab-970b-c97c347ac894.png)

You can find different components from the above diagrams:
1. [Checkpoint Publishing System](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/585/Checkpoint-Publishing-System-(CPS)). The core system that process the Checkpoint content. This system triggers the "Content Agent" using two main Perl scripts: [prepilot.pl](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_git/cp-publishing?path=/Platform/Drivers/scripts/prepilot.pl) and [postpilot.pl](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_git/cp-publishing?path=/Platform/Drivers/scripts/postpilot.pl).
2. [Content Agent](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/315/Content-Agent). Spring Boot application that allows executing different commands. This is the application that starts the content pipeline.
3. DMS REST API. Spring Boot RESTful application that facilitates the retrieval of the existing Checkpoint content information. Repository [link](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_git/cp-publishing?path=/CpsCore2.0/ContentProcessing/DMSRestAPI).
4. Content Service. Spring Boot application deployed to an AWS EC2 Instance. Allows content-related transactions with AWS Services. The two main tasks in the Content Pipeline are:
   - Upload the Manifest file to the Content S3 bucket.
   - Create the "Promote" event and publish it to Kinesis.

   E.g. The admin endpoint to sync content is: https://cpa-qed-cap-content-service.5463.aws.thomsonreuters.com/api/admin/v1/content/sync.
5. AWS Datasync. AWS Service that synchronizes XML Documents and JSON Metadata information of them to the "content" S3 bucket.
6. Content S3 Bucket. Contains per-document information that gets generated through the content pipeline. Main folders: XML, Metadata, Manifest, HTML, JSON, and Plaintext.
7. AWS Lambda Functions. Compute elements that process information and transform it into common data to be used by other services.
8. Kinesis Streams. AWS Service that does broadcast the content pipeline results to all of the consumers.
   - Content stream. Contains per document metadata information.
   - Promote stream. Sends the signal of the Novus content promotion event to all services so they can promote their data from staging databases to live.
   - Platform data stream. Sends information of platform-related content such as sources, TOC, and ODSes.
9. Microservices. Consumers of the content pipeline.

## AWS Lambda workflow
```
Content Agent
	└─>a205159-cp-dev-manifest-publisher (λ function [NodeJs], trigger: 'manifest/' S3 folder)
		└─>a205159-cp-dev-content (SQS)
			└─>a205159-cp-dev-metadata-publisher (λ function [Java], trigger: SQS)
				└─>a205159-cp-dev-html-publisher (λ function [Java], trigger metadata λ)
					└─>a205159-cp-dev-json-publisher (λ function [Java], trigger: 'html/' S3 folder)
						└─>a205159-cp-dev-plaintext-publisher (λ function [python], trigger: json λ)
							└─>a205159-cp-dev-content-publisher (λ function [NodeJs], trigger: 'text/' S3 folder)
```

# References
- Checkpoint Content Pipeline Recording (Travis) - [Overview of the Content Pipeline for Checkpoint.mp4](https://trten.sharepoint.com/sites/TRTAKSCheckpointAnswers/_layouts/15/stream.aspx?id=%2Fsites%2FTRTAKSCheckpointAnswers%2FShared%20Documents%2FGeneral%2F06%20Knowledge%20Base%2FKnowledge%20Sharing%20%28KT%20session%29%2FCheckpoint%20%2D%20Knowledge%20Repo%2FRecordings%2FOverview%20of%20the%20Content%20Pipeline%20for%20Checkpoint%2Emp4&referrer=StreamWebApp%2EWeb&referrerScenario=AddressBarCopied%2Eview%2Efe588a8a%2D7e5c%2D48fc%2D8797%2Dd647e68d630d)