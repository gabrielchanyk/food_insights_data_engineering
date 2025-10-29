# 🔍 Data Exploration & Discovery

## 📑 Table of Contents

- [Data Contract / Template](#📄-data-contract--template)
  - [QuickBite Data Contract](#🗂️-quickbite-data-contract)
  - [FoodNow Data Contract](#🗂️-foodnow-data-contract)
  - [MealDash Data Contract](#🗂️-mealdash-data-contract)
    - [Sample MealDash Data Contract (JSON)](#sample-mealdash-data-contract-json)
    - [Sample MealDash Data Schema (JSON)](#sample-mealdash-data-schema-json)
- [Full Files](#📂-full-files)

## 📄 Data Contract / Template

| Field                      | Description                                                         | Example                                                 |
| -------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------- |
| **Data Source Name**       | Name of the partner or system providing the data                    | QuickBite                                               |
| **Data Owner**             | Contact person or team responsible for data accuracy                | data-team@quickbite.com                                 |
| **Contract Version**       | Version number of the data contract                                 | v1.2                                                    |
| **Effective Date**         | When this contract takes effect (useful for updates or if outdated) | 2025-10-26                                              |
| **Data Refresh Frequency** | How often data is delivered                                         | Near real-time / Daily / Hourly                         |
| **Delivery Method**        | How the data is provided                                            | REST API, SFTP, Kafka, Pub/Sub, etc.                    |
| **Connection Information** | Credentials or authentication details                               | OAuth 2.0                                               |
| **Data Schema**            | Used for validations and monitoring of data                         | `json { "orderNumber": "int", "orderName": "string" } ` |

---

## 🗂️ QuickBite Data Contract

| Contract Field             | Data Source Information            |
| -------------------------- | ---------------------------------- |
| **Data Source Name**       | QuickBite                          |
| **Data Owner**             | QuickBite API contact@gmail.com    |
| **Contract Version**       | v1.0                               |
| **Effective Date**         | Oct 30, 2025                       |
| **Data Refresh Frequency** | Near real-time                     |
| **Delivery Method**        | REST API with JSON payloads        |
| **Connection Information** | API key/token                      |
| **Data Schema**            | Will not go further for case study |

---

## 🗂️ FoodNow Data Contract

| Contract Field             | Data Source Information            |
| -------------------------- | ---------------------------------- |
| **Data Source Name**       | FoodNow                            |
| **Data Owner**             | FoodNow_kafka contact@gmail.com    |
| **Contract Version**       | v1.0                               |
| **Effective Date**         | Oct 30, 2025                       |
| **Data Refresh Frequency** | Kafka event stream (event-based)   |
| **Delivery Method**        | Kafka                              |
| **Connection Information** | Kafka servers with SSL/TLS keys    |
| **Data Schema**            | Will not go further for case study |

---

## 🗂️ MealDash Data Contract

| Contract Field             | Data Source Information                       |
| -------------------------- | --------------------------------------------- |
| **Data Source Name**       | MealDash                                      |
| **Data Owner**             | mealdash_csv@gmail.com                        |
| **Contract Version**       | v1.0                                          |
| **Effective Date**         | Oct 30, 2025                                  |
| **Data Refresh Frequency** | Daily                                         |
| **Delivery Method**        | CSV + YAML files                              |
| **Connection Information** | SFTP (passwordless or username/password auth) |
| **Data Schema Reference**  | mealdash_schema_v1.json                       |

### Sample MealDash Data Contract (JSON)

```json
{
  "data_source_name": "MealDash",
  "data_owner": "mealdash_csv@gmail.com",
  "contract_version": "v1.0",
  "effective_date": "2025-10-30",
  "data_refresh_frequency": "daily",
  "delivery_method": "CSV + YAML files",
  "connection_information": {
    "protocol": "SFTP",
    "authentication_methods": ["passwordless", "username_password"],
    "notes": "Preferred method: SSH key-based (passwordless).",
    "host": "sftp.mealdash.com",
    "username": "ftp_user",
    "password_secret_name": "ftp-password-secret",
    "file_path": "/path/to/data.csv",
    "s3_destination": "s3://my-bucket/ftp_data/"
  },
  "data_schema_reference": "order_schema.json",
  "description": "Daily delivery of MealDash order, revenue, feedback, and menu data to InsightEats. Delivered via secure SFTP as CSV and YAML metadata files."
}
```

### Sample MealDash Data Schema (JSON)

```json
{
  "orders": [
    { "name": "order_id", "datatype": "bigint", "required": true },
    { "name": "menu_id", "datatype": "bigint", "required": true },
    { "name": "revenue_id", "datatype": "bigint", "required": true },
    { "name": "quantity", "datatype": "integer", "required": true },
    { "name": "price", "datatype": "double", "required": true },
    { "name": "promotion_id", "datatype": "bigint", "required": false }
  ]
}
```

### 📂 Full Files

#### Data Schema for Orders

- [Orders Data Schema](/Code/dag/schemas/order_schema.json)
- [Example of Full Data Schema](/Code/datacontract_schema.json)

#### Data Contract

- [Data Contract](/Code/dag/data_contract.json)

🔙 [Back to Main README](/README.md)
