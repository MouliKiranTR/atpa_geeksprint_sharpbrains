## 1. Description

## 2. Repository Link


- [GitHub Link](https://github.com/tr/cp_cm-classifier)

## 3. Libraries

- cptam-pycmclassifier
- cptam-pydata

## 4. Testing

### Unit Tests
- Run the test defined in the readme.txt file

### API Testing
Since there's no Swagger documentation available, the API can be tested manually using the following approach:

**Endpoint:** `POST /v1/cmclassify/{guid}`

**Environment URL:** 
```
https://cpa-dev-cpa-cm-classifier.tr-tax-cp-preprod.aws-int.thomsonreuters.com
```

**Sample Request:**
```http
POST https://cpa-dev-cpa-cm-classifier.tr-tax-cp-preprod.aws-int.thomsonreuters.com/v1/cmclassify/i688d46bb8dcdc656ac6eee89105f331b
Content-Type: application/json

{
    "practiceArea": "FEDERAL",
    "sections": [
        {
            "title": "Test",
            "type": "Section",
            "children": [
                {
                    "type": "Paragraph",
                    "text": "Deductions"
                }
            ]
        }
    ]
}
```

**Test GUID:** `i688d46bb8dcdc656ac6eee89105f331b`
> Note: This GUID exists in the database and can be used to verify successful database connectivity.

**Request Parameters:**
- `guid` (path parameter): Unique identifier for the classification request
- Request body: JSON object containing:
  - `practiceArea`: Practice area classification (e.g., "FEDERAL")
  - `sections`: Array of section objects with title, type, and children properties

## 5. Diagrams

- [Architecture diagram](https://lucid.app/lucidchart/9aeb4fc0-5c66-4039-b206-824c0a6d6ddd/edit?invitationId=inv_cd8a8f63-048d-47f2-a008-652ebb79f5ef&page=d4ohBGESoUUS#)

