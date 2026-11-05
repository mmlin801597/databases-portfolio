# Module03 Task 4 — One Query, from Algebra to Plan

## SQL Query

The dashboard query from Task 1 calculates the number of distinct customers and total revenue for each city for orders placed in 2025.

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
```

## Relational Algebra

The query can be represented as:

```text
γ city;
  COUNT(DISTINCT customer_id) → customers,
  SUM(qty × price) → revenue
(
  σ 2025-01-01 ≤ ordered_on < 2026-01-01
  (
    customer
    ⋈ customer.customer_id = orders.customer_id orders
    ⋈ orders.order_id = order_line.order_id order_line
    ⋈ order_line.product_id = product.product_id product
  )
)
```

The main relational algebra operations are:

- **σ (selection):** filters orders to those placed in 2025.
- **⋈ (join):** connects `customer`, `orders`, `order_line`, and `product`.
- **γ (grouping/aggregation):** groups the result by city and calculates the number of customers and total revenue.
- **π (projection):** the final result contains `city`, `customers`, and `revenue`. The SQL `SELECT` clause performs this projection.

## Confirmation

The SQL matches the relational algebra.

The SQL `WHERE` clause corresponds to **σ**, the `JOIN` clauses correspond to **⋈**, and the `GROUP BY` with `COUNT` and `SUM` corresponds to **γ**. The `SELECT` clause corresponds to **π**.

Therefore, the SQL query and the relational algebra expression describe the same logical operation.