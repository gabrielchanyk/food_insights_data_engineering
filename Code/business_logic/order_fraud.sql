-- =========================================================
-- ORDER FRAUD DETECTION DASHBOARD
-- Compatible with: Amazon Athena (Presto SQL)
-- Author: Gabriel Chan
-- Description: Identify potential fraud orders (>= $500 AND cancelled)
--              and detect which regions have the most cases
-- =========================================================


-- =========================================================
-- 1. FRAUD ORDERS BY REGION (past 7 days)
-- =========================================================
-- Detects all cancelled orders with total_order_cost >= $500
-- and aggregates them by restaurant region.
-- =========================================================

SELECT
    r.location AS region,
    COUNT(o.order_id) AS suspected_fraud_orders,
    SUM(o.total_order_cost) AS total_fraud_value,
    ROUND(AVG(o.total_order_cost), 2) AS avg_fraud_order_value
FROM
    "Order" o
JOIN
    "Menu" m ON o.menu_id = m.menu_id
JOIN
    "Restarant" r ON m.restaurant_id = r.restaurant_id
WHERE
    o.total_order_cost >= 500
    AND lower(o.status) = 'cancelled'
    AND o.order_date >= current_timestamp - INTERVAL '7' DAY
GROUP BY
    r.location
ORDER BY
    suspected_fraud_orders DESC;


-- =========================================================
-- 2. FRAUD RATE BY REGION
-- =========================================================
-- Compares high-value cancelled orders to total orders
-- to show which regions have the highest fraud ratio.
-- =========================================================

WITH total_orders AS (
    SELECT
        r.location AS region,
        COUNT(o.order_id) AS total_orders
    FROM
        "Order" o
    JOIN
        "Menu" m ON o.menu_id = m.menu_id
    JOIN
        "Restarant" r ON m.restaurant_id = r.restaurant_id
    WHERE
        o.order_date >= current_timestamp - INTERVAL '7' DAY
    GROUP BY
        r.location
),
fraud_orders AS (
    SELECT
        r.location AS region,
        COUNT(o.order_id) AS fraud_orders
    FROM
        "Order" o
    JOIN
        "Menu" m ON o.menu_id = m.menu_id
    JOIN
        "Restarant" r ON m.restaurant_id = r.restaurant_id
    WHERE
        o.total_order_cost >= 500
        AND lower(o.status) = 'cancelled'
        AND o.order_date >= current_timestamp - INTERVAL '7' DAY
    GROUP BY
        r.location
)
SELECT
    t.region,
    t.total_orders,
    COALESCE(f.fraud_orders, 0) AS fraud_orders,
    ROUND(CAST(COALESCE(f.fraud_orders, 0) AS DOUBLE) / t.total_orders * 100, 2) AS fraud_rate_percent
FROM
    total_orders t
LEFT JOIN
    fraud_orders f ON t.region = f.region
ORDER BY
    fraud_rate_percent DESC NULLS LAST;


-- =========================================================
-- 3. HIGH-VALUE CANCELLED ORDER DETAILS (for investigation)
-- =========================================================
-- Provides detailed view of all high-value cancelled orders
-- useful for fraud review and pattern analysis.
-- =========================================================

SELECT
    o.order_id,
    c.name AS customer_name,
    c.email AS customer_email,
    r.name AS restaurant_name,
    r.location AS region,
    o.total_order_cost,
    o.price,
    o.taxes,
    o.tip,
    o.status,
    o.order_date
FROM
    "Order" o
JOIN
    "Menu" m ON o.menu_id = m.menu_id
JOIN
    "Restarant" r ON m.restaurant_id = r.restaurant_id
JOIN
    "Customer" c ON o.customer_id = c.customer_id
WHERE
    o.total_order_cost >= 500
    AND lower(o.status) = 'cancelled'
    AND o.order_date >= current_timestamp - INTERVAL '7' DAY
ORDER BY
    o.total_order_cost DESC
LIMIT 100;