# 🗄️ Data Modeling

## 📑 Table of Contents

- [Courier Platforms & Key Data Domains](#📌-courier-platforms--key-data-domains)
- [ERD Diagram](#🖼️-erd-diagram)
- [Order Table](#order-table)
- [Menu Table](#menu-table)
- [Revenue Table](#revenue-table)
- [Delivery Table](#delivery-table)

---

## 📌 Courier Platforms & Key Data Domains

- **QuickBite:** Orders, deliveries, customer actions, frequent menu updates
- **MealDash:** Revenue, transactions, customer feedback, menu data
- **FoodNow:** Driver statuses, delivery tracking, promotions

**Assumption:**  
All courier platforms must include **customer information, transaction/revenue data, menu information, delivery tracking, restaurant, and promotions** to function correctly.  
_Think of real-world examples like Instacart, UberEats, DoorDash._

---

## 🖼️ ERD Diagram

![Data Model](/Diagrams/data-model.png)

---

## 📦 Tables

### Order Table

| Name             | Datatype      | Description                                                    |
| ---------------- | ------------- | -------------------------------------------------------------- |
| order_id         | UUID          | Unique identifier for each order                               |
| menu_id          | UUID          | Identifier referencing the menu item associated with the order |
| revenue_id       | UUID          | Foreign key linking to the corresponding revenue record        |
| quantity         | INTEGER       | Number of units of the menu item ordered                       |
| price            | DECIMAL(10,2) | Price per unit of the menu item at the time of order           |
| taxes            | DECIMAL(10,2) | Taxes applied to the order                                     |
| tip              | DECIMAL(10,2) | Customer tip amount                                            |
| total_order_cost | DECIMAL(10,2) | Total cost of the order (including taxes and tip)              |
| status           | STRING        | Status of the order: Active, Succeeded, or Cancelled           |
| promotion_id     | UUID          | Identifier referencing any promotion applied to the order      |

**Notes:**

- Useful for fraud detection (e.g., cancelled orders over $500).
- Helps track geographic areas for improvement and high-value transactions.
- Enables analysis of menu item popularity and updates over time.

---

### Menu Table

| Name          | Datatype      | Description                                                        |
| ------------- | ------------- | ------------------------------------------------------------------ |
| menu_id       | UUID          | Unique identifier for each menu item                               |
| name          | STRING        | Name of the menu item                                              |
| category      | STRING        | Category of the menu item (e.g., appetizer, main course, beverage) |
| description   | TEXT          | Detailed description of the menu item                              |
| price         | DECIMAL(10,2) | Price of the menu item                                             |
| availability  | BOOLEAN       | Indicates whether the menu item is currently available             |
| restaurant_id | UUID          | Identifier referencing the restaurant offering the item            |

---

### Revenue Table

| Name              | Datatype      | Description                                                     |
| ----------------- | ------------- | --------------------------------------------------------------- |
| order_id          | UUID          | Unique identifier referencing the associated order              |
| platform_name     | STRING        | Name of platform to track revenue sources                       |
| amount            | DECIMAL(10,2) | Total revenue generated from the order before fees              |
| platform_fee      | DECIMAL(10,2) | Fee charged by the delivery platform for processing the order   |
| restaurant_payout | DECIMAL(10,2) | Net amount paid to the restaurant after deducting platform fees |

**Notes:**

- Provides insights into how much each platform is making overall.

---

### Delivery Table

| Name             | Datatype      | Description                                                            |
| ---------------- | ------------- | ---------------------------------------------------------------------- |
| delivery_id      | UUID          | Unique identifier for each delivery                                    |
| driver_id        | UUID          | Identifier for the driver assigned to the delivery                     |
| status           | STRING        | Current status of the delivery (e.g., pending, in_transit, delivered)  |
| current_location | JSON          | Real-time location of the driver or delivery, typically in coordinates |
| distance         | DECIMAL(10,2) | Distance traveled for the delivery, in kilometers or miles             |
| time_taken       | INT           | Total time taken for delivery (e.g., minutes or seconds)               |

**Notes:**

- Useful for optimizing delivery routes and tracking driver performance.

[back to main](/README.md)
