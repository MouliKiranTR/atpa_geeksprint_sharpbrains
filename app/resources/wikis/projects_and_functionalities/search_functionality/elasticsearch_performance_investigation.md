# TLDR Recommendations
- For master nodes, the lowest generic instance type is enough. It does not influence the search and for a cluster with 3 nodes, it is sufficient.

- Memory is not an issue for this setup; 64GB for data nodes is enough.
- There is no much difference between instance storage and IOPS provisioned storage

- More CPU power is required. The number of available search threads is strictly related to the nr of available CPUs. For 16 cores per data node, we have 25 search threads. Search threads count is a number of searches we can handle concurrently. 

- As an additional step, a more restrictive query can be constructed that will select fewer documents, which will save CPU cycles wasted on scoring records that are not returned either way because of the low score. We need some additional testing on how it influences the intuitive search ranking.


ES setup:

- 3 dedicated master nodes
  - c5.large.elasticsearch
- 3 data nodes
  - m5.4xlarge.elasticsearch  - 16 vCPU, 64GB memory or larger (focused on CPUs)

# The problem
We have an AWS elasticsearch setup:

- 3 dedicated master nodes
  - m5.xlarge.elasticsearch
- 3 data nodes
  - r5.2xlarge.elasticsearch - 8 vCPU, 64 GB memory



We encounter longer response times for a high number of concurrent requests.

# Investigation
I started by recreating the environment with a close to the production setup.

- 3 dedicated master nodes
  - c5.large.elasticsearch
- 3 data nodes
  - i3.2xlarge.elasticsearch  - 8 vCPU, 61GB memory

Then switched to general-purpose instances with IOPS provisioned

- 3 dedicated master nodes
  - c5.large.elasticsearch
- 3 data nodes
  - m5.4xlarge.elasticsearch  - 16 vCPU, 64GB memory


I chose the i3 instance for data nodes to check if the storage influences the ES. This type of storage is local machine storage, so these are SSDs located on the same physical machine than the ES instance.

I've created a few JMeter tests for the following scenarios:

- 1 request (0.5 users) - no other requests send to the ES at the same time. It is used as a baseline showing how the ES behaves without any significant load.
- 5 requests (1 user) - this case is a simulation of a request to the intuitive search. For one intuitive search request, five requests to the ES are performed in average
- 50 requests (10 users) - simulation of 5 users performing the search concurrently
- 125 requests (25 users)
- 250 requests (50 users)

These tests are stress tests trying to put the load on elasticsearch. The number of users shows users hitting the ES at the same time. In real life, it means hundreds of users using the system the usual way: perform a search, view the results list, open the document, and so on.


In addition to that, I repeated the above tests for a different number of returned documents to check how it influences the performance as well.

- 0 documents - this tests the basic match query, no scoring needed here
- 1 document - this includes the scoring minimalizing the document retrieve part
- 10 documents - usual page size as a reference
- 200 documents - the number of documents we use

# Tests results
## All the results




| CPUs | Users | # Docs | # Samples | Average | Median | 90% Line | 95% Line | 99% Line | Min | Max |Throughput | Received KB/sec | Comment |
|--|--|--|--|--|--|--|--|--|--|--|--|--|--|
|8	|0.2	|0	|​1000	|​3	|​3	|​4	|​5	|​41	|​1	|​78	|​3.66886	|​1.29	||
|8	|1	|0	|55000	|5	|2	|6	|36	|62	|1	|117	|97.24703	|34.42	||
|8	|25	|0	|125000	|10	|3	|40	|49	|81	|1	|253	|407.37844	|144.52	||
|8	|50	|0	|250000	|12	|3	|45	|58	|88	|1	|250	|436.40832	|155.05	||
|8	|0.2	|1	|1000	|52	|42	|93	|115	|197	|4	|329	|3.11834	|1.09	|Enabling scoring|
|8	|1	|1	|5000	|60	|50	|110	|136	|208	|2	|413	|14.82079	|5.16	||
|8	|10	|1	|50000	|386	|404	|540	|584	|715	|2	|1857	|72.74960	|25.76	||
|8	|25	|1	|125000	|1191	|1201	|1730	|1990	|2495	|3	|3660	|83.06294	|29.51	||
|8	|50	|1	|250000	|2674	|2532	|4766	|5259	|5909	|2	|7729	|83.09496	|29.56	||
|8	|0.2	|10	|1000	|62	|51	|115	|150	|240	|2	|397	|3.00774	|1.06	||
|8	|1	|10	|5000	|71	|60	|131	|167	|241	|2	|586	|14.35651	|5.03	||
|8	|10	|10	|50000	|504	|524	|671	|722	|853	|3	|1978	|62.42462	|22.24	||
|8	|25	|10	|125000	|1430	|1470	|1992	|2290	|2756	|1	|4149	|69.89113	|24.97	||
|8	|50	|10	|250000	|3245	|3648	|5448	|5746	|6254	|2	|7924	|69.50153	|24.87	||
|8	|0.2	|200	|1000	|94	|83	|166	|196	|324	|2	|548	|2.57206	|0.91	||
|8	|1	|200	|5000	|111	|96	|200	|240	|341	|2	|707	|10.93099	|3.85	||
|8	|10	|200	|50000	|511	|500	|889	|1000	|1219	|3	|2518	|42.60363	|15.26	||
|8	|25	|200	|125000	|1749	|1870	|2582	|2825	|3406	|2	|5501	|45.32677	|16.28	||
|8	|50	|200	|250000	|4583	|5032	|7778	|8293	|9178	|3	|11715	|45.07498	|16.22	||
|16	|0.2	|0	|1000	|2	|2	|3	|3	|5	|1	|48	|4.39043	|1.54	||
|16	|1	|0	|55000	|2	|2	|3	|3	|39	|1	|83	|116.14745	|41.10	||
|16	|25	|0	|125000	|3	|2	|3	|8	|41	|1	|86	|463.30959	|164.28	||
|16	|50	|0	|250000	|3	|2	|3	|10	|42	|1	|90	|461.27334	|163.76	||
|16	|0.2	|1	|1000	|67	|48	|125	|165	|342	|1	|1014	|3.42384	|1.20	||
|16	|1	|1	|5000	|55	|44	|103	|131	|205	|3	|1127	|17.26579	|6.02	||
|16	|10	|1	|50000	|86	|73	|159	|195	|291	|1	|1511	|153.37423	|54.23	||
|16	|25	|1	|125000	|352	|370	|520	|572	|753	|1	|1748	|188.08532	|66.66	||
|16	|50	|1	|250000	|983	|901	|1880	|2029	|2224	|2	|3468	|198.89114	|70.68	||
|16	|0.2	|200	|1000	|97	|88	|171	|198	|308	|2	|428	|2.60030	|0.92	||
|16	|1	|200	|5000	|88	|76	|160	|195	|268	|2	|683	|12.63357	|4.46	||
|16	|10	|200	|50000	|136	|121	|242	|290	|413	|1	|998	|79.85996	|28.58	||
|16	|25	|200	|125000	|373	|331	|711	|822	|1059	|1	|2738	|105.12886	|37.68	||
|16	|50	|200	|250000	|777	|686	|1589	|1858	|2429	|1	|4137	|104.06733	|37.37	||


## CPU utilization
### 0 documents - match only and count
The CPU usage is no more than 32-33%
![8 cores - aggregated [0 docs] - cpu utilization.png](/.attachments/8%20cores%20-%20aggregated%20[0%20docs]%20-%20cpu%20utilization-bbf63d4e-d9a8-41a1-bdfd-8363b191f254.png)


We can see that for 0 docs query, ES performs excellent for all nr of concurrent requests (250 max). Checking an ES thread pool, we can see some spikes in the queue, so probably we are somewhere close to the limit.
![8 cores - aggregated [0 docs] - search thread pool.png](/.attachments/8%20cores%20-%20aggregated%20[0%20docs]%20-%20search%20thread%20pool-3b9a61b3-7a88-41f1-9160-d233ea75083c.png)


### 1 document - enable scoring
Enabling scoring increased CPU usage significantly. For the 50 concurrent users (250 threads), the CPU is almost constant 100%. Which is also reflected in the search thread pool.
![8 cores - aggregated [1 docs] - cpu utilization.png](/.attachments/8%20cores%20-%20aggregated%20[1%20docs]%20-%20cpu%20utilization-6077f140-a23c-4c03-9bf8-67cc0ce19db6.png)
![8 cores - aggregated [1 docs] - search thread pool.png](/.attachments/8%20cores%20-%20aggregated%20[1%20docs]%20-%20search%20thread%20pool-1ed96895-dfbf-421f-896b-23f30c2b3445.png)


Used search thread pool means that requests are queued and have to wait to be processed. We can see that in increased the response time.

### 10/200 documents
Here the situation is similar to the 1 document. The difference is the higher response time
![8 cores - aggregated [200 docs] - cpu utilization.png](/.attachments/8%20cores%20-%20aggregated%20[200%20docs]%20-%20cpu%20utilization-722515eb-89f9-4d2a-bc72-71c7eaec6051.png)
![8 cores - aggregated [200 docs] - search thread pool.png](/.attachments/8%20cores%20-%20aggregated%20[200%20docs]%20-%20search%20thread%20pool-0dc9ea6c-e657-4bd5-91ce-21cf929d2c69.png)



## 16 cores CPU utilization
### 0 documents - match only and count
The CPU usage dropped, and the thread pool spikes disappeared.
![16 cores - aggregated [0 docs] - cpu utilization.png](/.attachments/16%20cores%20-%20aggregated%20[0%20docs]%20-%20cpu%20utilization-641836dd-648a-4f79-b595-bc5a059d2f64.png)
![16 cores - aggregated [0 docs] - search thread pool.png](/.attachments/16%20cores%20-%20aggregated%20[0%20docs]%20-%20search%20thread%20pool-e533ada3-dfd9-4ec1-9764-323d9dfcd562.png)


### 1 document - enable scoring
Increasing nr of cores improved things a lot in this case; the CPU is still high, but if we look closely on the charts, the test took less time (40min vs. 1.5h), and the thread pool is a bit less loaded.
![16 cores - aggregated [1 docs] - cpu utilization.png](/.attachments/16%20cores%20-%20aggregated%20[1%20docs]%20-%20cpu%20utilization-ccb2495d-f8a3-41dd-b844-c1300e70b00b.png)
![16 cores - aggregated [1 docs] - search thread pool.png](/.attachments/16%20cores%20-%20aggregated%20[1%20docs]%20-%20search%20thread%20pool-77bd05cf-1554-483a-810a-4cd73df025f9.png)


### 10/200 documents
A similar situation is for 200 docs (1h 10min vs. 3h)
![16 cores - aggregated [200 docs] - cpu utilization.png](/.attachments/16%20cores%20-%20aggregated%20[200%20docs]%20-%20cpu%20utilization-a9e5cbd1-6b8f-4d89-8a35-8e7b712e6afb.png)![16 cores - aggregated [200 docs] - search thread pool.png](/.attachments/16%20cores%20-%20aggregated%20[200%20docs]%20-%20search%20thread%20pool-9045f9b9-7199-476d-bf8c-c2d01f38c77e.png)



## Memory
In all cases, the ES had ~31GB of the heap and ~31GB for the system memory, and in all cases, memory looked perfectly fine. For the hardest test (200 docs, 50 users), we had no full GC and only young GC, which is the desired state.
![16 cores - aggregated [200 docs] - young collection count.png](/.attachments/16%20cores%20-%20aggregated%20[200%20docs]%20-%20young%20collection%20count-601da553-01f7-49a5-b498-0ae001af365f.png)
![16 cores - aggregated [200 docs] - old collection count.png](/.attachments/16%20cores%20-%20aggregated%20[200%20docs]%20-%20old%20collection%20count-d341224b-2aa9-408d-af3d-a0a8d3608be7.png)

### 8 cores vs. 16 cores
![8 cores - aggregated [200 docs] - memory pressure.png](/.attachments/8%20cores%20-%20aggregated%20[200%20docs]%20-%20memory%20pressure-faae2a12-2c67-4f48-a1ba-7f5d50bbc404.png)
![16 cores - aggregated [200 docs] - memory pressure.png](/.attachments/16%20cores%20-%20aggregated%20[200%20docs]%20-%20memory%20pressure-8c168231-110e-4282-8c84-72498ffda593.png)


# Conclusion
We can see that to handle more users we need more CPU. Hence a few things can be done to improve performance:

- Increase nr of CPUs available to ES (preferred one)
- Restrict the query - this way we the ES will have to score fewer documents
- Simplify the query - we can lose precision




