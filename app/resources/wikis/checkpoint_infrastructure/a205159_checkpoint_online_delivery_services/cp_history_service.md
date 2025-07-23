## 1. Description

>> **[AI-GENERATED CONTENT: This text was created using artificial intelligence tools and requires human review to verify its accuracy and appropriateness]**

>> The cp_history-service microservice in the cp_web-app is responsible for tracking, storing, and managing user activity history and preferences. It exposes a set of RESTful endpoints that allow the application to:
>> *   Retrieve and display a user’s recently viewed documents and actions.
>> *   Store and fetch user-specific search selections, such as selected countries, states, and other filters, to personalize and streamline future searches.
>> *   Manage the user’s search history, including creating new history entries, updating existing selections, and deleting history records as needed.
>> *   **Support features like “recently viewed,” “last selected countries,” and “search state recall” across different modules of the application.**
>> *   Enable backend and frontend components to access and update user history data, ensuring a consistent and efficient user experience.

>> The service acts as a central point for all history-related data, making it possible for the cp_web-app to provide personalized content, remember user preferences, and facilitate quick access to frequently used or recently accessed information. Its endpoints include operations for getting, updating, and deleting history and search selection data, supporting both direct user interactions and background processes within the application.

## 2. Repository Link

>- [cp_history-service](https://github.com/tr/cp_history-service)

## 3. Libraries

## 4. Testing

>- [Swagger Links](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/1175/Swagger-links)

## 5. Diagrams

>- [Architectural Diagram](https://lucid.app/lucidchart/9aeb4fc0-5c66-4039-b206-824c0a6d6ddd/edit?invitationId=inv_cd8a8f63-048d-47f2-a008-652ebb79f5ef&page=3PuhfUG5fL.8#)