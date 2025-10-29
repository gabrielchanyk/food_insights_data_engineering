# ⚙️ Pipeline Example

## 📑 Table of Contents

- [Data Ingestion](#-data-ingestion)
  - [REST API (JSON Format Input)](#-rest-api-json-format-input)
  - [Kafka (Streaming)](#-kafka-streaming)
  - [FTP (CSV or YAML)](#-ftp-csv-or-yaml)
  - [Pseudocode Overview](#-pseudocode-overview)
- [Data Transformation](#-data-transformation)
  - [DAG Workflow for Amazon Redshift / Athena](#-dag-workflow-for-amazon-redshift--athena)
- [Ingestion → Cleaning → Transformation Pipeline](#-ingestion--cleaning--transformation-pipeline)
- [Gold Zone DAG Pipeline](#-gold-zone-dag-pipeline)

---

## 🚀 Data Ingestion

Data ingestion is structured by **data source type**, with a dedicated system for each ingestion path:

- **REST API (JSON format)**
- **FTP (CSV or YAML)**
- **Kafka (Streaming)**

Schema drift and data consistency are managed through **Data Contracts** and **Schema Validation**.  
Files in JSON, CSV, or YAML format are ingested into **Amazon S3 (Data Lake)** as a first step, followed by schema registration in **AWS Glue Data Catalog**.  
For Kafka, the **AWS Glue Schema Registry** can be used to enforce schema evolution policies.

> 💡 _AWS Glue’s schema inference and validation features can also automate type detection and standardization._

---

## 🌐 REST API (JSON Format Input)

| Feature / Aspect          | **AWS Lambda**                                                           | **AWS Fargate**                                                        |
| ------------------------- | ------------------------------------------------------------------------ | ---------------------------------------------------------------------- |
| **Purpose**               | Event-driven serverless compute for short-lived functions                | Serverless container execution for continuous or long-running services |
| **Runtime Model**         | Executes code on demand (cold starts possible); max 15 min runtime       | Runs containerized apps continuously or per task; no time limit        |
| **API Hosting**           | Integrates with API Gateway for REST/HTTP endpoints                      | Integrates with ALB or API Gateway for container-based APIs            |
| **Performance & Latency** | Fast, but can experience cold starts                                     | Consistent performance; containers stay warm                           |
| **Scalability**           | Auto-scales per request (fine-grained)                                   | Auto-scales by task count based on load                                |
| **Workload Type**         | Lightweight, stateless, event-driven APIs                                | Persistent APIs or long-running microservices                          |
| **Execution Time Limit**  | 15 minutes max                                                           | No time limit                                                          |
| **Cost Considerations**   | Pay per request and execution time (cost-efficient for bursty workloads) | Pay per vCPU-second and GB-second (efficient for steady workloads)     |
| **Cold Start Behavior**   | Possible (100–300 ms latency)                                            | None once running                                                      |
| **Integration Options**   | S3, DynamoDB, Kinesis, EventBridge, Step Functions                       | ECS, ECR, RDS, ALB, CloudMap                                           |
| **Typical Workflow**      | API Gateway → Lambda → DynamoDB/S3/RDS                                   | ALB/API Gateway → ECS (Fargate) container → RDS/S3                     |
| **Best For**              | Short, bursty REST APIs, webhooks                                        | Persistent REST APIs, low-latency, near real-time APIs                 |

#### ✅ REST API Technology Decision: **AWS Fargate**

AWS Fargate is chosen for the REST API ingestion layer because it provides **always-on**, containerized compute with **low-latency** performance — essential for **near real-time workloads**.  
Unlike Lambda, Fargate containers are continuously active, avoiding cold starts and execution time limits.

---

## 🔄 Kafka (Streaming)

| Feature / Aspect        | **Amazon MSK**                          | **AWS Glue Streaming**                         |
| ----------------------- | --------------------------------------- | ---------------------------------------------- |
| **Primary Role**        | Real-time data ingestion & buffering    | Real-time ETL transformation & loading         |
| **Core Function**       | Managed Kafka message broker            | Managed Spark Streaming ETL                    |
| **Input / Output**      | Producers → Kafka Topics → Consumers    | Kafka/Kinesis → Transformed data → S3/Redshift |
| **Transformations**     | None (raw stream only)                  | Yes — cleansing, validation, joins             |
| **Schema Handling**     | Optional via Glue Schema Registry       | Native schema inference + validation           |
| **Latency**             | Sub-second                              | Seconds to minutes (micro-batch)               |
| **Durability / Replay** | Persistent retention & replay supported | No persistence                                 |
| **Scalability**         | Scales via Kafka partitions             | Scales by DPUs                                 |
| **Management Level**    | Managed Kafka cluster (topic control)   | Fully managed ETL jobs                         |
| **Integration**         | MSK Connect, Glue, Lambda, Firehose     | Direct output to Redshift, S3, DynamoDB        |
| **Pricing Model**       | Pay per broker-hour + storage           | Pay per DPU-hour                               |
| **Best Use Case**       | Continuous data ingestion & buffering   | Continuous / near real-time transformations    |
| **Pipeline Role**       | Ingest / Stream Layer                   | Transform / Load Layer                         |

#### ✅ Kafka Technology Decision: **Amazon MSK**

Amazon MSK is selected for **external Kafka ingestion** due to its **high durability**, **low latency**, and **tight integration with Redshift**.  
Business logic transformations can be **deferred** and handled later via **Amazon Athena**, optimizing both performance and cost.

---

## 📂 FTP (CSV or YAML)

| Feature / Aspect              | **Amazon EMR**                                 | **AWS Batch**                                       | **AWS Glue**                            |
| ----------------------------- | ---------------------------------------------- | --------------------------------------------------- | --------------------------------------- |
| **CSV Transformation**        | Spark/Hive for large-scale parallel processing | Containerized scripts; flexible execution           | Native ETL via PySpark                  |
| **Data Size Handling**        | Best for GB–TB scale                           | Best for MB–few GB                                  | Best for GB–TB scale                    |
| **Parallelism / Scalability** | Auto-distributes across nodes                  | Concurrent jobs via container tasks                 | Auto-parallelizes via DPUs              |
| **Incremental / Streaming**   | Spark Streaming available                      | Batch-only                                          | Glue Streaming available                |
| **Schema Handling**           | Automatic inference                            | Manual in code                                      | Inference + validation via Data Catalog |
| **Automation**                | Step Functions, EventBridge                    | Job Queues, EventBridge                             | Built-in scheduler and triggers         |
| **Cost Considerations**       | Pay for EC2 + EBS + EMR fees                   | Pay for compute time; cost-efficient for small jobs | Pay per DPU-hour; fully serverless      |
| **Typical Workflow**          | S3 → EMR → S3/Redshift                         | S3 → Batch job → S3/Redshift                        | S3 → Glue job → S3/Redshift             |

#### ✅ FTP (CSV or YAML) Technology Decision: **AWS Batch**

AWS Batch is ideal for **small-to-medium CSV workloads**. It is **cost-efficient**, **container-based**, and doesn’t require cluster or DPU management.  
Batch allows each CSV or YAML file to be processed independently in parallel jobs, integrating easily with **EventBridge** or **Step Functions** for scheduling.  
This approach is optimal for **daily ingestion pipelines** that require lightweight transformations with predictable cost.

---

## Overall Modularized Coding Structure

![coding_structure](/Diagrams/coding_structure.png)

---

## 🧩 Pseudocode Overview

JSON config-based ingestion:

- Validate schemas using data contracts.
- Reject any record or file failing schema checks before loading to target tables.

📁 **Related Files:**

- [AWS Batch Ingestion Folder](/Code/aws_batch)
- [AWS Batch Ingestion Python](/Code/aws_batch/aws_batch.py)
- [AWS Batch Ingestion Docker](/Code/aws_batch/Dockerfile)
- [AWS Batch Ingestion Requirements](/Code/aws_batch/requirements.txt)

---

## 🔄 Data Transformation

### 🧭 DAG Workflow for Amazon Redshift / Athena

- Using configurable YAML files with Amazon Redshift SQL queries to transform from raw to standardized data:
  - enforcing proper datatypes
  - applying true nulls
  - trimming whitespaces
- DAGS orchestrate ingestion → transformation pipelines while passing parameters dynamically.

📄 [AWS Athena SQL DAG](/Code/Transform_dag/transform.py)

---

## 🧱 Ingestion → Cleaning → Transformation Pipeline

Flow:
`INGEST → Cleaning DAG (AWS Batch) → ATHENA (Transform)`

📂 [DAG Dependency for MealDash](/Code/mealdash_ingest_clean_dag/)

- [DAG Python Code](/Code/mealdash_ingest_clean_dag/dag_code.py)
- [Orders Mapping YAML](/Code/mealdash_ingest_clean_dag/maps/orders_std.yaml)

---

## 🪙 Gold Zone DAG Pipeline

📂 [DAG Dependency for MealDash](/Code/transform_gold_dag/)

- [DAG Python Code](/Code/transform_gold_dag/dag_code.py)
- [Orders Mapping YAML](/Code/transform_gold_dag/maps/orders_gold.yaml)

🔙 [Back to Main README](/README.md)
