# 📊 Exploratory Analysis for BI Revenue

## 🧠 Overview

This project provides **exploratory business intelligence (BI) dashboards** for _InsightEats_, focusing on:

- 💰 **Revenue analytics**
- 🔍 **Fraud detection**
- 🍽️ **Menu optimization**

These dashboards enable both business and technical teams to gain actionable insights into performance, revenue trends, and operational health.

---

## ⚙️ Dashboard Platform Comparison

| **Feature / Aspect**          | **Amazon QuickSight**                                                                             | **Amazon Managed Grafana**                                                                                          |
| ----------------------------- | ------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Primary Use Case**          | Business intelligence, self-service analytics, executive dashboards                               | Operational monitoring, metrics tracking, time-series analysis, multi-source dashboards                             |
| **Audience**                  | Business analysts, management, marketing, product teams                                           | Operations teams, data engineers, SREs, real-time monitoring teams                                                  |
| **Data Sources**              | Redshift, RDS, S3, Athena, Salesforce, other BI sources                                           | Redshift, CloudWatch, Prometheus, Elasticsearch, multiple streaming sources                                         |
| **Data Latency**              | Batch / near real-time with SPICE caching                                                         | Real-time or near-real-time streams, live metrics                                                                   |
| **Dashboard Focus**           | Trend analysis, comparisons, KPI tracking, customer insights                                      | System health, delivery metrics, real-time orders, anomaly detection                                                |
| **Visualization Types**       | Bar charts, line charts, scatter plots, heat maps, pivot tables, KPI widgets                      | Line charts, gauges, heat maps, tables, alerts, annotations, composite dashboards                                   |
| **Interactivity**             | Filters, drill-downs, parameter controls, ad-hoc queries                                          | Time-range selectors, live-updating panels, annotations, alert triggers                                             |
| **AI/ML Integration**         | Connects to ML predictions via Redshift or SageMaker for forecasting/recommendations              | Limited AI/ML; primarily visualizes outputs of models or operational metrics                                        |
| **Alerting**                  | No native alerting (requires integration via API, email, or Slack)                                | Built-in alerting on thresholds, anomalies, or missing data                                                         |
| **Strengths for InsightEats** | Revenue trends, failed deliveries, top-selling categories, menu performance, executive dashboards | Real-time delivery tracking, driver performance, ingestion pipeline monitoring, anomaly detection on revenue/orders |
| **Recommended Scenarios**     | Historical reporting, BI dashboards for management, high-level metrics                            | Operational dashboards for engineering, live order tracking, and alerting                                           |

---

## 💡 Why Choose Grafana?

Grafana is the **recommended platform** for InsightEats because it provides:

- ⚡ **Real-time dashboards** for ingestion pipelines and delivery events
- 🔗 **Multi-source data integration** (Amazon Redshift, Kafka, CloudWatch)
- 🚨 **Built-in alerting** for anomalies and threshold breaches
- 🧩 **Flexible and dynamic visualizations** with customizable panels and queries

---

## 📈 Dashboards

### **1. Revenue per Region**

Visualizes total revenue distribution across geographic regions to identify high-performing markets.

![Revenue Dashboard](/Diagrams/analysis_dashboard.png)

🔗 [View SQL Logic → `/Code/business_logic/regionalrevenue.sql`](/Code/business_logic/regionalrevenue.sql)

---

### **2. Order Fraud Detection**

Detects potentially fraudulent orders (≥ $500) and highlights impacted regions for investigation.

![Fraud Detection](/Diagrams/fraud_detection.png)

🔗 [View SQL Logic → `/Code/business_logic/order_fraud.sql`](/Code/business_logic/order_fraud.sql)

---

### **3. Menu Item Optimization**

Analyzes menu category performance (beverages, mains, appetizers, etc.) to identify optimization opportunities and improve profitability.

![Menu Optimization](/Diagrams/menu_optimization.png)

🔗 [View SQL Logic → `/Code/business_logic/menu_item_optimization.sql`](/Code/business_logic/menu_item_optimization.sql)

---

🔙 [Back to Main README](/README.md)
