# Basic information

*   Spike Title: Create a better process for managing password changes for VDS accounts
*   @<7C68C102-F04F-6080-AF39-6A819B28E311> 

# Contents

[[_TOC_]]

# References and Resources 


### Repositories

*   [cp_web-app](https://github.com/tr/cp_web-app) 


# Purpose

### Problem Statement
The passwords for VDS accounts are configured to expire annually. Each environment has dedicated VDS accounts, meaning we will receive four separate emails throughout the year, each prompting us to update the passwords for the respective environment (development, testing, staging, production). Once notified, passwords must be updated within 30 days to avoid disruptions.
Currently, this is a manual process that requires careful attention to ensure timely updates, particularly for production environments where missed deadlines could lead to critical system-access issues. Due to the repetitive nature of this task and the risks associated with potential oversights, we recognize the need to develop a streamlined, automated solution that minimizes manual intervention and ensures password updates are handled efficiently and reliably across all environments.

### Objectives
*  Look into ways to automatically determine when a password is going to expire and automate the change password process.
*  Document suggestions/recommendations.
*  Go over suggestions/recommendations with the Tech leadership.

# Investigation Details

Technical Analysis

### Research Findings

We propose leveraging AWS Secrets Manager to securely store and manage the passwords for VDS accounts. This approach aims to fully automate password retrieval and usage, eliminating the need for any manual intervention during password updates.

## Implementation Details


### Required Changes
To implement this solution, the following steps will be taken:

Create a Custom Class

A custom class will be developed to extend the functionality of the JNDIRealm class.  
This new class will utilize AWS Secrets Manager SDK or API methods to securely fetch the required passwords from AWS Secrets Manager at runtime.  
Integrate AWS Secrets Manager with the Custom Class

The custom class will handle secure communication with AWS Secrets Manager to retrieve the appropriate password based on the environment or application it is associated with.  
This ensures the password is always up-to-date and retrieved dynamically when needed.  
Update context.xml Configuration

The existing reference to JNDIRealm in the context.xml file will be replaced with the new custom class's fully qualified class name.  
This configuration change will route authentication requests through the custom class, enabling seamless integration with AWS Secrets Manager.

This is the workflow diagram after our integration. 
![image.png](/.attachments/image-93fc2bb5-5416-4bf1-a925-d7e9569b2e06.png)

# Results
Currently, we are facing an issue where Tomcat is unable to locate our custom class during deployment. This is specifically due to the fact that our custom JAR file, which contains the implementation of the custom class, is not accessible in the classpath of the JVM that Tomcat relies on.
To resolve this, it is necessary to place the created JAR file in the **JAVA_HOME/lib** directory (the standard library directory of the Java runtime environment). By adding the JAR file here, the JVM will be able to load the custom class during Tomcat's runtime, ensuring that Tomcat can recognize the class and avoid class-loading errors during deployment.

