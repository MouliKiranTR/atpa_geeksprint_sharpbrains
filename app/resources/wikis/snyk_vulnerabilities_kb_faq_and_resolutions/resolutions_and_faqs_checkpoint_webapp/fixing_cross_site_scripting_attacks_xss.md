# Fixing Cross Site Scripting Attacks (XSS)
- Unsanitized input from an HTTP parameter flows into print, where it is used to render an HTML page returned to the user. This may result in a Cross-Site Scripting attack (XSS).
- For more info : _**CWE-79**_:- https://cwe.mitre.org/data/definitions/79.html

To fix XSS attacks : 

Please go through documentation provided by Snyk :

https://learn.snyk.io/lesson/xss/?_gl=1*xi6aos*_ga*NTU5ODg3MDMyLjE3MTMyNTczNDE.*_ga_X9SH3KP7B4*MTcyOTE1NjA1Mi4zNC4xLjE3MjkxNTYwNTUuMC4wLjA.

- Escaping the origin place where attack may happen is one of the ways we can prevent the occurrence of attack. As said XSS mitigation where a hacker tries to inject a malicious script but the script's content has escaped and we are safe.

**How to escape the content** 
- In Java, we have _StringEscapeUtils.escapeHtml4(String input)_ from _org.apache.commons.text.StringEscapeUtils_
- This helps in escaping where user input gets injected into a response

**Issues when working with web-app**
- We have dependencies of **commons-lang -2.6, commons-lang3 -3.8.1** where StringEscapeUtils can be found, but these are deprecated and in future there might be a chance of removal. So we use the latest _**apache.commons.text**_  
- For more information on the methods escapeHtml(2.6) and escapeHtml4(from later versions), please refer to below links.
1. Lang : 2.6 : https://commons.apache.org/proper/commons-lang/javadocs/api-2.6/org/apache/commons/lang/StringEscapeUtils.html
2. Lang3 : 3.8.1 : https://commons.apache.org/proper/commons-lang/apidocs/org/apache/commons/lang3/StringEscapeUtils.html
3. Text :1.12.0 : https://commons.apache.org/proper/commons-text/apidocs/org/apache/commons/text/StringEscapeUtils.html#escapeHtml3(java.lang.String)
- Please make sure you're using the right import i.e., **org.apache.commons.text**

 ![EscapeUtils.png](/.attachments/EscapeUtils-abdbce0f-880d-4ee9-bc79-6fcdf5ce6ba2.png)

- If you are not finding the right import there may be a chance, dependencies are not built properly. Please do IvyIdea --> Resolve for All Modules and restart your IntelliJ IDE.