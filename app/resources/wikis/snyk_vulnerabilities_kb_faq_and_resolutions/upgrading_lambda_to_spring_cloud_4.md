****Upgrading Lambda to Spring Cloud 4****
=================================================================

Introduction
------------

Upgrading from Spring Cloud 3 to Spring Cloud 4 involves changes in the way AWS Lambda functions are handled. The `SpringBootRequestHandler` class is replaced by `FunctionInvoker`.

Changes in Handler
------------------

In Spring Cloud 4, you should replace the `SpringBootRequestHandler<T, U>` with `FunctionInvoker`, which does not require type arguments. Here's an example of a custom handler class:

`public class  DataPreparationHandler extends FunctionInvoker {}`

Issue with Unit Tests
---------------------

The `FunctionInvoker` constructor triggers the application context, unlike the old `SpringBootRequestHandler`. You need to configure the Spring context appropriately for tests.

Steps to Resolve
----------------

### 1. Create Test-Specific Profiles

Create a test profile with specific properties to ensure that the application context is correctly configured during testing.
*   **bootstrap-test.yml**: Disable the config server.
    

```
spring:  
  cloud:  
    config:  
      enabled: false
```

    
*   **application-test.yml**: Define application properties. If there is database-specific configurations use H2 and disable Flyway.
    

```
spring:  
  datasource:  
    url: jdbc:h2:mem:testdb  
    driver-class-name: org.h2.Driver  
    username: sa  
    password:  
  flyway:  
    enabled: false

aws:  
  dms:  
    s3:  
      bucket-name: none
  
\\ your lambda specific properties
...
```
   

### 2. Set Active Profile

The `@SpringBootTest` and `@ActivateProfile("test")` annotations **won't** work as expected because the `FunctionInvoker` constructor will create its own application context using the default profile.
To ensure the test profile is used, set the profile as a system property:


```
public class DataPreparationHandlerTest {  
  
    DataPreparationHandler dataPreparationHandler;  
  
    @BeforeEach  
    public void setUp() {  
        System.setProperty("spring.profiles.active", "test");  
    }  
  
    @Test  
    public void test_DataPreparationHandler() {  
        dataPreparationHandler = new DataPreparationHandler();  
    }  
  
    @AfterEach  
    public void tearDown() {  
        System.clearProperty("spring.profiles.active");  
    }  
}
```


### 3. Use `@BeforeAll` for Setting Profiles (Optional)

If you prefer, you can set the profile using `@BeforeAll`.

Example
------------

Please refer to the following [Pull Request](https://github.com/tr/cp_news-dataprep/pull/11/files)