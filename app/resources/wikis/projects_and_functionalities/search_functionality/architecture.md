**Overview**

During the assignment team manage to transform legacy IntuitiveSearch application to maven module that currently follows almost all TR java code policies.

Instead of using Novus as a Search Engine, queries from cp-intuitive-search module can be directed to either Novus or newly implemented search engine based on Elasticsearch. 

![Diagram](/.attachments/image-ce7e30c3-f50c-478b-947e-e7e81f573c0e.png)

**Implementation details**

1. All codebase is currently stored in ADO Git repository:

   https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_git/cp-intuitive-search

2. Board and backlog items can be found in Search Team's board space:

   https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_boards/board/t/Checkpoint%20Search%20Team/Stories

3. Building system - module is using Maven instead of Ant. All dependencies, previously provided in binary format as a part of the repository were moved to TR's jfrog repository. In order to build project one needs to generate access key in jfrog account.

4. ML model changes - previously intuitive search had enabled internal rescoring mechanism, based on ML model trained some time ago. It was also using BerkeleyDBs data to feed the reasoning. In the development phase, experiments showed that this model is no longer useful and search engine recall is good enough to disable it.

4. Main code parts:

![image.png](/.attachments/image-0b648781-4d96-4b8e-8fc3-65b132b07b59.png)
 
   - Spring based configuration - module is using Spring framework based on BOM in version 4.0.9.RELEASE
   - Spead framework - all search requests are still served using spead activities executed in multithreaded execution framework 
   - CoreSearch, CoreSearchSerialized modules were also upload to jfrog repository and source code is already available in ado git
   - Elasticsearch search capabilities - all code related to querying Elasticsearch engine can be found in com.trgr.trta.search.elasticsearch package. Main entry point (class is autowired as spring bean to search algorithm) is 

```java
public class ElasticSearchRepository implements RepositorySearch
```

Base on parameters search algorithm is executing one or few queries that are constructed using builders from the package:

```java
package com.trgr.trta.search.elasticsearch.request.builder.impl
```
    
5. Possible improvements

   - moving to Spring Boot project - implementation already done in branch
   - 


