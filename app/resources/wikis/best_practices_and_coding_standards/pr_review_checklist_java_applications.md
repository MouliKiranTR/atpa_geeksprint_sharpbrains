**Overview:**
The primary purpose of the code review process is to make sure the overall health of the codebase improves over time. To accomplish this, we need to balance a series of trade-offs among the developers and the reviewers.

First, the developers should be able to follow the best coding practices and implementation strategies outlined for them. Also, the reviewers need to carefully review the changes to ensure the codebase stays consistent and maintainable.

In the rest of the document, we will discuss the Developer Checklist, the PR review Checklist, and the Post Merge Developer Checklist. A couple of things to call out:

- This checklist is applicable to the Checkpoint web application and existing microservices developed in the Java platform.
- Eventually, we will come up with the PR review checklist for the CP-UI, CUAS-API, and CUAS-UI applications and possibly for the AWS Lambdas developed in Python language. 
- Also, we will come up with a [Pull Request Template](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/476/WIP-Pull-Request-Template). that will provide options to check the required items while creating the pull request.
- Right now, we don't enforce the check style errors through the Jenkins build pipeline in the Checkpoint web application. Once we start to enforce the check style errors through the build pipeline, we will remove a number of items from the Developer Checklist.
- So at this moment, this Checklist is mostly for awareness for the developers who create the pull requests and who review them.

**Developer Checklist:**
The developer should perform the following checks before submitting the pull request for review.  

- Perform a self-review of your code. **It's recommended to request code reviews from GitHub Co-pilot prior to request reviewers to review the changes.** This will help get some early feedback before asking others to review the code.
- Comment on complex business logic.
- Create Swagger documentation (if applicable).
- Meet at least 80% code coverage for the new changes (please note, this might not be the case for the legacy codebase - servlets and JSP changes in the Checkpoint Web application)
- Follow the [style guidelines](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/475/WIP-Coding-Standards-Java-Style-Guides) of the project.
- Verify the new and existing unit tests pass locally with my changes.
- Verify my changes don't generate new warnings (Check style and Sonar Lint).
- Verify my changes are behind a feature flag (split) or checkpoint property for the cp-web-app and cp-UI projects.
- Verify the console of my development editor (IntelliJ, Visual Studio Editor) is clean and don't print any errors or warnings when I test out my changes.
- Remove any commented code from the pull request.
- Follow the [proper commit and pull request conventions](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/469/Git-conventions) when someone commits the code to create any pull request.

For the **Checkpoint Web** application, make sure to perform the following checks:
- Use Lombok instead of writing boilerplate code.
- Run `ant --> localCheckStyle` command to make sure no new warnings were generated.
- Verify no new Sonar Lint warnings were generated before submitting the pull request.
- Run all unit tests for a test class.
- **Run the whole test suite to make sure all the unit tests pass successfully for you.**

**Important Notes: DevOps team made the required changes to integrate the unit test suite as a part of the Checkpoint build process. Based on our confirmation, once they turn it on, if any unit test fails, the build process will fail too. The build will pass only when all the unit tests pass successfully.** 

**Please make sure all the unit tests pass in your local environment before creating any pull requests. If you see any failure in the unit test, please check the latest [build status](https://cpjenkins.int.westgroup.com/job/Checkpoint/job/Deploy/job/Dev/job/checkpoint-dev-deploy-2/) to confirm the number of failed unit tests matches with the number of unit tests fails in your local environment.**

![image.png](/.attachments/image-98b25d92-3662-47ea-8475-a3e97e5d2e6b.png)

Also, for the **microservice** projects, perform the following checks as well:
- Use Lombok instead of writing boilerplate code.
- Run unit tests using the code coverage option.
- Run `mvn install` or `mvn verify` to make sure the build was successful before creating the pull request.

![image.png](/.attachments/image-c5796bed-ae00-44ad-b19b-bd29f89dc0aa.png)

**PR Review Checklist:**
It’s always better to take a quick look at a couple of things from the pull request to get a better understanding of the ask or requirements before deep-diving into the codebase. If either of these items is missing in the pull request, please suggest adding these points to the pull request.
- Task or user story number attached to the pull request.
- Description and/or snapshots added to the pull request. Snapshots are important for the UI changes – 1. Before: how the UI looked like (if applicable) and 2. After: How the UI looks now.

From a very high level, a reviewer should make sure the following things from a number of areas such as: 
- **Design**: Is the code well-designed, production-ready, and testable?
- **Functionality**: Do the changes fulfill the requirements or UACs outlined in the user story? 
- **Exception Handling**: Specific exceptions are handled properly? For example, you are using CIAM based login flow to log in to the Checkpoint application. You might not have permission to use the Checkpoint application or the exchange of tokens could fail and throw exceptions. In this type of case, catch the exceptions, log them in the log file and show the meaningful message to the end-users.
- **Complexity**: Can the code be simplified?
- **Tests**: Do the code changes have supportive unit tests?
- **Structure**: Does the code follows the existing convention of the application or use the related existing controller/service classes instead of creating new ones?
- **Code Quality**: Is the code reusable (if applicable)?
- **Naming**: The changes confirm Java naming conventions for the variables, classes, methods, etc.?
- **Style**: Does the code follow our style guides?

**Please note it's always important to provide constructive feedback and attach any example code or reference while you are suggesting for any precise improvement.**

Also, if it turns out the pull request contains changes from the mission-critical functionality, please pull the changes into your local environment and test out the changes as a part of reviewing the pull request.

Now, as a part of doing the in-depth code review, a reviewer should check several things including the following. **The list will grow over time and for most of the points, we will add an example code to get a better understanding of what is acceptable and what is not acceptable.**

**Design and Implementation:**
1. OOP principles (Abstraction, Encapsulation, Inheritance, and Polymorphism) can be applied in the code changes?
2. Any design patterns such as Singleton, Builder, or dependency injection that can be used to manage reusable, robust, and maintainable code?
3. Do changes confirm the SOLID principle?
4. Kept the business logic in the service classes and any reusable utility methods in the helper or utility classes?
5. Kept the controller class thin?
6. Wrote enough operational logs?

![image.png](/.attachments/image-350f1a4e-b629-452a-8de1-2c0d7ae0ca31.png)

8. Used [Java Stream APIs](https://www.baeldung.com/java-8-streams).
9. Used LocalDate, LocalTime, and LocalDateTime classes to work with Date/Time?
10. Used Optional in place of null?
11. Used [try](https://www.baeldung.com/java-try-with-resources) instead of try/catch/finally?

![image.png](/.attachments/image-afb00c25-5f32-4409-85b1-6dfd8624c65b.png)

12. Used StringBuilder instead of String?  
13. Used switch-case over multiple if-else conditions?

![image.png](/.attachments/image-4b11cb90-8bfe-4c39-a912-3435f9c0686f.png)

**Check Styles:**
14. Applied correct code indentation and formatting?
15. Used optimized imports instead of wildcard (*) imports? For example, unless otherwise indicated in local-checkstyle file, we should not use wild-card import (using *) unless the total classes used from same package is more than 10.
16. Broke down the code into multiple lines instead of putting them in a long one-line code?
17. Used white space to separate combined statements?
18. Used spaces before and after brackets?
19. Used curly braces for one-liner also?  


**Post Merge Check List - Checkpoint:**
- Please check the build pipeline for the specific application after you merge your pull request. Here is the Jenkins pipeline list for the Checkpoint application.

|Environment  | Jenkins Pipeline |
|--|--|
| Checkpoint |https://cpjenkins.int.westgroup.com/job/Checkpoint/job/Builds/job/cp-web-app/job/checkpoint/   |
| Checkpoint CI | https://cpjenkins.int.westgroup.com//job/Checkpoint/job/Builds/job/Pipelines/job/checkpoint-ci-deploy/  |
| Checkpoint DEV | https://cpjenkins.int.westgroup.com/job/Checkpoint/job/Deploy/job/Dev/job/checkpoint-dev-deploy/   |
| CP-UI | https://cpjenkins.int.westgroup.com/job/Checkpoint/job/Builds/job/cp-web-app/job/CheckpointBentoUI/ |

- Changes are deployed to the Checkpoint pipeline first.
- CI build triggers every half an hour and deploys the changes to the CI environment.
- DEV build triggers 2 or 3 times a day but we can always trigger the build manually as needed.
- Similarly, when we merge any pull requests for the CP-UI application, build triggers for the CP-UI application as well.
- Once the code is deployed to the CI and DEV environment successfully, please verify your changes through UI or swagger-ui.

**How to Monitor Checkpoint Build Pipeline?**
- The build pipeline triggers a new build when we merge any changes.
- Browse this [link](https://cpjenkins.int.westgroup.com/job/Checkpoint/job/Builds/job/cp-web-app/job/checkpoint/) to access Checkpoint build pipeline. 
- It takes around 55 minutes to complete the build after we integrated the test suite as a part of the build pipeline.
- Monitor the build intermittently to make sure the build passes for you successfully. 
- Or if it fails, check the console logs to figure out the root cause of the failure.

![image.png](/.attachments/image-2e54f8af-0246-486f-8260-1f58c1610ec1.png)

- Also, you can check the Test Result as well to find out how many unit tests failed in the last build.

![image.png](/.attachments/image-967096aa-6406-4d02-ab7d-624ace618094.png)


**Post Merge Check List - Microservices:**
- Each of the microservices has its own build pipeline. To find the microservice-specific build pipeline contact with the Checkpoint DevOps team or access the build pipeline from the ADO. 
- To access the build pipeline using ADO, please merge the pull request --> go to ADO --> search for the microservice --> go to History and choose in the progress build to access the build pipeline for that microservice.
- Also, we hooked up [Sonar Qube](https://sonar.prod.thomsonreuters.com/projects) in each of the build pipelines for the microservices. 
- [SonarQube](https://www.sonarqube.org/) enhance our Workflow with continuous code quality & code security. It's a code quality assurance tool that collects and analyzes source code, and provides reports for the code quality of your project. It combines static and dynamic analysis tools and enables quality to be measured continuously over time.

**References:**
- The Standard of Code Review - https://google.github.io/eng-practices/review/reviewer/standard.html#principles
- What to look for in a code review - https://google.github.io/eng-practices/review/reviewer/looking-for.html
- Code Review Developer Guide - https://google.github.io/eng-practices/review/
- Google Java Style Guide - https://google.github.io/styleguide/javaguide.html
- Code Review Checklist for Java - https://dev.to/smartyansh/code-review-checklist-for-java-beginners-181f
















