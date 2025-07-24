# **Some requests and responses with real values in dev postgreSQL database(7/7/2025) I used for cp-charts-service endpoints:**



**1. GET /api/v1/charts/chartpars**

**Response Body:**

```json
[
  {
    "id": "BNA",
    "name": "Bloomberg BNA 2017 State Tax Department Survey",
    "taxTypes": [
      "BNABNA"
    ],
    "sortOrder": 1,
    "status": "updated",
    "lastUpdated": "2025-07-04T02:46:38.069+00:00"
  },
  {
    "id": "BNASTCIT",
    "name": "Corporate Income Tax",
    "taxTypes": [
      "BNASTCITBNASTCIT"
    ],
    "sortOrder": 2,
    "status": "updated",
    "lastUpdated": "2025-07-04T02:46:38.114+00:00"
  },
  {
    "id": "BNASTGIN",
    "name": "Green Incentives Chart Builder",
    "taxTypes": [
      "BNASTGINBNASTGIN"
    ],
    "sortOrder": 3,
    "status": "updated",
    "lastUpdated": "2025-07-04T02:46:38.203+00:00"
  },
  {
    "id": "BNASTIIT",
    "name": "Individual Income Tax",
    "taxTypes": [
      "BNASTIITBNASTIIT"
    ],
    "sortOrder": 4,
    "status": "updated",
    "lastUpdated": "2025-07-04T02:46:38.204+00:00"
  },
  {
    "id": "BNASTSUT",
    "name": "Sales&Use Tax",
    "taxTypes": [
      "BNASTSUTBNASTSUT"
    ],
    "sortOrder": 5,
    "status": "updated",
    "lastUpdated": "2025-07-04T02:46:38.208+00:00"
  },
  {
    "id": "IBFD",
    "name": "IBFD Tax Rates",
    "taxTypes": [
      "IBFDIBFD"
    ],
    "sortOrder": 6,
    "status": "updated",
    "lastUpdated": "2025-07-04T02:46:38.275+00:00"
  },
  {
    "id": "IBFDINTPEN",
    "name": "IBFD Interest&Penalties",
    "taxTypes": [
      "IBFDINTPENIBFDINTPEN"
    ],
    "sortOrder": 7,
    "status": "updated",
    "lastUpdated": "2025-07-04T02:46:38.286+00:00"
  },
  {
    "id": "IBFDSTPR",
    "name": "IBFD KF - Non US States/Provinces",
    "taxTypes": [
      "IBFDSTPRIBFDSTPR"
    ],
    "sortOrder": 8,
    "status": "updated",
    "lastUpdated": "2025-07-04T02:46:38.301+00:00"
  },
  {
    "id": "IBFDTREATY",
    "name": "IBFD Tax Treaties",
    "taxTypes": [
      "IBFDTREATYIBFDTREATY"
    ],
    "sortOrder": 9,
    "status": "updated",
    "lastUpdated": "2025-07-04T02:46:38.305+00:00"
  },
  {
    "id": "IBFDUSST",
    "name": "IBFD KF -US States",
    "taxTypes": [
      "IBFDUSSTIBFDUSST"
    ],
    "sortOrder": 10,
    "status": "updated",
    "lastUpdated": "2025-07-04T02:46:38.308+00:00"
  },
  {
    "id": "INTL",
    "name": "International",
    "taxTypes": [
      "INTLINC"
    ],
    "sortOrder": 11,
    "status": "updated",
    "lastUpdated": "2025-07-04T02:46:38.310+00:00"
  },
  {
    "id": "INTLRATES",
    "name": "International Tax Rates",
    "taxTypes": [
      "INTLRATESINTLRATES"
    ],
    "sortOrder": 12,
    "status": "updated",
    "lastUpdated": "2025-07-04T02:46:38.451+00:00"
  },
  {
    "id": "PAY",
    "name": "Payroll Tax",
    "taxTypes": [
      "PAYPAY"
    ],
    "sortOrder": 13,
    "status": "updated",
    "lastUpdated": "2025-07-04T02:46:38.451+00:00"
  },
  {
    "id": "BEPS",
    "name": "BEPS",
    "taxTypes": [
      "BEPSBEPS"
    ],
    "sortOrder": 14,
    "status": "updated",
    "lastUpdated": "2025-07-04T02:46:38.544+00:00"
  },
  {
    "id": "INTLCREDITS",
    "name": "",
    "taxTypes": [
      "INTLCREDITSINTLCREDITS"
    ],
    "sortOrder": 15,
    "status": "updated",
    "lastUpdated": "2025-07-04T02:46:38.545+00:00"
  },
  {
    "id": "IBFDATAD",
    "name": "ATAD Implementation Table",
    "taxTypes": [
      "IBFDATADIBFDATAD"
    ],
    "sortOrder": 16,
    "status": "updated",
    "lastUpdated": "2025-07-04T02:46:38.548+00:00"
  },
  {
    "id": "IBFDBEPS",
    "name": "IBFD BEPS Country Monitor",
    "taxTypes": [
      "IBFDBEPSIBFDBEPS"
    ],
    "sortOrder": 17,
    "status": "updated",
    "lastUpdated": "2025-07-04T02:46:38.556+00:00"
  },
  {
    "id": "IBFDMLIT",
    "name": "Outline",
    "taxTypes": [
      "IBFDMLITIBFDMLIT"
    ],
    "sortOrder": 18,
    "status": "updated",
    "lastUpdated": "2025-07-04T02:46:38.580+00:00"
  },
  {
    "id": "CREDITS",
    "name": "Credits&Incentives",
    "taxTypes": [
      "CREDITSCREDITS"
    ],
    "sortOrder": 19,
    "status": "updated",
    "lastUpdated": "2025-07-04T02:46:38.585+00:00"
  },
  {
    "id": "EF",
    "name": "E-Filing",
    "taxTypes": [
      "EFCORP",
      "EFPSHIP",
      "EFPERS"
    ],
    "sortOrder": 20,
    "status": "updated",
    "lastUpdated": "2025-07-04T02:46:38.594+00:00"
  },
  {
    "id": "NEXUS",
    "name": "NEXUS",
    "taxTypes": [
      "NEXUSCORP",
      "NEXUSSU"
    ],
    "sortOrder": 21,
    "status": "updated",
    "lastUpdated": "2025-07-04T02:46:39.779+00:00"
  },
  {
    "id": "SL",
    "name": "State&Local",
    "taxTypes": [
      "SLCORP",
      "SLPERS",
      "SLPSHIP",
      "SLSCORP",
      "SLLLC",
      "SLLLP",
      "SLFRAN",
      "SLINIT",
      "SLSU",
      "SLPROP",
      "SLLO",
      "SLEG",
      "SLFM",
      "SLPU",
      "SLINS"
    ],
    "sortOrder": 22,
    "status": "updated",
    "lastUpdated": "2025-07-04T02:46:39.786+00:00"
  },
  {
    "id": "IBFDDTM",
    "name": "Digital Taxation Monitor",
    "taxTypes": [
      "IBFDDTMIBFDDTM"
    ],
    "sortOrder": 23,
    "status": "updated",
    "lastUpdated": "2025-07-04T02:46:48.801+00:00"
  },
  {
    "id": "IBFDTAXCOMP",
    "name": "Tax Compliance Tables",
    "taxTypes": [
      "IBFDTAXCOMPIBFDTAXCOMP"
    ],
    "sortOrder": 24,
    "status": "updated",
    "lastUpdated": "2025-07-04T02:46:48.813+00:00"
  },
  {
    "id": "IBFDTPDOC",
    "name": "Transfer Pricing Documentation Table",
    "taxTypes": [
      "IBFDTPDOCIBFDTPDOC"
    ],
    "sortOrder": 25,
    "status": "updated",
    "lastUpdated": "2025-07-04T02:46:48.834+00:00"
  },
  {
    "id": "IBFDVATST",
    "name": "VAT&Sales Tax Tables",
    "taxTypes": [
      "IBFDVATSTIBFDVATST"
    ],
    "sortOrder": 26,
    "status": "updated",
    "lastUpdated": "2025-07-04T02:46:48.843+00:00"
  }
]
````

**2.GET /api/v1/charts/jurisdictions**
**Response Body:**

```json
[
  {
    "id": "AK",
    "odsName": "SLAK",
    "name": "Alaska",
    "type": "State"
  },
  {
    "id": "AL",
    "odsName": "SLAL",
    "name": "Alabama",
    "type": "State"
  },
  {
    "id": "AR",
    "odsName": "SLAR",
    "name": "Arkansas",
    "type": "State"
  },
  {
    "id": "AZ",
    "odsName": "SLAZ",
    "name": "Arizona",
    "type": "State"
  },
  {
    "id": "CA",
    "odsName": "SLCA",
    "name": "California",
    "type": "State"
  },
  {
    "id": "CO",
    "odsName": "SLCO",
    "name": "Colorado",
    "type": "State"
  },
  {
    "id": "CT",
    "odsName": "SLCT",
    "name": "Connecticut",
    "type": "State"
  },
  {
    "id": "DE",
    "odsName": "SLDE",
    "name": "Delaware",
    "type": "State"
  },
  {
    "id": "DC",
    "odsName": "SLDC",
    "name": "District of Columbia",
    "type": "Federal District"
  },
  {
    "id": "FL",
    "odsName": "SLFL",
    "name": "Florida",
    "type": "State"
  },
  {
    "id": "GA",
    "odsName": "SLGA",
    "name": "Georgia",
    "type": "State"
  },
  {
    "id": "HI",
    "odsName": "SLHI",
    "name": "Hawaii",
    "type": "State"
  },
  {
    "id": "IA",
    "odsName": "SLIA",
    "name": "Iowa",
    "type": "State"
  },
  {
    "id": "ID",
    "odsName": "SLID",
    "name": "Idaho",
    "type": "State"
  },
  {
    "id": "IL",
    "odsName": "SLIL",
    "name": "Illinois",
    "type": "State"
  },
  {
    "id": "IN",
    "odsName": "SLIN",
    "name": "Indiana",
    "type": "State"
  },
  {
    "id": "KS",
    "odsName": "SLKS",
    "name": "Kansas",
    "type": "State"
  },
  {
    "id": "KY",
    "odsName": "SLKY",
    "name": "Kentucky",
    "type": "State"
  },
  {
    "id": "LA",
    "odsName": "SLLA",
    "name": "Louisiana",
    "type": "State"
  },
  {
    "id": "MA",
    "odsName": "SLMA",
    "name": "Massachusetts",
    "type": "State"
  },
  {
    "id": "MD",
    "odsName": "SLMD",
    "name": "Maryland",
    "type": "State"
  },
  {
    "id": "ME",
    "odsName": "SLME",
    "name": "Maine",
    "type": "State"
  },
  {
    "id": "MN",
    "odsName": "SLMN",
    "name": "Minnesota",
    "type": "State"
  },
  {
    "id": "MI",
    "odsName": "SLMI",
    "name": "Michigan",
    "type": "State"
  },
  {
    "id": "MO",
    "odsName": "SLMO",
    "name": "Missouri",
    "type": "State"
  },
  {
    "id": "MS",
    "odsName": "SLMS",
    "name": "Mississippi",
    "type": "State"
  },
  {
    "id": "MT",
    "odsName": "SLMT",
    "name": "Montana",
    "type": "State"
  },
  {
    "id": "NC",
    "odsName": "SLNC",
    "name": "North Carolina",
    "type": "State"
  },
  {
    "id": "ND",
    "odsName": "SLND",
    "name": "North Dakota",
    "type": "State"
  },
  {
    "id": "NE",
    "odsName": "SLNE",
    "name": "Nebraska",
    "type": "State"
  },
  {
    "id": "NH",
    "odsName": "SLNH",
    "name": "New Hampshire",
    "type": "State"
  },
  {
    "id": "OK",
    "odsName": "SLOK",
    "name": "Oklahoma",
    "type": "State"
  },
  {
    "id": "NJ",
    "odsName": "SLNJ",
    "name": "New Jersey",
    "type": "State"
  },
  {
    "id": "NM",
    "odsName": "SLNM",
    "name": "New Mexico",
    "type": "State"
  },
  {
    "id": "NV",
    "odsName": "SLNV",
    "name": "Nevada",
    "type": "State"
  },
  {
    "id": "NY",
    "odsName": "SLNY",
    "name": "New York",
    "type": "State"
  },
  {
    "id": "OH",
    "odsName": "SLOH",
    "name": "Ohio",
    "type": "State"
  },
  {
    "id": "OR",
    "odsName": "SLOR",
    "name": "Oregon",
    "type": "State"
  },
  {
    "id": "PA",
    "odsName": "SLPA",
    "name": "Pennsylvania",
    "type": "State"
  },
  {
    "id": "RI",
    "odsName": "SLRI",
    "name": "Rhode Island",
    "type": "State"
  },
  {
    "id": "SC",
    "odsName": "SLSC",
    "name": "South Carolina",
    "type": "State"
  },
  {
    "id": "SD",
    "odsName": "SLSD",
    "name": "South Dakota",
    "type": "State"
  },
  {
    "id": "TN",
    "odsName": "SLTN",
    "name": "Tennessee",
    "type": "State"
  },
  {
    "id": "TX",
    "odsName": "SLTX",
    "name": "Texas",
    "type": "State"
  },
  {
    "id": "UT",
    "odsName": "SLUT",
    "name": "Utah",
    "type": "State"
  },
  {
    "id": "VA",
    "odsName": "SLVA",
    "name": "Virginia",
    "type": "State"
  },
  {
    "id": "VT",
    "odsName": "SLVT",
    "name": "Vermont",
    "type": "State"
  },
  {
    "id": "WA",
    "odsName": "SLWA",
    "name": "Washington",
    "type": "State"
  },
  {
    "id": "WI",
    "odsName": "SLWI",
    "name": "Wisconsin",
    "type": "State"
  },
  {
    "id": "WV",
    "odsName": "SLWV",
    "name": "West Virginia",
    "type": "State"
  },
  {
    "id": "WY",
    "odsName": "SLWY",
    "name": "Wyoming",
    "type": "State"
  }
]
```

**3. GET /api/v1/charts/taxYears**
**Response Body:**

```json
[
  "2024",
  "2023",
  "2022",
  "2021",
  "2020",
  "2017",
  "2016",
  "2015",
  "2014",
  "2013",
  "2012"
]
```


**4. GET /api/v1/charts/taxtypes/{type}**

**a)** 

```
Parameters: 
type: IBFDINTPEN
parType: IBFDINTPEN
```

**Response Body:**

```json
{
  "type": "IBFDINTPEN",
  "name": "IBFD Interest & Penalties",
  "parType": "IBFDINTPEN",
  "year": null,
  "description": null,
  "sortOrder": 1
}
````

**b)** 

```
Parameters:
type: IBFDSTPR
parType: IBFDSTPR
```

**Response Body:**
```json
{
  "type": "IBFDSTPR",
  "name": "IBFD KF - Non US States/Provinces",
  "parType": "IBFDSTPR",
  "year": null,
  "description": null,
  "sortOrder": 1
}
```

**c)** 

```
Parameters:
type: random
parType: random
```
 
**Response Body:**
```json
{
  "type": null,
  "name": null,
  "parType": null,
  "year": null,
  "description": null,
  "sortOrder": 0
}
```


**5. GET /api/v1/charts/{partype}/taxtypes**

**a)** 


```
Parameters:
parType: IBFDINTPEN
```

**Response Body:**

```json
[
  {
    "type": "IBFDINTPEN",
    "name": "IBFD Interest & Penalties",
    "parType": "IBFDINTPEN",
    "year": null,
    "description": null,
    "sortOrder": 1
  }
]
```

**b)** 

```
Parameters:
parType: IBFDSTPR
```


**Response Body:**
```sql
[
  {
    "type": "IBFDSTPR",
    "name": "IBFD KF - Non US States/Provinces",
    "parType": "IBFDSTPR",
    "year": null,
    "description": null,
    "sortOrder": 1
  }
]
```

**c)** 

```
Parameters:
parType: random
```


**Response Body:**
```json
[]
```

**6. POST /api/v1/charts/charttypes**

**a)**
**Request Body:**
```json
{
  "taxTypes": ["PSHIP"],
  "parType": "EF",
  "years": ["2024"]
}
```

**Response Body:**
```json
{
  "PSHIP": [
    {
      "id": "PSHIP1",
      "name": "52--53 Week Filers--(Tax Year 2024)",
      "taxType": "PSHIP",
      "parType": "EF",
      "chartTypes": [
        {
          "id": "82052024",
          "name": "E-File 52--53 Week Filer Return (Tax Year 2024)",
          "taxType": "PSHIP",
          "parType": "EF",
          "sortOrder": 1,
          "year": "2024",
          "description": "This chart shows if the state allows the e-filing of a 52--53 week filer's return."
        }
      ],
      "sortOrder": 1,
      "year": "2024"
    },
    {
      "id": "PSHIP2",
      "name": "Amended Returns--(Tax Year 2024)",
      "taxType": "PSHIP",
      "parType": "EF",
      "chartTypes": [
        {
          "id": "82102024",
          "name": "E-File Amended Return (Tax Year 2024)",
          "taxType": "PSHIP",
          "parType": "EF",
          "sortOrder": 1,
          "year": "2024",
          "description": "If the partnership wishes to make changes to an e-filed return that has been accepted and acknowledged by the state, can the partnership e-file an amended return?"
        }
      ],
      "sortOrder": 6,
      "year": "2024"
    },
    {
      "id": "PSHIP3",
      "name": "E-File Application Process--(Tax Year 2024)",
      "taxType": "PSHIP",
      "parType": "EF",
      "chartTypes": [
        {
          "id": "80902024",
          "name": "State Application Process (Tax Year 2024): EROs",
          "taxType": "PSHIP",
          "parType": "EF",
          "sortOrder": 1,
          "year": "2024",
          "description": "This chart shows the process for accepting electronic return originators (EROs) into the state's e-file program."
        },
        {
          "id": "80952024",
          "name": "State Application Process (Tax Year 2024): Software Developers",
          "taxType": "PSHIP",
          "parType": "EF",
          "sortOrder": 2,
          "year": "2024",
          "description": "This chart shows the process for accepting software developers into the state's e-file program."
        },
        {
          "id": "81002024",
          "name": "State Application Process (Tax Year 2024): Transmitters or EDI Uploading",
          "taxType": "PSHIP",
          "parType": "EF",
          "sortOrder": 3,
          "year": "2024",
          "description": "This chart shows the process for accepting electronic data interface (EDI) transmitters into the state's e-file program."
        },
        {
          "id": "81052024",
          "name": "State Application Process (Tax Year 2024): Partnership Self Filers",
          "taxType": "PSHIP",
          "parType": "EF",
          "sortOrder": 4,
          "year": "2024",
          "description": "This chart shows the process for accepting partnership self filers into the state's e-file program."
        }
      ],
      "sortOrder": 11,
      "year": "2024"
    },
    {
      "id": "PSHIP4",
      "name": "E-File Calendar--(Tax Year 2024)",
      "taxType": "PSHIP",
      "parType": "EF",
      "chartTypes": [
        {
          "id": "81802024",
          "name": "E-File Calendar (Tax Year 2024): Beginning Date for Accepting E-Filed Returns",
          "taxType": "PSHIP",
          "parType": "EF",
          "sortOrder": 1,
          "year": "2024",
          "description": "This chart shows the beginning date for transmitting e-filed state returns."
        },
        {
          "id": "81852024",
          "name": "E-File Calendar (Tax Year 2024): Cut-Off Date for Filing Extended Initial E-Returns",
          "taxType": "PSHIP",
          "parType": "EF",
          "sortOrder": 2,
          "year": "2024",
          "description": "This chart shows the last date for transmitting extended initial e-filed state returns."
        },
        {
          "id": "81902024",
          "name": "E-File Calendar (Tax Year 2024): Cut-Off Date for Resubmitting Extended Rejected E-Returns",
          "taxType": "PSHIP",
          "parType": "EF",
          "sortOrder": 3,
          "year": "2024",
          "description": "This chart shows the last date for resubmitting extended rejected e-filed state returns."
        },
        {
          "id": "81952024",
          "name": "E-File Calendar (Tax Year 2024): Turnaround Deadline for Resubmitting Rejected Returns",
          "taxType": "PSHIP",
          "parType": "EF",
          "sortOrder": 4,
          "year": "2024",
          "description": "This chart shows the turnaround deadline for resubmitting rejected returns."
        }
      ],
      "sortOrder": 16,
      "year": "2024"
    },
    {
      "id": "PSHIP5",
      "name": "E-File Program--(Tax Year 2024)",
      "taxType": "PSHIP",
      "parType": "EF",
      "chartTypes": [
        {
          "id": "80002024",
          "name": "Supports E-Filing (Tax Year 2024)",
          "taxType": "PSHIP",
          "parType": "EF",
          "sortOrder": 1,
          "year": "2024",
          "description": "This chart shows whether the state allows or requires partnerships to e-file their annual income tax return through the federal/state e-file program (i.e. using a commercial vendor's website, a commercial vendor's software package or a paid tax preparer) or the state's independent e-file program."
        },
        {
          "id": "80052024",
          "name": "Supports E-Filing (Tax Year 2024): Participates in Federal/State 1065 E-File Program",
          "taxType": "PSHIP",
          "parType": "EF",
          "sortOrder": 2,
          "year": "2024",
          "description": "Partnerships preparing and/or transmitting their state income tax return or relying on tax professionals to do so may electronically file their annual return using the IRS federal/state 1065 e-file program. This chart shows whether or not the state participates in the program."
        },
        {
          "id": "80102024",
          "name": "Supports E-Filing (Tax Year 2024): Fed/State But Also Accepts State-Only E-Filing",
          "taxType": "PSHIP",
          "parType": "EF",
          "sortOrder": 3,
          "year": "2024",
          "description": "The IRS allows an electronic return originator (ERO) or a partnership self filer to transmit/retransmit a state return through the federal/state e-file system without simultaneously transmitting a federal return. This chart shows whether the state will accept the state-only return."
        },
        {
          "id": "80152024",
          "name": "Supports E-Filing (Tax Year 2024): State Has Separate Direct E-File Program",
          "taxType": "PSHIP",
          "parType": "EF",
          "sortOrder": 4,
          "year": "2024",
          "description": "Assuming a state does not participate in the federal/state 1065 e-filing program, does it have its own direct e-file program?"
        },
        {
          "id": "80202024",
          "name": "Supports Online or Web Filing (Tax Year 2024)",
          "taxType": "PSHIP",
          "parType": "EF",
          "sortOrder": 5,
          "year": "2024",
          "description": "This chart shows whether or not the state allows or requires partnership self filers to prepare and file their income tax return on the state website."
        }
      ],
      "sortOrder": 21,
      "year": "2024"
    },
    {
      "id": "PSHIP6",
      "name": "EFIN/ETIN--(Tax Year 2024)",
      "taxType": "PSHIP",
      "parType": "EF",
      "chartTypes": [
        {
          "id": "81502024",
          "name": "Use of Federal EFIN/ETIN (Tax Year 2024)",
          "taxType": "PSHIP",
          "parType": "EF",
          "sortOrder": 1,
          "year": "2024",
          "description": "This chart shows if the state allows an electronic return originator to use the federal EFIN or ETIN."
        }
      ],
      "sortOrder": 26,
      "year": "2024"
    },
    {
      "id": "PSHIP7",
      "name": "ELF Coordinator--(Tax Year 2024)",
      "taxType": "PSHIP",
      "parType": "EF",
      "chartTypes": [
        {
          "id": "82202024",
          "name": "State ELF Coordinator (Tax Year 2024)",
          "taxType": "PSHIP",
          "parType": "EF",
          "sortOrder": 1,
          "year": "2024",
          "description": "This chart shows the name, address, telephone number, fax number and e-mail address of the state electronic filing coordinator."
        }
      ],
      "sortOrder": 31,
      "year": "2024"
    },
    {
      "id": "PSHIP8",
      "name": "Filing Extensions--(Tax Year 2024)",
      "taxType": "PSHIP",
      "parType": "EF",
      "chartTypes": [
        {
          "id": "82152024",
          "name": "E-File Request for Extension (Tax Year 2024)",
          "taxType": "PSHIP",
          "parType": "EF",
          "sortOrder": 1,
          "year": "2024",
          "description": "If the state requires partnerships to file a state application for extension of time to file an annual income tax return, does the state allow the application to be filed online?"
        }
      ],
      "sortOrder": 36,
      "year": "2024"
    },
    {
      "id": "PSHIP9",
      "name": "Fiscal Year Returns--(Tax Year 2024)",
      "taxType": "PSHIP",
      "parType": "EF",
      "chartTypes": [
        {
          "id": "82002024",
          "name": "E-File Fiscal Year Return (Tax Year 2024)",
          "taxType": "PSHIP",
          "parType": "EF",
          "sortOrder": 1,
          "year": "2024",
          "description": "This chart shows if the state allows the e-filing of a partnership's fiscal year tax return."
        }
      ],
      "sortOrder": 41,
      "year": "2024"
    },
    {
      "id": "PSHIP10",
      "name": "Mandatory E-Filing--Partnerships--(Tax Year 2024)",
      "taxType": "PSHIP",
      "parType": "EF",
      "chartTypes": [
        {
          "id": "80602024",
          "name": "Mandatory E-Filing--Partnerships (Tax Year 2024)",
          "taxType": "PSHIP",
          "parType": "EF",
          "sortOrder": 1,
          "year": "2024",
          "description": "The IRS currently requires certain partnerships with more than 100 partners to file their federal income tax return electronically. This chart shows whether or not the state has a similar (or any other) mandate for partnerships to e-file their state income tax returns."
        },
        {
          "id": "80652024",
          "name": "Mandatory E-Filing--Partnerships (Tax Year 2024): Effective Year of Mandate",
          "taxType": "PSHIP",
          "parType": "EF",
          "sortOrder": 2,
          "year": "2024",
          "description": "Assuming that the state requires partnerships to e-file the annual partnership income tax return, this chart shows the year of mandate."
        },
        {
          "id": "80702024",
          "name": "Mandatory E-Filing--Partnerships (Tax Year 2024): Threshold?",
          "taxType": "PSHIP",
          "parType": "EF",
          "sortOrder": 3,
          "year": "2024",
          "description": "Assuming that the state requires partnerships to e-file the annual partnership income tax return, this chart shows the e-filing requirement threshold."
        },
        {
          "id": "80752024",
          "name": "Mandatory E-Filing--Partnerships (Tax Year 2024): Exceptions to Mandate",
          "taxType": "PSHIP",
          "parType": "EF",
          "sortOrder": 4,
          "year": "2024",
          "description": "Assuming that the state requires partnerships to e-file the annual partnership income tax return, this chart shows if the state has provided any exception to the mandate."
        },
        {
          "id": "80802024",
          "name": "Mandatory E-Filing--Partnerships (Tax Year 2024): Waiver Process",
          "taxType": "PSHIP",
          "parType": "EF",
          "sortOrder": 5,
          "year": "2024",
          "description": "Assuming that the state provides an exception to the e-filing mandate, this chart shows whether or not the state provides for a formal waiver process."
        },
        {
          "id": "80852024",
          "name": "Mandatory E-Filing--Partnerships (Tax Year 2024): Penalties for Noncompliance",
          "taxType": "PSHIP",
          "parType": "EF",
          "sortOrder": 6,
          "year": "2024",
          "description": "Assuming that the state requires partnerships to e-file the annual partnership income tax return, this chart shows the penalty for noncompliance."
        }
      ],
      "sortOrder": 46,
      "year": "2024"
    },
    {
      "id": "PSHIP11",
      "name": "Mandatory E-Filing--Tax Professionals--(Tax Year 2024)",
      "taxType": "PSHIP",
      "parType": "EF",
      "chartTypes": [
        {
          "id": "80252024",
          "name": "Mandatory E-Filing--Tax Professionals (Tax Year 2024)",
          "taxType": "PSHIP",
          "parType": "EF",
          "sortOrder": 1,
          "year": "2024",
          "description": "This chart shows whether or not the state mandates tax professionals to e-file the annual partnership income tax return."
        },
        {
          "id": "80302024",
          "name": "Mandatory E-Filing--Tax Professionals (Tax Year 2024): Effective Year of Mandate",
          "taxType": "PSHIP",
          "parType": "EF",
          "sortOrder": 2,
          "year": "2024",
          "description": "Assuming that the state requires tax professionals to e-file the annual partnership income tax return, this chart shows the year of mandate."
        },
        {
          "id": "80352024",
          "name": "Mandatory E-Filing--Tax Professionals (Tax Year 2024): Threshold?",
          "taxType": "PSHIP",
          "parType": "EF",
          "sortOrder": 3,
          "year": "2024",
          "description": "Assuming that the state requires tax professionals to e-file the annual partnership income tax return, this chart shows the e-filing requirement threshold."
        },
        {
          "id": "80402024",
          "name": "Mandatory E-Filing--Tax Professionals (Tax Year 2024): Exceptions to Mandate",
          "taxType": "PSHIP",
          "parType": "EF",
          "sortOrder": 4,
          "year": "2024",
          "description": "Assuming that the state requires tax professionals to e-file the annual partnership income tax return, this chart shows if the state has provided any exception to the mandate."
        },
        {
          "id": "80452024",
          "name": "Mandatory E-Filing--Tax Professionals (Tax Year 2024): Waiver Process",
          "taxType": "PSHIP",
          "parType": "EF",
          "sortOrder": 5,
          "year": "2024",
          "description": "Assuming that the state provides an exception to the e-filing mandate, this chart shows whether or not the state provides for a formal waiver process."
        },
        {
          "id": "80502024",
          "name": "Mandatory E-Filing--Tax Professionals (Tax Year 2024): Taxpayer Opt-Out",
          "taxType": "PSHIP",
          "parType": "EF",
          "sortOrder": 6,
          "year": "2024",
          "description": "Assuming that the state has a mandatory e-filing program, this chart shows whether or not taxpayers can opt out of the requirement to e-file their returns."
        },
        {
          "id": "80552024",
          "name": "Mandatory E-Filing--Tax Professionals (Tax Year 2024): Penalties for Noncompliance",
          "taxType": "PSHIP",
          "parType": "EF",
          "sortOrder": 7,
          "year": "2024",
          "description": "Assuming that the state requires tax professionals to e-file the annual partnership income tax return, this chart shows the penalty for noncompliance."
        }
      ],
      "sortOrder": 51,
      "year": "2024"
    },
    {
      "id": "PSHIP12",
      "name": "Signature Documents--(Tax Year 2024)",
      "taxType": "PSHIP",
      "parType": "EF",
      "chartTypes": [
        {
          "id": "81252024",
          "name": "E-Filing Signature Documents (Tax Year 2024): Electronic (Digitized) Signature/PIN",
          "taxType": "PSHIP",
          "parType": "EF",
          "sortOrder": 1,
          "year": "2024",
          "description": "This chart shows if the state allows or requires the use of an e-signature (PIN) option for partnership returns."
        },
        {
          "id": "81302024",
          "name": "E-Filing Signature Documents (Tax Year 2024): Rubber Stamp Signature",
          "taxType": "PSHIP",
          "parType": "EF",
          "sortOrder": 2,
          "year": "2024",
          "description": "Assuming that the state allows or requires the partnership self filer or ERO to sign a signature form, this chart shows whether the state allows the use of a rubber stamp signature."
        },
        {
          "id": "81352024",
          "name": "E-Filing Signature Documents (Tax Year 2024): Scanned (PDF) Copy of Original Signature",
          "taxType": "PSHIP",
          "parType": "EF",
          "sortOrder": 3,
          "year": "2024",
          "description": "Assuming that the state allows or requires the partnership self filer or ERO to sign a signature form, this chart shows whether the state allows the use of a scanned (PDF) copy of the original signature."
        },
        {
          "id": "81402024",
          "name": "E-Filing Signature Documents (Tax Year 2024): Photocopy or Fax of Paid Preparer's Original Signature",
          "taxType": "PSHIP",
          "parType": "EF",
          "sortOrder": 4,
          "year": "2024",
          "description": "Assuming that the state allows or requires the ERO to sign a signature form, this chart shows whether the state allows the use of a photocopy or fax of the paid preparer's original signature."
        },
        {
          "id": "81452024",
          "name": "E-Filing Signature Documents (Tax Year 2024): Photocopy or Fax of Partner's Original Signature",
          "taxType": "PSHIP",
          "parType": "EF",
          "sortOrder": 5,
          "year": "2024",
          "description": "Assuming that the state allows or requires the ERO to sign a signature form, this chart shows whether the state allows the use of a photocopy or fax of the partner's original signature."
        }
      ],
      "sortOrder": 56,
      "year": "2024"
    },
    {
      "id": "PSHIP13",
      "name": "Signature Process--(Tax Year 2024)",
      "taxType": "PSHIP",
      "parType": "EF",
      "chartTypes": [
        {
          "id": "81102024",
          "name": "E-Filing Signature Process (Tax Year 2024): E-Filing Signature Form Required",
          "taxType": "PSHIP",
          "parType": "EF",
          "sortOrder": 1,
          "year": "2024",
          "description": "For purposes of signing the electronic return, this chart shows whether the state allows or requires a partnership self filer or an ERO to sign a signature form."
        },
        {
          "id": "81152024",
          "name": "E-Filing Signature Process (Tax Year 2024): ERO or Partnership Self Filer Keeps Signature Form",
          "taxType": "PSHIP",
          "parType": "EF",
          "sortOrder": 2,
          "year": "2024",
          "description": "Assuming that the state allows or requires the partnership self filer or ERO to sign a signature form, this chart shows whether the form is required to be kept by the partnership self filer or the ERO."
        },
        {
          "id": "81202024",
          "name": "E-Filing Signature Process (Tax Year 2024): Signature Form Sent to State Tax Agency",
          "taxType": "PSHIP",
          "parType": "EF",
          "sortOrder": 3,
          "year": "2024",
          "description": "Assuming that the state allows or requires a signature form, this chart shows whether the form is required to be sent to the state."
        }
      ],
      "sortOrder": 61,
      "year": "2024"
    },
    {
      "id": "PSHIP14",
      "name": "Tax Due Payment--(Tax Year 2024)",
      "taxType": "PSHIP",
      "parType": "EF",
      "chartTypes": [
        {
          "id": "81552024",
          "name": "Tax Due Payment (Tax Year 2024): Electronic Funds Transfer (EFT)",
          "taxType": "PSHIP",
          "parType": "EF",
          "sortOrder": 1,
          "year": "2024",
          "description": "When paying a balance due on an e-filed return, does the state allow the partnership to pay by electronic funds transfer (EFT)?"
        },
        {
          "id": "81602024",
          "name": "Tax Due Payment (Tax Year 2024): Electronic Funds Withdrawal (EFW)",
          "taxType": "PSHIP",
          "parType": "EF",
          "sortOrder": 2,
          "year": "2024",
          "description": "When paying a balance due on an e-filed return, does the state allow the partnership to pay by electronic funds withdrawal (EFW)?"
        },
        {
          "id": "81652024",
          "name": "Tax Due Payment (Tax Year 2024): Online Payment via State Website",
          "taxType": "PSHIP",
          "parType": "EF",
          "sortOrder": 3,
          "year": "2024",
          "description": "In addition to, or as an alternative to the EFT/EFW payment method, does the state allow the partnership to pay the balance due on an e-filed return through the state revenue department's website?"
        },
        {
          "id": "81702024",
          "name": "Tax Due Payment (Tax Year 2024): Credit Card Payment",
          "taxType": "PSHIP",
          "parType": "EF",
          "sortOrder": 4,
          "year": "2024",
          "description": "When paying a balance due on an e-filed return, does the state allow the partnership to pay by credit card or debit card?"
        },
        {
          "id": "81752024",
          "name": "Tax Due Payment (Tax Year 2024): Mail Check Payment",
          "taxType": "PSHIP",
          "parType": "EF",
          "sortOrder": 5,
          "year": "2024",
          "description": "When paying a balance due on an e-filed return, does the state allow the partnership to pay by check or money order?"
        }
      ],
      "sortOrder": 66,
      "year": "2024"
    }
  ]
}
```

**b)**
**Request Body:**
```json
{
  "taxTypes": ["random"],
  "parType": "random",
  "years": ["2024"]
}
```

**Response Body:**
```json
{
  "random": []
}
```


**7. POST /api/v1/charts/search**

**a)**

```
Parameters:
page = 1
maxResult = 25
```
**Request Body:**
```json
{
  "parType": "SL",
  "states": ["NC"],
  "chartCriteria": [
    {
      "taxType": "CORP",
      "chartTypes": ["10170"]
    }
  ]
}
```

```json
[
  {
    "chartId": "10170",
    "chartTitle": "Combined Reporting Required/Allowed",
    "chartDesc": "This chart shows whether each state requires or allows combined reporting.",
    "chartHeaders": [
      "State",
      "Combined Return",
      "Authority",
      "Editorial Reference"
    ],
    "chartContainer": [
      {
        "docId": "ie89857306d7f41d4e5c3b9e01957331d",
        "chartEntry": "10170",
        "taxType": "CORP",
        "stateCol": "NC",
        "chartColumns": [
          {
            "description": "NC",
            "srcLink": [],
            "shortAnswer": null,
            "updatedDate": null
          },
          {
            "description": "<br/> North Carolina does not require or allow combined reporting. However, exceptions apply.",
            "srcLink": [],
            "shortAnswer": "Does not allow.",
            "updatedDate": null
          },
          {
            "description": "<LINK>N.C. Gen. Stat.   § 105-130.14</LINK>",
            "srcLink": [
              {
                "destinationGuid": "i9e19bccb8df4e805816f88f7c6daab91",
                "srcUrl": "/app/main/docLinkNew?DocID=i9e19bccb8df4e805816f88f7c6daab91",
                "linkText": "N.C. Gen. Stat.   § 105-130.14"
              }
            ],
            "shortAnswer": null,
            "updatedDate": null
          },
          {
            "description": "<LINK>12,410</LINK>;<LINK>¶ 1013NC:1000</LINK>",
            "srcLink": [
              {
                "destinationGuid": "ie89857306d7f41d4e5c3b9e01957331d",
                "srcUrl": "/app/main/docLinkNew?DocID=ie89857306d7f41d4e5c3b9e01957331d",
                "linkText": "12,410"
              },
              {
                "destinationGuid": "ie6382f29243dccc7fb3f929e9b9d3eac",
                "srcUrl": "/app/main/docLinkNew?DocID=ie6382f29243dccc7fb3f929e9b9d3eac",
                "linkText": "¶ 1013NC:1000"
              }
            ],
            "shortAnswer": null,
            "updatedDate": null
          }
        ]
      }
    ]
  }
]
```

**b)** 
**Request Body:**
```json
{
  "parType": "random",
  "states": ["random"],
  "chartCriteria": [
    {
      "taxType": "random",
      "chartTypes": ["random"]
    }
  ]
}
```

**Response Body:**
```json
[] 
```

**8. POST /api/v1/charts/suggestions**

**a)** 

```
Parameters:
searchTerms: c corporation tax
practiCeArea: 2
maxResults: 10
chartParType: SL
```
**Request Body:**
```json
{
  "taxTypes": ["CORP"]
}
```
**Response Body:**
```json
[
  {
    "heading": "Charts",
    "contents": [
      {
        "snapshotId": "11330|SL|CORP",
        "title": "Where to File—C Corporations—Tax Due",
        "text": "This chart shows where to file the C corporation's annual return when tax is due.",
        "contentUrl": null,
        "metadata": null,
        "score": 24.991678
      },
      {
        "snapshotId": "11760|SL|CORP",
        "title": "Estimated Tax Threshold--C Corporations",
        "text": "This chart shows the threshold for paying estimated taxes by a C corporation.",
        "contentUrl": null,
        "metadata": null,
        "score": 24.991678
      },
      {
        "snapshotId": "11535|SL|CORP",
        "title": "Estimated Tax Installments--C Corporations",
        "text": "Assuming that the state allows or requires the payment of estimated taxes on an installment basis, this chart shows the amount of the estimated tax installments that C Corporations must pay.",
        "contentUrl": null,
        "metadata": null,
        "score": 24.991678
      },
      {
        "snapshotId": "12895|SL|CORP",
        "title": "Filing Date—C Corporation—Amended Return",
        "text": "This chart shows the due date for filing an amended corporation income tax return.",
        "contentUrl": null,
        "metadata": null,
        "score": 24.426086
      },
      {
        "snapshotId": "10240|SL|CORP",
        "title": "Filing Date—C Corporation—Annual Return",
        "text": "This chart shows the due date for filing the C Corporation's annual return.",
        "contentUrl": null,
        "metadata": null,
        "score": 24.426086
      },
      {
        "snapshotId": "10230|SL|CORP",
        "title": "Estimated Tax Due Dates--C Corporations",
        "text": "This chart shows the due dates for paying estimated tax by C Corporations.",
        "contentUrl": null,
        "metadata": null,
        "score": 24.00821
      },
      {
        "snapshotId": "11605|SL|CORP",
        "title": "Estimated Tax Safe Harbor--C Corporations",
        "text": "This chart shows the estimated tax safe harbor for C corporations.",
        "contentUrl": null,
        "metadata": null,
        "score": 24.00821
      },
      {
        "snapshotId": "11045|SL|CORP",
        "title": "Penalties--Underpayment of Estimated Tax--C Corporations",
        "text": "This chart shows the penalty for underpayment of estimated tax by C Corporations.",
        "contentUrl": null,
        "metadata": null,
        "score": 24.00821
      },
      {
        "snapshotId": "10880|SL|CORP",
        "title": "Supports E-filing--C Corporation Annual Return",
        "text": "This chart shows whether the state allows or requires C Corporations to e-file their annual income tax return through the federal/state e-file program (i.e. using a commercial vendor's website, a commercial vendor's software package or a paid tax preparer) or the state's independent e-file program.",
        "contentUrl": null,
        "metadata": null,
        "score": 23.662218
      },
      {
        "snapshotId": "13105|SL|CORP",
        "title": "Filing Date Short Period Returns--C Corporation",
        "text": "This chart shows the short period return due date for C corporations.",
        "contentUrl": null,
        "metadata": null,
        "score": 23.662218
      }
    ],
    "weight": 6.6,
    "significant": false
  }
]
```

**And when Parameter 'practiceArea" value change to 1:**
**Response Body:**
```json
[
  {
    "heading": "Charts",
    "contents": [],
    "weight": 0,
    "significant": false
  }
]
```

**9. POST /api/admin/v1/charts/import**

```
Response: 
Started import Chart Data from s3://a205159-cp-charts-service-dev/chart-data/202507041123.xml
```


**10. POST /api/admin/v1/charts/export**

In postman create new request, **Authorization**: mark **Bearer** token and paste **cp_access_token**'s **value** from checkpoint.ci.thomsonreuters.com

In **Request Body**, mark **form_data**

**1. convertDocRequest**  (mark **text**) value: `{"threadId":"abc-123","documents":[{"docId":"doc-001","docName":"hello","type":"htm"}],"convertToDocType":"pdf"}`

**2. files**   (mark **file**) value: `zip file containing .htm file`

p.s for this you can create for example **hello.htm** file with content: 

```
<!DOCTYPE html>
<html>
  <body>
    Hello, world!
  </body>
</html>
```


then compress as zip and you can upload this **hello.zip** file


**11. POST /api/v1/charts/email**

In postman create new request, **Authorization**: mark **Bearer** token and paste **cp_access_token**'s **value** from checkpoint.ci.thomsonreuters.com

In **Request Body**, mark **form_data**

**1. emailRequest** (mark **text**) value:
    

```
{
  "emailType": "Standard",
  "recipients": "nika.ozashvili@epam.com, nozas18@freeuni.edu.ge",
  "userEmail": "nika.ozashvili@thomsonreuters.com",
  "bccRecipients": "nikushaozashvili@gmail.com",
  "subject": "Test Chart Email",
  "attachmentFormat": "pdf",
  "attachmentName": "hello",
  "message": "Here is your chart data.",
  "disclaimerType": "DEFAULT",
  "userDisclaimer": "",
  "saveDisclaimer": false,
  "selectedText": ""
}
```


**2. files**   (mark **file**) value: `zip file containing .htm file`
p.s for this you can create for example **hello.htm file** with content: 

```
<!DOCTYPE html>
<html>
  <body>
    Hello, world!
  </body>
</html>
```


then compress as zip and you can upload this **hello.zip** file
