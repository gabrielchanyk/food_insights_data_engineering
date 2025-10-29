-- =========================================================
-- MENU ITEM OPTIMIZATION DASHBOARD
-- Compatible with: Amazon Athena (Presto SQL)
-- Author: Gabriel Chan
-- Description: Analyze top-performing menu items by category
--              (Appetizer, Beverage, Main, etc.)
-- =========================================================


-- =========================================================
-- 1. TOP-SELLING MENU ITEMS PER CATEGORY (last 30 days)
-- =========================================================
-- Shows the best-selling menu items per category based on
-- quantity sold and total revenue generated.
-- =========================================================

SELECT
    m.category AS category,
    m.name AS menu_item_name,
    r_rest.name AS restaurant_name,
    r_rest.location AS region,
    SUM(o.quantity) AS total_quantity_sold,
    SUM(rv.amount) AS total_revenue,
    ROUND(AVG(m.price), 2) AS average_unit_price
FROM
    "Order" o
JOIN
    "Menu" m ON o.menu_id = m.menu_id
JOIN
    "Revenue" rv ON o.order_id = rv.order_id
JOIN
    "Restarant" r_rest ON m.restaurant_id = r_rest.restaurant_id
WHERE
    o.order_date >= current_timestamp - INTERVAL '30' DAY
GROUP BY
    m.category, m.name, r_rest.name, r_rest.location
ORDER BY
    m.category ASC,
    total_quantity_sold DESC,
    total_revenue DESC;


-- =========================================================
-- 2. CATEGORY-LEVEL PERFORMANCE SUMMARY (last 30 days)
-- =========================================================
-- Summarizes overall performance of each category by
-- total orders, quantity, and revenue.
-- =========================================================

SELECT
    m.category AS category,
    COUNT(DISTINCT o.order_id) AS total_orders,
    SUM(o.quantity) AS total_items_sold,
    SUM(rv.amount) AS total_revenue,
    ROUND(AVG(m.price), 2) AS avg_item_price
FROM
    "Order" o
JOIN
    "Menu" m ON o.menu_id = m.menu_id
JOIN
    "Revenue" rv ON o.order_id = rv.order_id
WHERE
    o.order_date >= current_timestamp - INTERVAL '30' DAY
GROUP BY
    m.category
ORDER BY
    total_revenue DESC;


-- =========================================================
-- 3. TOP 3 MENU ITEMS PER CATEGORY (RANKED)
-- =========================================================
-- Uses a window function to rank items within each category
-- based on quantity sold, allowing you to see top performers.
-- =========================================================

WITH ranked_items AS (
    SELECT
        m.category,
        m.name AS menu_item_name,
        SUM(o.quantity) AS total_quantity_sold,
        SUM(rv.amount) AS total_revenue,
        ROW_NUMBER() OVER (
            PARTITION BY m.category
            ORDER BY SUM(o.quantity) DESC
        ) AS rank_within_category
    FROM
        "Order" o
    JOIN
        "Menu" m ON o.menu_id = m.menu_id
    JOIN
        "Revenue" rv ON o.order_id = rv.order_id
    WHERE
        o.order_date >= current_timestamp - INTERVAL '30' DAY
    GROUP BY
        m.category, m.name
)
SELECT
    category,
    menu_item_name,
    total_quantity_sold,
    total_revenue,
    rank_within_category
FROM
    ranked_items
WHERE
    rank_within_category <= 3
ORDER BY
    category, rank_within_category;