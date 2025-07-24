**Scenario/Overview**
=====================

On January 2nd Editorial Team added new charts for 2025 but no changes were reflected on Checkpoint's charts. 

**Analysis**
=================

Upon further investigation of the logs, it could be noticed that there were some SQL exceptions coming from some prepared statements. After finding the method which was throwing the exception, and debugging the code, it could be noticed that there was some code that the program's execution was not reaching. 

From the class ChartDataServiceImpl.java the method updateTaxTypes had the following lambda function: 

![image.png](/.attachments/image-9148e6f8-fbb4-4df8-a80d-26e8eb4b9c7a.png)

The code inside this function was skipped during runtime. 

**Technical Issue Details**
=================

The collection TaxTypes was processed as a java stream to which the .map() operator was applied, however the result of the .map() operation wasn't used elsewhere in the code nor assigned to a variable the compiler skipped this block of code. The reason for this behavior is that lambda functions are expected to be "pure functions" this means they shouldn't have side effects and always return the same value for a given input (idempotency), the function's utility was achieved through side effects by modifying the state of an object outside it's scope. 

Since the result of the map operation was not used anywhere nor assigned to another variable, the compiler did the right thing not executing the function (since it is supposed to be a "pure function"). 

**Root Cause Analysis**
=================

During the previous releases the java stream had a final ".toList()" operation, this last operation forced the compiler to run the code inside the lambda function. 

The reason for this operation to be removed from the stream's pipeline was because of a SonarQube alert for the result of the ".toList()" method not being used anywhere, at first glance the method could simply be removed to pass the Sonar's test however this caused all the issued described previously. 

**Solution**
=================

Iterate the Collection with an enhanced for loop instead of the stream and put the lambda's function body inside the loop's scope. 

 