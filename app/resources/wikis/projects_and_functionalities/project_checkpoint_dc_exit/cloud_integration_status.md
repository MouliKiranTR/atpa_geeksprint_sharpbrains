# Checkpoint Web App Integrations
Services currently integrated into the Checkpoint Web Application running in Cloud:

|          Service        |       Owner     |                      CI                     |                     Demo                    |                      QED                    |                Prod                |
|-------------------------|-----------------|:-------------------------------------------:|:-------------------------------------------:|:-------------------------------------------:|:----------------------------------:|
| **Database**            | Checkpoint/CUAS | <span style="color:green">PostgreSQL</span> | <span style="color:green">PostgreSQL</span> | <span style="color:green">PostgreSQL</span> | <span style="color:green">PostgreSQL</span> |
| **Search Autocomplete** | Checkpoint      | <span style="color:green">Cloud</span>      | <span style="color:green">Cloud</span>      | <span style="color:green">Cloud</span>      | <span style="color:green">Cloud</span> |
| **Doc Conversion**      | Checkpoint      | <span style="color:green">Cloud</span>      | <span style="color:green">Cloud</span>      | <span style="color:green">Cloud</span>      | <span style="color:green">Cloud</span> |
| **TRTA**                | Cobalt Delivery | <span style="color:green">Cloud</span>      | <span style="color:green">Cloud</span>      | <span style="color:green">Cloud</span>      | <span style="color:green">Cloud</span> |
| **GIS**                 | Cobalt Delivery | <span style="color:green">Cloud</span>      | <span style="color:green">Cloud</span>      | <span style="color:green">Cloud</span>      | <span style="color:green">Cloud</span> |
| **Novus**               | Novus team      | <span style="color:green">Cloud</span>      | <span style="color:green">Cloud</span>      | <span style="color:green">Cloud</span>      | <span style="color:green">Cloud</span> |
| **Nightly Snapshots**               | CPS team      | <span style="color:green">Dual</span>      | <span style="color:green">Dual</span>      | <span style="color:green">Dual</span>      | <span style="color:green">Dual</span>      |


# CUAS

Services currently integrated into the CUAS Application running in Cloud:

|          Service        |       Owner     |     CI     |    Demo    | QED | Prod |
|-------------------------|-----------------|------------|------------|-----|------|
| **Database**            | Checkpoint/CUAS | <span style="color:green">Done</span> | <span style="color:green">Done</span> |<span style="color:green">Done</span>|<span style="color:green">Done</span> |

# Databases synchonization
| Environment     | Type | Status                                            |
|:---------------:|:----:|---------------------------------------------------|
| DEV <-> CI      | DMS (one-time)  | <span style="color:green">Done</span>             |
| QA <-> Demo     | DMS (one-time)  | <span style="color:green">Done</span>             |
| Preprod <-> QED | HVR  | <span style="color:green">Done</span>  |
| Prod <-> Prod   | HVR  | <span style="color:green">Done</span>  |

# Product URLs

| Environment | AWS URL                                                 | On Prem URL                                                   | Region URL                                                      | C1 URL                                                       | C2 URL                                                       |
| ----------- | ------------------------------------------------------- | ------------------------------------------------------------- | --------------------------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Production  | [<span style="color:green"> PROD (EAG/AWS) </span>](https://checkpoint.riag.com/app/)      | [ <span style="color:green"> PROD (EAG/AWS) </span>](https://checkpoint.riag.com/app/)            | [<span style="color:red">USE1</span>](https://region-use1.checkpoint.thomsonreuters.com/)      | [<span style="color:red">C1</span>](http://site-use1c1.checkpoint.thomsonreuters.com/)      | [<span style="color:red">C2 </span>](http://site-use1c2.checkpoint.thomsonreuters.com/)      |
| QED/PreProd | [<span style="color:green">QED AWS</span>](https://checkpoint.qed.thomsonreuters.com/)   | [<span style="color:green">PreProd EAG</span>](https://preprod.checkpoint.thomsonreuters.com/) | [<span style="color:green">USE1</span>](https://region-use1.checkpoint.qed.thomsonreuters.com/)  | [<span style="color:green">C1</span>](http://site-use1c1.checkpoint.qed.thomsonreuters.com/)  | [<span style="color:red">C2</span>](http://site-use1c2.checkpoint.qed.thomsonreuters.com/)  |
| DEMO/QA     | [<span style="color:green">DEMO AWS</span>](https://checkpoint.demo.thomsonreuters.com/) | [<span style="color:green">QA EAG</span>](https://qa.checkpoint.thomsonreuters.com/)           | [<span style="color:green">USE1</span>](https://region-use1.checkpoint.demo.thomsonreuters.com/) | [<span style="color:green">C1</span>](http://site-use1c1.checkpoint.demo.thomsonreuters.com/) | [<span style="color:red"> C2 </span>](http://site-use1c2.checkpoint.demo.thomsonreuters.com/) |
| CI/DEV      | [<span style="color:green">CI AWS</span>](https://checkpoint.ci.thomsonreuters.com/)     | [<span style="color:green">DEV EAG</span>](https://dev.checkpoint.thomsonreuters.com/app/)     | [<span style="color:green">USE1</span>](https://region-use1.checkpoint.ci.thomsonreuters.com/)   | <span style="color:red">N/A</span>   | <span style="color:red">N/A</span> |


