# 📊 Exploratory Analysis for BI Revenue

## Overview

This project provides **exploratory business intelligence (BI) dashboards** for _InsightEats_, focusing on **revenue analytics**, **fraud detection**, and **menu optimization**.

### Why Grafana?

Grafana is the best fit for InsightEats because it offers:

- ⚡ **Real-time dashboards** for ingestion pipelines and delivery events
- 🔗 **Multi-source integration** (Amazon Redshift, Kafka, CloudWatch)
- 🚨 **Built-in alerting** for quick insights on abnormalities
- 🧩 **Flexible data manipulation** and visualization options

---

## 📈 Dashboards

### **1. Revenue per Region**

Visualizes total revenue distribution across different regions.

![Revenue Dashboard](/Diagrams/analysis_dashboard.png)

🔗 [View SQL Logic → `/Code/business_logic/regionalrevenue.sql`](/Code/business_logic/regionalrevenue.sql)

---

### **2. Order Fraud Detection**

Detects potentially fraudulent orders (≥ $500) and highlights affected regions.

![Fraud Detection](/Diagrams/fraud_detection.png)

🔗 [View SQL Logic → `/Code/business_logic/order_fraud.sql`](/Code/business_logic/order_fraud.sql)

---

### **3. Menu Item Optimization**

Analyzes performance across menu categories (e.g., beverages, mains, appetizers) to identify optimization opportunities.

![Menu Optimization](/Diagrams/menu_optimization.png)

🔗 [View SQL Logic → `/Code/business_logic/menu_item_optimization.sql`](/Code/business_logic/menu_item_optimization.sql)

---
