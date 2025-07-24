## 1. Description
This library provides endpoints and services for sending notifications via Amazon SNS (Simple Notification Service) for Checkpoint applications.

### Usage
This is a library service intended to be included in other Java services. It exposes controllers and beans for SNS integration.

## 2. Repository Link

>- [cp_notify-sns](https://github.com/tr/cp_notify-sns.git)

## 3. Libraries

## 4. Testing
As this is a library (not a standalone Spring Boot application), there are two main approaches to testing changes:  
1. Local Standalone Test Application  
- Add a main class in the source tree (same level as util, domain, controller, config, etc.):  
```java  
package com.trta.ks.notify;  
  
import org.springframework.boot.SpringApplication;      
import org.springframework.boot.autoconfigure.SpringBootApplication;            

     @SpringBootApplication  
     public class TestingApplication {         public static void main(String[] args){            
           SpringApplication.run(TestingApplication.class, args);         
     }      
}  
```   
- Set environment variables:
```shell script  
AWS_REGION=us-east-1  
AWS_PROFILE=tr-tax-cp-preprod  
```  
- Run the TestingApplication (e.g., via your IDE).   
- Once running, use http://localhost:8080 to access the endpoints exposed by the library. Endpoint details and request requirements can be found in the controller classes.  
  
2. Integration via a Consuming Service  
- Install the library locally:  
     After running mvn install in the library project, the built artifact will be saved to your local Maven repository (usually at ~/.m2/repository)  
- Search for consumer services:  
     Use the search functionality in the Thomson Reuters internal GitHub organization to look for the artifact name of this library (for example, notify-sns).  
     Look for pom.xml files in the search results that include this library as a dependency. This will help you identify which services are consuming the library.  
- Update the dependency version:  
     In the consuming service’s pom.xml, update the version of the library dependency to match the version you just built (e.g., 1.0.0-SNAPSHOT):  
```pom  
   <dependency>  
     <groupId>com.trta.ks</groupId>     
     <artifactId>notify-sns</artifactId>     
     <version>1.0.0-SNAPSHOT</version>   
   </dependency>
```   
- Check the configuration:  
     Identify the main configuration class (often named with sns in it) that ensures the library’s package is included in component scanning.  
- Constructor changes:  
     If any bean constructors in the library were modified, update the consuming service’s code accordingly (particularly for beans registered with @Bean). To minimize effort, try to avoid unnecessary changes to constructor signatures.  
- Run the consuming service and test endpoints as documented in its controller classes.  
  
### Tip:  
Whenever you make further changes to the library, re-run mvn install to update the artifact in your local .m2 repository, so consuming services will pick up the latest version.  
  
## Notes  
   - Always check controller classes for endpoint documentation and request/response details.  
   - If you need to test with a different AWS profile or region, adjust the environment variables accordingly.

## 5. Diagrams 