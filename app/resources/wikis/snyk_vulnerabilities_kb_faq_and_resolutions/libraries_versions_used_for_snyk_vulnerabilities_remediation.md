**Please make sure you are using the latest versions of libraries when addressing vulnerabilities.**  
If you notice that you've already used an updated library version, but the list still shows an older one, please update the information on that page. This will help ensure other developers are aware and can use the latest version as well.


**Service/Repo:**
*   Java 17
*   Spring Framework 6.2.0
*   Spring Security 6.5.0
*   Spring Boot 3.5.0
*   Spring cloud 2024.0.1
- **AWS SDK 2**
*   flyway-core 9.22.3 (this version worked with Postgres 12)
*   cp-parent 1.1.38.0-RELEASE with updating checkstyle
*   slf4j 2.0.16
*   logstash logback encoder 8.0
*   Avro 1.11.4
*   lombok 1.18.36
*   config-kms-client 0.7.10
*   com.fasterxml.jackson.core.jackson-databind 2.18.2 or higher
*   Migration from springfox → openapi swagger
*   Spring Data Opensearch 1.5.4 
*   jackson-databind 2.17.2

**Lambda:** 
*   spring-cloud-function-dependencies - 4.2.x or above
*   com.amazonaws.aws-java-sdk-bom - 1.12.780
*   aws-lambda-java-events 3.14.0 or higher
*   aws-lambda-java-core 1.2.3
*   com.amazonaws.aws-java-sdk-s3 1.12.780
*   (Optional) Migration from io.symphonia.lambda-logging → software.amazon.lambda.powertools-logging (lambda-logging is no longer supported and powertools-logging is being supported by Amazon)