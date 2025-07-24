Follow the Instructions  given  in readme  file for  Installation.

**LocalTest:**
Run the Docker desktop.
![image.png](/.attachments/image-cd61af4f-831a-45d3-9581-84f1f3e00479.png)

Login to cloud-tool
1. Open `File` -> `Settings` -> `Docker` -> `Docker for windows` and wait connection successful
![image.png](/.attachments/image-90c07a29-0f20-420e-afaf-7ae58d18561c.png)

2. Open Run/Debug Configurations and create a new configuration for `AWS Lambda`
*   Select `Configuration`
*   Set the handler to `com.trta.contenttech.metadatapublisher.MetadataPublisherHandler`
*   Set the runtime to `java17`
*   Set architecture to `X86_64`
*   Set timeout to `300`
*   Set memory to `1024`
*   Set `Environment Variables`

|  **Name**|**Value**  |
|--|--|
| CONFIG_SERVER_URL |[http://cpa-config-server.tr-tax-cp-preprod.aws-int.thomsonreuters.com](http://cpa-config-server.tr-tax-cp-preprod.aws-int.thomsonreuters.com/)  |
| ENVIRONMENT | dev |
|HTML_PUBLISHER_LAMBDA  | a205159-cp-dev-html-publisher |
|MAIN_CLASS  | com.trta.contenttech.metadatapublisher.MetadataPublisherApplication |
| SPRING_PROFILES_ACTIVE | dev |

![image.png](/.attachments/image-b016814e-441b-42ec-b8b3-2e0a76ae9198.png)

- Set `Text` in `Input` tab.  Any one of the below you can use it.
   Test query
**New**
{
  "Records": [
    {
      "body": "{\"bucket\":\"a205159-cp-content-dev\",\"contentSet\":\"ftlap\",\"documentId\":\"i166f181fd5814bc69bd7ddc359bda0bb\",\"action\":\"new\"}",
      "eventSource": "aws:sqs"
    }
  ]
}

**Deleted**
{
  "Records": [
    {
      "body": "{\"bucket\":\"a205159-cp-content-dev\",\"contentSet\":\"ftlap\",\"documentId\":\"i166f181fd5814bc69bd7ddc359bda0bb\",\"action\":\"deleted\"}",
      "eventSource": "aws:sqs"
    }
  ]
}

**3**. After completing the all configurations run the Lambda. If it is successfully ran you see the below log in console.
![image.png](/.attachments/image-c14ce5a2-bcac-402b-a26f-ffad4409f82b.png)


It saves result metadata to elastic server.
To verify metadata use [Swagger UI](https://cp-dev-cp-metadata-service.tr-tax-cp-preprod.aws-int.thomsonreuters.com/api/docs/cp-metadata-service/swagger-ui/index.html#/cp-metadata-service-controller/get_1 "https://cp-dev-cp-metadata-service.tr-tax-cp-preprod.aws-int.thomsonreuters.com/api/docs/cp-metadata-service/swagger-ui/index.html#/cp-metadata-service-controller/get_1").

![image.png](/.attachments/image-eebb4e49-a2d0-4ca0-b863-294cddc565b7.png)