# Module03 Task 5 — Window Functions and Subquery Rewrite

## Grouped reference query

```sql
SELECT c.customer_id, c.name, COUNT(*) AS late_orders
FROM orders o JOIN customer c ON c.customer_id=o.customer_id
WHERE o.status='late'
GROUP BY c.customer_id, c.name
ORDER BY late_orders DESC;
```

This returns one row per customer with at least one late order.

## Correlated subquery, restricted to the same customer set

```sql
SELECT c.customer_id, c.name,
       (SELECT COUNT(*) FROM orders o
        WHERE o.customer_id=c.customer_id AND o.status='late') AS late_orders
FROM customer c
WHERE EXISTS (SELECT 1 FROM orders o
              WHERE o.customer_id=c.customer_id AND o.status='late')
ORDER BY late_orders DESC;
```

The `EXISTS` condition matters: without it, the correlated form returns customers with zero late orders while the grouped query omits them.

## Window version with one row per customer

```sql
SELECT customer_id, name, late_orders
FROM (
  SELECT c.customer_id, c.name,
         COUNT(*) OVER (PARTITION BY c.customer_id) AS late_orders,
         ROW_NUMBER() OVER (PARTITION BY c.customer_id ORDER BY o.order_id) AS rn
  FROM orders o JOIN customer c ON c.customer_id=o.customer_id
  WHERE o.status='late'
)
WHERE rn=1
ORDER BY late_orders DESC;
```

A window aggregate preserves input rows. `ROW_NUMBER()` plus `rn=1` reduces each customer's late orders to one output row. Run `python Module03/task5_verify.py` to compare result sets and capture current plans.

## Interpretation

The grouped query directly expresses the desired aggregation. The correlated form may repeat lookups per customer, while the window version processes the qualifying late-order rows and requires partitioning. The better choice depends on data, indexes, and the report's required row set. The original draft's claims about what an LLM produced are personal session evidence and should only be retained if confirmed from that session.

## Verified results and current plans

`task5_verify.py` ran the grouped, correlated, and one-row window queries against the generated fixture. Their sorted outputs were identical at **400 customer rows**.

Current plan summary from this workspace's SQLite:

- Grouped: scan orders, search customer by primary key, temporary B-tree for grouping.
- Correlated: scan customers, use an automatic partial covering index for the `EXISTS` predicate, then a correlated scalar subquery scan of orders.
- Window: co-routines for the derived query, scan orders, search customer by primary key, and temporary B-tree for window ordering.

Re-run the script when SQLite changes; the optimizer plan is version- and data-dependent.
