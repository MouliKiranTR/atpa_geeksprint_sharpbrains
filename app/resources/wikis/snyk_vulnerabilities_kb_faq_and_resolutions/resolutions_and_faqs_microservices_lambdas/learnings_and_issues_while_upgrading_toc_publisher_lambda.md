
We experienced many difficulties while upgrading the services/ lambdas to Spring Boot 3x, mainly due to dependency conflicts with other dependencies, incompatible/ old configuration and packaging issues. This document aims to document all the issues faced and serves as a guide to future developers to resolve their errors quickly. 


-  To upgrade from Spring boot 2.x.x to Spring Boot 3.x.xn you will need to upgrade the Java version to Amazon Coretto JDK 17 as Spring 6 is only compatible with Java 17.
- While upgrading from Spring Boot 2 to Spring Boot 3, the following issues were faced of which some might not be reproduceable in local - 
1. Locally everything working fine and your are starting to get some config's beans not found errors on cloud.It's because **while packaging we are removing tomcat**,and we have to be attentive not to include tomat with any of our dependencies. For example for toc-publisher I was using some **Servlet** related classes which requires tomcat as for http requests ,as it is excluded while packaging it may cause issues,so we have to use other classes (regular or reactive).
2. Locally everything working fine and your are getting properties not found errors on cloud,
![Screenshot 2024-10-25 150223build.png](/.attachments/Screenshot%202024-10-25%20150223build-574a3ec1-7dd4-425b-9f5f-8924f5ee2149.png)
it is related to trasnformers we have inside maven shade plugin,after spring boot 2.7.x some of the transformers are deleted from parent pom,so we should add them manually(if you have any,we had an transformers list in our lambda ,please see
![Screenshot 2024-10-25 145240transform.png](/.attachments/Screenshot%202024-10-25%20145240transform-ede62876-309e-4df9-b9ae-8265334f22e7.png)

3. You may face some `checkstyle` errors and warnings as the old structure was phased out and is no longer supported. This can be fixed by using the `checkstyle` configuration from `cp-parent` which can be found on [TR GitHub](https://github.com/tr/cp_parent).

4. If you are working on an AWS Lambda and it uses `io.symphonia.lambda-logging` then you need to upgrade to `software.amazon.lambda.powertools-logging` and use `org.aspectj.aspectjrt` along with `dev.aspectj.aspectj-maven-plugin` with it. You will also need to upgrade the logging configuration xml and update it to `log4jj2.xml`. For more information please check out the `cp-charts-publisher` lambda and view this [pull request](https://github.com/tr/cp_charts-publisher/pull/11).

**Common steps to upgrade** - 
- Upgrade the JDK version to 17. 
- Upgrade `spring-boot-dependencies` and `spring-cloud-dependencies` to a relevant version. 
- Check the compatibility matrix to see which version of [Spring Cloud](https://spring.io/projects/spring-cloud) is compatible with your version of Spring Boot. For my specific version it's cloud version 2023.0.3 for Spring Boot 3.3.4.
    ```
            <dependency>
                <groupId>org.springframework.cloud</groupId>
                <artifactId>spring-cloud-dependencies</artifactId>
                <version>${spring.cloud.version}</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
    ```
- Depending on the codebase you're working on, you might need to update the OAuth2 configuration to the one that is compatible with Spring `6.x`. In case of Lambdas, the `OAuth2ClientConfiguration` was updated. Example - [cp-charts-publisher](https://github.com/tr/cp_charts-publisher/blob/main/src/main/java/com/tr/checkpoint/charts/config/OAuthClientConfiguration.java)
- If your microservice/ lambda has `SpringBootRequestHandler`, it needs to be changed to `FunctionInvoker`.
- If your microservice/ lambda uses `RestTemplate`, it needs to be changed to use either `RestClient` or `WebClient` as `RestTemplate` is deprecated.

Part of services uses checkpoint libraries that could bring critical transitive issues
* **Spring cloud function adapter aws**
   * Consider also updating spring cloud related dependencies , also related dependencies such as spring-cloud-function-context

**References**
- Lambdas
1. [cp-toc-publisher](https://github.com/tr/cp_toc-publisher)
2. [cp-charts-publisher](https://github.com/tr/cp_charts-publisher)



