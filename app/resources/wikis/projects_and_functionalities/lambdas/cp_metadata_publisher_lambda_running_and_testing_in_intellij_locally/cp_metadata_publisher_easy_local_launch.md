## Environment variables
- Set Spring profile configuration with the `spring.profiles.active` entry. P.e. `spring.profiles.active=local` for local environment.
- Use `$ cloud-tool login` to create AWS credentials. Select tr-tax-cp-preprod - a205159-PowerUser2 profile.
- As a result, the data of `tr-tax-cp-preprod` profile in file `~/.aws/credentials` will be updated.
- In Intellij IDEA click:  
`Run` -> `Edit Configurations...` -> `Alt + E` -> `Environment variables` -> click `+` button -> add Name/Value  

Add environment variables from the table below:

| Name                   | Value                                                                 |
|:-----------------------|:----------------------------------------------------------------------|
| AWS_ACCESS_KEY_ID      | `C:/Users/UserId/.aws/credentials`                                    |
| AWS_SECRET_ACCESS_KEY  | `C:/Users/UserId/.aws/credentials`                                    |
| CONFIG_SERVER_URL      | `http://cpa-config-server.tr-tax-cp-preprod.aws-int.thomsonreuters.com`                                    |

## Testing AWS Lambda Locally with Spring Boot
This guide explains how to test your AWS Lambda locally using Spring Boot and a test REST controller (LocalTestController).  
You will simulate Lambda invocation by running the Spring Boot application and sending a POST request to the `LocalTestController`.
1. Start the Spring Boot Application
   Make sure to run the `MetadataPublisherApplication` class to start the Spring Boot application.  
   This will load the Spring context and expose the test REST API endpoint:  
   `mvn spring-boot:run`  
   Alternatively, run the main method in `MetadataPublisherApplication` directly from your IDE.
2. Send a Test POST Request
   Once the application is running, use curl or a tool like Postman to send a POST request to the `LocalTestController`.  
   The controller simulates passing an event (SQSEvent) to the Lambda function.

## Update the lambda code
1. update the return type of this method
```java
void extractMetadata(String publication, String guid);
to
DocumentMetadata extractMetadata(String publication, String guid);
```
2. update `apply` method
```java
    @Override  
    public String apply(SQSEvent event) {  
        ObjectMapper mapper = new ObjectMapper();  
        DocumentMetadata documentMetadata = null;  
  
        for (SQSEvent.SQSMessage message : event.getRecords()) {  
            log.info("Received queue: {}, message: {}", queueUrl, message.toString());  
            MessageBody messageBody;  
            try {  
                messageBody = mapper.readValue(message.getBody(), MessageBody.class);  
  
                if (!messageBody.getAction().equals(("deleted"))) {  
                    documentMetadata = extractMetadataService.extractMetadata(messageBody.getContentSet(), messageBody.getDocumentId());  
                } else {  
                    extractMetadataService.deleteMetadata(messageBody.getDocumentId());  
                }  
  
                JSONObject nextLambdaPayload = new JSONObject();  
                nextLambdaPayload.put("bucket", messageBody.getBucket());  
                nextLambdaPayload.put("publication", messageBody.getContentSet());  
                nextLambdaPayload.put("id", messageBody.getDocumentId());  
                nextLambdaPayload.put("action", messageBody.getAction());  
                log.info("Calling HTML publisher lambda with payload: {}", nextLambdaPayload);  
//                invokeLambda(nextLambdaPayload);  
  
            } catch (Exception ex) {  
                log.error("SQS message ingest error occurred.", ex);  
            }  
        }  
//        this.deleteMessagesByQueueUrl(event.getRecords(), queueUrl);  
        if (documentMetadata != null) {  
            return documentMetadata.toString();  
        }  
        return "done";  
    }
```
3. Add `LocalTestController` controller
```java
/*  
 * Copyright (c) 2025 Thomson Reuters Global Resources. * All Rights Reserved. Proprietary and confidential information of TRGR. * Disclosure, use, or reproduction without the written authorization of TRGR is prohibited. */  
package com.trta.contenttech.metadatapublisher.controllers;  
  
import com.amazonaws.services.lambda.runtime.events.SQSEvent;  
import com.trta.contenttech.metadatapublisher.MetadataPublisherFunction;  
import lombok.RequiredArgsConstructor;  
import org.springframework.util.MimeTypeUtils;  
import org.springframework.web.bind.annotation.PostMapping;  
import org.springframework.web.bind.annotation.RequestBody;  
import org.springframework.web.bind.annotation.RequestMapping;  
import org.springframework.web.bind.annotation.RestController;  
import java.util.List;  
  
/**  
 * REST controller for testing the Lambda function locally. * Allows testing the {@link MetadataPublisherFunction}'s apply logic by sending a POST request with JSON payload.  
 * This controller is used only for development and debugging purposes, not for production use. */@RestController  
@RequestMapping(path = "/test", produces = MimeTypeUtils.APPLICATION_JSON_VALUE)  
@RequiredArgsConstructor  
public class LocalTestControllerMy {  
  
    private final MetadataPublisherFunction function;  
  
    /**  
     * POST endpoint to test the Lambda function with a custom payload.     *     * @param payload JSON payload representing SQS message body.  
     * @return Result of processing the payload using {@link MetadataPublisherFunction}.  
     */    @PostMapping(produces = MimeTypeUtils.APPLICATION_JSON_VALUE)  
    public String publish(@RequestBody final String payload) {  
        SQSEvent event = new SQSEvent();  
        SQSEvent.SQSMessage message = new SQSEvent.SQSMessage();  
        message.setBody(payload);  
        event.setRecords(List.of(message));  
  
        return function.apply(event);  
    }  
}
```
4. Use postman with body:
```json
{
    "bucket": "a205159-cp-content-dev/",
    "contentSet": "ftlap",
    "documentId": "i0017b3ecf8d9eb12e9cfc23612cd265b",
    "action": "new"
  }
```
to test and debug lambda locally
POST: `http://localhost:8080/test`
![image.png](/.attachments/image-57d29e61-0654-4b28-a0d9-a17775feacf8.png)

PS
If spring boot starts with the following error:
`... 13 common frames omitted`
just delete/move/rename the file `logback-spring.xml`