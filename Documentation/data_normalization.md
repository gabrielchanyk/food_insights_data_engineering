# 🧮 Data Normalization

![Data Normalization](/Diagrams/data_normalization.png)

The following SQL example demonstrates how to use multiple menu categories (beverages, mains, appetizers) into tables for consistent pricing and analysis across all order types.

```sql
-- Data Normalization Query

-- Beverage Table

SELECT
    o.order_id,
    b.price,
    (oi.quantity * b.price) AS total,
    'beverage' AS category
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN beverages b ON oi.beverage_name = b.name

-- Main Table

SELECT
    o.order_id,
    m.price,
    (oi.quantity * m.price) AS total,
    'main' AS category
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN mains m ON oi.main_name = m.name

-- Appetizer Table

SELECT
    o.order_id,
    a.price,
    (oi.quantity * a.price) AS total,
    'appetizer' AS category
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN appetizers a ON oi.appetizer_name = a.name;
```
