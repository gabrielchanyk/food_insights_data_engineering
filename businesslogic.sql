-- Total revenue by region
SELECT region, partner, SUM(total_amount) AS revenue
FROM orders
WHERE order_ts >= NOW() - INTERVAL '24 hours'
GROUP BY region, partner
ORDER BY revenue DESC;

-- Orders by region
SELECT region, COUNT(*) AS order_count
FROM orders
WHERE order_ts >= NOW() - INTERVAL '1 hour'
GROUP BY region
ORDER BY order_count DESC;

-- Top-selling menu items by region
SELECT region, menu_items.name AS item_name, SUM(items.qty) AS quantity
FROM orders
JOIN items ON orders.order_id = items.order_id
JOIN menu_items ON items.item_id = menu_items.menu_item_id
WHERE order_ts >= NOW() - INTERVAL '7 days'
GROUP BY region, item_name
ORDER BY quantity DESC
LIMIT 20;

--- top selling categories
SELECT
    m.category AS category,
    COUNT(o.order_id) AS total_orders,
    SUM(r.amount) AS total_revenue,
    AVG(m.price) AS average_price
FROM
    "Order" o
JOIN
    "Menu" m ON o.menu_id = m.menu_id
JOIN
    "Revenue" r ON o.order_id = r.order_id
GROUP BY
    m.category
ORDER BY
    total_revenue DESC;