# Module03 Task 5 — Window Functions and Subquery Rewrite

## Original Query

The original report counts the number of late orders for each customer:

```sql
SELECT c.customer_id,
       c.name,
       COUNT(*) AS late_orders
FROM orders o
JOIN customer c
    ON c.customer_id = o.customer_id
WHERE o.status = 'late'
GROUP BY c.customer_id, c.name
ORDER BY late_orders DESC;
```

This query groups the late orders by customer and returns one row for each customer.

## 1. Correlated Subquery

```sql
SELECT c.customer_id,
       c.name,
       (
           SELECT COUNT(*)
           FROM orders o
           WHERE o.customer_id = c.customer_id
             AND o.status = 'late'
       ) AS late_orders
FROM customer c
ORDER BY late_orders DESC;
```

### Explanation

The outer query goes through the customers. For each customer, the correlated subquery counts the orders that belong to that customer and have the status `late`.

It is called a **correlated subquery** because the inner query uses `c.customer_id` from the outer query.

## 2. Window Function

```sql
SELECT customer_id,
       name,
       COUNT(*) OVER (PARTITION BY customer_id) AS late_orders
FROM (
    SELECT c.customer_id,
           c.name
    FROM orders o
    JOIN customer c
        ON c.customer_id = o.customer_id
    WHERE o.status = 'late'
)
ORDER BY late_orders DESC;
```

### Explanation

The inner query selects all late orders and their customers.

The window function:

```sql
COUNT(*) OVER (PARTITION BY customer_id)
```

counts the late orders for each customer without grouping the rows into a single row.

Therefore, a customer with several late orders appears several times in the result.

To produce the same one-row-per-customer result as the original query, an additional step is needed.

## Correct One-Row-Per-Customer Window Version

```sql
SELECT customer_id,
       name,
       late_orders
FROM (
    SELECT c.customer_id,
           c.name,
           COUNT(*) OVER (PARTITION BY c.customer_id) AS late_orders,
           ROW_NUMBER() OVER (
               PARTITION BY c.customer_id
               ORDER BY c.customer_id
           ) AS rn
    FROM orders o
    JOIN customer c
        ON c.customer_id = o.customer_id
    WHERE o.status = 'late'
)
WHERE rn = 1
ORDER BY late_orders DESC;
```

### Explanation

The `COUNT(*) OVER` calculates the number of late orders for each customer.

The `ROW_NUMBER()` function gives each row within the same customer a number. The outer query keeps only `rn = 1`, so only one row is returned for each customer.

This makes the window-function query produce the same type of result as the original query.

## Plan Comparison

### Correlated Subquery Plan

```text
QUERY PLAN
|--SCAN c
|--CORRELATED SCALAR SUBQUERY 1
|  `--SCAN o
`--USE TEMP B-TREE FOR ORDER BY
```

The plan shows that SQLite scans the `customer` table and then runs the correlated subquery for each customer. Inside the subquery, SQLite scans the `orders` table to find the customer's late orders.

Because there is no index on `orders.customer_id`, the `orders` table can be scanned repeatedly. This can become expensive as the number of customers grows.

### Window Function Plan

```text
QUERY PLAN
|--CO-ROUTINE (subquery-1)
|  |--CO-ROUTINE (subquery-3)
|  |  |--CO-ROUTINE (subquery-4)
|  |  |  |--SCAN o
|  |  |  |--SEARCH c USING INTEGER PRIMARY KEY (rowid=?)
|  |  |  `--USE TEMP B-TREE FOR ORDER BY
|  |  `--SCAN (subquery-4)
|  `|--SCAN (subquery-3)
|--SCAN (subquery-1)
`--USE TEMP B-TREE FOR ORDER BY
```

The window-function plan is more complex. SQLite uses several co-routines to process the subqueries and window functions. It also uses temporary B-trees for ordering.

Both queries scan the `orders` table, but they process the data differently. The correlated subquery repeatedly performs the inner query for each customer, while the window-function version processes the late-order rows using window functions.

## Readability Comparison

The **correlated subquery** is easier to read for this particular task because it directly expresses the requirement: for each customer, count their late orders.

The **window-function version** is more complex because it calculates the count while keeping the individual rows and then uses `ROW_NUMBER()` to return only one row per customer.

However, window functions are useful for more advanced analytical queries where we need to compare individual rows with values calculated over a group of rows.

| Method | Readability | Plan complexity |
|---|---|---|
| Correlated subquery | Easier | Simpler |
| Window function | More complex | More complex |

## Which Query Did the LLM Produce by Default?

The LLM produced the **correlated subquery** version by default.

This was a reasonable choice because the task only requires one late-order count for each customer. The correlated subquery is more direct and easier to understand for this report.

The window-function version is more useful when additional row-level analysis is required, but for this particular query, the correlated subquery is more readable.