Datadog is used for a centralized logging, monitoring, and analytics for CP applications and services. We have three organizations:

# trta-cp-prod
- [Link](https://trta-cp-prod.datadoghq.com/)
- Contains Checkpoint owned services such as:
  - _200172_
    - CP WebApp
    - Search Auto Complete
    - Doc Conversion
  - _205159_
    - CP microservices (this is where Search API/Service, Tool Service, Auth Service, etc. are)

# tr-contentandresearch-prod
- [Link](https://tr-contentandresearch-prod.datadoghq.com/)
- Contains Cobalt shared services such as:
  - _203669_
    - CUAS API
    - CP and CUAS Shared DB (this can also be found in the trta-cp-prod account)
  - _203848_
    - Checkpoint US Search Service (TRTA Search)

# tr-central-prod
- [Link](https://tr-central-prod.datadoghq.com/)
- Contains Apigee which sits in front of the CP Search API


