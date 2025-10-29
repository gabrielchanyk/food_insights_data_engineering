# 🔎 Further Insights Needed

To improve data ingestion, monitoring, and business decisions, the following questions and considerations should be addressed:

### Data Ingestion & Contracts

- What is the **average quantity of data per load**?
  - Can be added as metadata in the **data contract** for capacity planning.
- What are the **actual fields present within each data source**?
  - Do we need all fields, or can we filter unnecessary ones?
- Is **historical data ingestion required**?
  - If yes, define scope and format.
- What is the **data retention period** for each source?
  - Useful for compliance and storage planning.

### Business & Monitoring Purpose

- What is the **true purpose of monitoring revenue, performance, and customer actions**?
  - For this case study, assume the goal is **time-to-insight** for faster and more efficient business decisions.
  - Example use cases:
    - Understanding the **core customer base demographic**.
    - Identifying **most-used promotions**.
    - Tracking performance trends to improve operational efficiency.

---

# 🚀 Future Implementations

- Develop a **working end-to-end data pipeline in AWS** using **mock food insights data**.
  - This will include ingestion, and transformation
  - Supports testing of schema enforcement, data contracts, and alerting.
