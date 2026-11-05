.timer on

-- BEFORE INDEX
EXPLAIN QUERY PLAN
SELECT
    status,
    COUNT(*) AS order_count
FROM orders
WHERE ordered_on >= '2025-06-01'
GROUP BY status;

SELECT
    status,
    COUNT(*) AS order_count
FROM orders
WHERE ordered_on >= '2025-06-01'
GROUP BY status;

-- CREATE INDEX
CREATE INDEX IF NOT EXISTS idx_orders_ordered_on
ON orders(ordered_on);

-- AFTER INDEX
EXPLAIN QUERY PLAN
SELECT
    status,
    COUNT(*) AS order_count
FROM orders
WHERE ordered_on >= '2025-06-01'
GROUP BY status;

SELECT
    status,
    COUNT(*) AS order_count
FROM orders
WHERE ordered_on >= '2025-06-01'
GROUP BY status;