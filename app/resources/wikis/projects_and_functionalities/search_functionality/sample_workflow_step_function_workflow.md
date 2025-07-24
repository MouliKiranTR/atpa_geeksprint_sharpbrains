 Step function workflow was implemented based on the story https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_workitems/edit/90954 .

Please look at that workflow below ([Definition File](/.attachments/ContentPipeline_StepFunctions_Definition-a05ee9b7-99de-402f-9c6d-38085ebf4a88.json)):


![Screen Shot 2020-07-02 at 8.10.08 PM.png](/.attachments/Screen%20Shot%202020-07-02%20at%208.10.08%20PM-b95b1c95-1ad4-4d6a-9e3f-af623dfc478d.png)

Implemented example in AWS - https://console.aws.amazon.com/states/home?region=us-east-1#/statemachines/view/arn:aws:states:us-east-1:401148645463:stateMachine:a205159-cp-content-workflow-stepfunction-test

The workflow includes 4 lambda functions: cp-metadata-publisher,  cp-html-publisher, cp-json-publisher, cp-plaintext-publisher. Each of this lambda function returns a response which is transmitted to the next step (function). 
To suit new approach and to reduce dependencies between lambda functions there was changed input and output parameters for each function except last one.

The changes are pushed in separate branch per each repository. Also test lambda functions are existed in AWS.



| Repository              |           Branch              | 
|--|--|
| cp-metadata-publisher   | stepfunction-metadata         | 
| cp-html-publisher       | 90954-step-function-workflow  |
| cp-json-publisher       | 90954-stepfunction-workflow   |


|  AWS                                            | 
|--|
| a205159-cp-test-stepfunction-metadata-publisher |
| a205159-cp-test-stepfunction-html-publisher     |
| a205159-cp-test-stepfunction-json-publisher     |

Before cp-metadata-publisher lambda function was triggered by SQS Event. Currently it is started by Step Function. So, to follow previous approach the new Step Function should be triggered by SQS Event. Based on AWS documentation it's not possible to do it just out of the box. That's why there was created a new "proxy lambda" function which is triggered by the SQS. This function processes SQS events, creates requests based on the event information and then starts Step Function workflow. 

The lambda function is deployed using:
- Repository - [cp-content-workflow-processing - initial-pull-request Branch](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_git/cp-content-workflow-processing?path=/src/main/java/com/trta/contentworkflowprocessing/ContentProcessingWorkflowHandler.java&version=GBinitial-pull-request&_a=contents).
- Lambda function name in AWS is [a205159-cp-test-content-workflow-processing](https://us-east-1.console.aws.amazon.com/lambda/home?region=us-east-1#/functions/a205159-cp-test-content-workflow-processing?tab=code).
- SQS queue (trigger): [a205159-step-sqs](https://us-east-1.console.aws.amazon.com/sqs/v2/home?region=us-east-1#/queues/https%3A%2F%2Fsqs.us-east-1.amazonaws.com%2F401148645463%2Fa205159-step-sqs)

So, let's imagine the whole picture. Please see below:
![Screen Shot 2020-07-02 at 9.13.55 PM.png](/.attachments/Screen%20Shot%202020-07-02%20at%209.13.55%20PM-0e262717-ebb2-4450-9962-2282ea65987b.png)


1. Some information is put to the SQS.
2. cp-content-workflow-processing is triggered.
3. cp-content-workflow-processing starts Step Function workflow.
4. cp-metadata-publisher is started by Step Function. cp-metadata-publisher step contains 
   re-try logic. So, if everything goes well then Step Functions takes response from the 
   function and triggers the next lambda function. If something went wrong during 2 or 3 
   times(it can be configured) then step fails and workflow ends.  The same logic is 
   described for cp-json-publisher.

Just to mention, Step function workflow triggers per each message from the SQS. So, if you receive 3 messages from SQSEvent than 3 workflow will be started

For better understanding we suggest you to find that workflow in AWS and test/investigate it.
