-- =========================================================
-- ORDER ANALYTICS DASHBOARD QUERIES
-- Compatible with: Amazon Athena (Presto SQL)
-- Author: Gabriel Chan
-- Description: Revenue, Orders, and Menu Insights based on ERD schema
-- =========================================================

-- =========================================================
-- 1. TOTAL REVENUE BY REGION (last 24 hours)
-- =========================================================
-- Summarizes total revenue by restaurant location (region)
-- and restaurant name (partner) over the past 24 hours.
-- =========================================================

SELECT
    r.location AS region,
    r.name AS partner,
    SUM(rv.amount) AS revenue
FROM
    "Order" o
JOIN
    "Revenue" rv ON o.order_id = rv.order_id
JOIN
    "Menu" m ON o.menu_id = m.menu_id
JOIN
    "Restarant" r ON m.restaurant_id = r.restaurant_id
WHERE
    o.order_date >= current_timestamp - INTERVAL '24' HOUR
GROUP BY
    r.location, r.name
ORDER BY
    revenue DESC;


-- =========================================================
-- 2. ORDERS BY REGION (last 1 hour)
-- =========================================================
-- Counts total orders placed by restaurant location (region)
-- within the last hour.
-- =========================================================

SELECT
    r.location AS region,
    COUNT(o.order_id) AS order_count
FROM
    "Order" o
JOIN
    "Menu" m ON o.menu_id = m.menu_id
JOIN
    "Restarant" r ON m.restaurant_id = r.restaurant_id
WHERE
    o.order_date >= current_timestamp - INTERVAL '1' HOUR
GROUP BY
    r.location
ORDER BY
    order_count DESC;


-- =========================================================
-- 3. TOP-SELLING MENU ITEMS BY REGION (last 7 days)
-- =========================================================
-- Identifies the most frequently ordered menu items
-- per restaurant region for the last 7 days.
-- =========================================================

SELECT
    r.location AS region,
    m.name AS item_name,
    SUM(o.quantity) AS total_quantity
FROM
    "Order" o
JOIN
    "Menu" m ON o.menu_id = m.menu_id
JOIN
    "Restarant" r ON m.restaurant_id = r.restaurant_id
WHERE
    o.order_date >= current_timestamp - INTERVAL '7' DAY
GROUP BY
    r.location, m.name
ORDER BY
    total_quantity DESC
LIMIT 20;


-- =========================================================
-- 4. TOP-SELLING CATEGORIES
-- =========================================================
-- Shows which menu categories generate the most orders
-- and revenue, including average menu price.
-- =========================================================

SELECT
    m.category AS category,
    COUNT(o.order_id) AS total_orders,
    SUM(rv.amount) AS total_revenue,
    AVG(m.price) AS average_price
FROM
    "Order" o
JOIN
    "Menu" m ON o.menu_id = m.menu_id
JOIN
    "Revenue" rv ON o.order_id = rv.order_id
GROUP BY
    m.category
ORDER BY
    total_revenue DESC;

