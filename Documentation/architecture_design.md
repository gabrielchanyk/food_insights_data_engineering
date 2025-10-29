# 🏗️ Architecture Design

## 📑 Table of Contents

- [Architecture Design](#🏗️-architecture-design)
- [Overall Assumptions](#⚙️-overall-assumptions)
- [Data Source Insights](#📦-data-source-insights)
- [Core Data Domain Requirements](#📊-core-data-domain-requirements)

---

![Architecture Diagram](/Diagrams/architecture.png)

---

# ⚙️ Overall Assumptions

- Collaborating with **courier partners** to develop clear and standardized **data contracts**.
- Establishing **Service Level Agreements (SLAs)** with couriers for data delivery and reliability (“signing” a contract).
- **Menu item names may vary** across platforms — **mapping and normalization** may be required.
- All **currency is standardized to USD**.
- There is currently **no centralized data architecture** — analysts are directly querying operational data sources for BI analytics.
- Data sources need to be ingested based on **refresh rates**

---

## 📦 Data Source Insights

| Data Source   | Type & Format                             | Key Data Elements                                           | Refresh / Ingestion         |
| ------------- | ----------------------------------------- | ----------------------------------------------------------- | --------------------------- |
| **QuickBite** | REST API (JSON payloads)                  | Orders, deliveries, customer actions, frequent menu updates | Near real-time              |
| **MealDash**  | SFTP (Daily CSV + YAML)                   | Revenue, transactions, customer feedback, menu data         | Daily                       |
| **FoodNow**   | Kafka event streams + XML partner reports | Driver statuses, delivery tracking, promotions              | Streaming + Scheduled batch |

---

## 📊 Core Data Domain Requirements

All courier platforms must contain, at minimum, the following data domains for proper integration and analysis:

- **Customer information**
- **Transaction and revenue data**
- **Menu and restaurant details**
- **Delivery and courier tracking**
- **Promotions and campaign data**

🔙 [Back to Main README](/README.md)
