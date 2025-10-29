# ⚠️ Failure Scenario

## 📑 Table of Contents

- [Failure Scenario](#️-failure-scenario)
  - [Failure Cases](#-failure-cases)
    - [QuickBite API — Malformed JSON](#-quickbite-api--malformed-json)
    - [MealDash — Corrupted CSV Upload](#-mealdash--corrupted-csv-upload)
    - [FoodNow — Kafka Stream Down for 30 Minutes](#-foodnow--kafka-stream-down-for-30-minutes)
  - [Monitoring Framework](#-monitoring-framework)
    - [Overview / Health Panel](#1-overview--health-panel)
    - [Airflow DAGs Panel](#2-airflow-dags-panel)
    - [AWS Batch Panel](#3-aws-batch-panel)
    - [AWS Fargate Panel](#4-aws-fargate-panel)
    - [AWS Kafka / MSK Panel](#5-aws-kafka--msk-panel)
    - [Alerts & Notifications Panel](#6-alerts--notifications-panel)

---

## 🚨 Failure Cases

### 🧩 QuickBite API — Malformed JSON

### 🧾 MealDash — Corrupted CSV Upload

**Detection:**

- Validation scripts or schema checks fail when JSON/CSV doesn’t match the defined data contract.
- Airflow task or AWS Batch job logs show schema mismatch errors or parsing failures.

**Resolution Scenarios:**

1. **Malformed/Corrupted File Represents a Structural Change**

   - Indicates a schema evolution.
   - Introduce **new schema versioning** via the data contract.
   - Coordinate updates with data producers to align field names and types.

2. **Intermittent Corruption or Malformed Records**
   - Schema remains valid; handle via **error catching and skipping logic**.
   - Use **schema inference** (AWS Glue / PySpark) where feasible to auto-detect fields.
   - Ensure faulty records are logged to an **error bucket (e.g., `s3://error-zone/`)**.
   - Notify producers and analysts for root cause follow-up.

---

### 📉 FoodNow — Kafka Stream Down for 30 Minutes

**Detection:**

- Kafka consumer lag increases.
- CloudWatch or MSK metrics show broker downtime or message ingestion stalls.

**Resolution:**

- If downtime is **expected behavior** (e.g., maintenance or throttling),  
  increase **timeouts** and set up **backoff retry logic**.
- If unexpected:
  - Trigger **alert via CloudWatch Alarms** or **Slack notifications**.
  - Attempt **graceful restart** of consumers or Fargate services.
  - Log downtime duration and message loss, if any, for SLA tracking.

---

![Failure Workflow](/Diagrams/failure-analysis.png)

> _Example failure handling workflow — from detection to alerting and remediation._

---

## 🧭 Monitoring Framework

### 1. Overview / Health Panel

**Purpose:** High-level visibility of all system components  
**Widgets:**

- **DAG Success Rate:** % of DAGs succeeded in the last 24h
- **Batch Jobs Status:** Pie chart (Succeeded / Failed / Running)
- **Fargate Task Health:** % of healthy vs. unhealthy tasks
- **Kafka Cluster Health:** Brokers up / down

---

### 2. Airflow DAGs Panel

**Widgets:**

- DAG Run Timeline (success/failure over time)
- Task Duration (average runtime per DAG)
- Retry Counts (per DAG/task)
- SLA Misses (count and list of missed SLAs)

**Alerts:**

- DAG failure
- SLA miss
- Task stuck > threshold duration

---

### 3. AWS Batch Panel

**Widgets:**

- Job Queue Length
- Job Status Distribution (Running / Failed / Succeeded)
- Job Duration Trend (average runtime)
- Compute Environment Utilization (vCPU & memory)

**Alerts:**

- Failed jobs
- Jobs stuck > threshold
- Under/over-utilized environments

---

### 4. AWS Fargate Panel

**Widgets:**

- Task Status (Running / Stopped / Failed)
- CPU & Memory Usage (per service/task)
- Network Traffic (in/out per task)
- Container Logs (recent errors/warnings)

**Alerts:**

- Task failures
- High CPU/memory usage
- Unhealthy container

---

### 5. AWS Kafka / MSK Panel

**Widgets:**

- Broker Health (CPU, memory, disk usage)
- Topic Throughput (messages in/out per second)
- Consumer Lag (per consumer group)
- Partition Status (under-replicated/offline)

**Alerts:**

- Broker down
- Consumer lag > threshold
- Disk usage > threshold
- Under-replicated partitions

---

### 6. Alerts & Notifications Panel

**Centralized alert visibility**

**Monitored Alerts:**

- DAG failures / SLA misses
- Batch job queue delays or failures
- Fargate unhealthy tasks
- Kafka consumer lag / broker issues

**Delivery Channels:**

- Email
- Slack

![Monitoring Dashboard](/Diagrams/monitoring.png)

> _Example centralized monitoring dashboard integrating Airflow, AWS Batch, Fargate, and MSK health metrics._

🔙 [Back to Main README](/README.md)
