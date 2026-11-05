# Module03 Task 1 — LLM Query Plan

## Prompt

SQLite schema: `customer(customer_id, name, city)`, `product(product_id, sku, price)`, `orders(order_id, customer_id, ordered_on, status)`, `order_line(order_id, product_id, qty)`. Write a query that returns, for each city, the number of distinct customers and the total revenue (sum of `qty*price`) of orders placed in 2025, ordered by revenue descending.

## Predicted Query Plan

Before running the query, I predict that SQLite will:

- Scan the `customer` table.
- Search `orders` using the customer join.
- Search `order_line` using `order_id`.
- Search `product` using `product_id`.
- Possibly use temporary B-trees for `COUNT(DISTINCT ...)`, `GROUP BY`, and `ORDER BY`.

## LLM SQL

```sql
SELECT c.city,
       COUNT(DISTINCT c.customer_id) AS customers,
       SUM(ol.qty * p.price) AS revenue
FROM customer c
JOIN orders o
    ON o.customer_id = c.customer_id
JOIN order_line ol
    ON ol.order_id = o.order_id
JOIN product p
    ON p.product_id = ol.product_id
WHERE o.ordered_on >= '2025-01-01'
  AND o.ordered_on < '2026-01-01'
GROUP BY c.city
ORDER BY revenue DESC;