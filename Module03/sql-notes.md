# Module03 SQL Curiosities

## Curiosity 1 — Temporary B-tree

**Source:** `Module03/profile.sql`

```text
USE TEMP B-TREE FOR GROUP BY
USE TEMP B-TREE FOR ORDER BY
```

**Question:** Why does SQLite need a temporary B-tree for grouping and ordering?

---

## Curiosity 2 — Correlated Subquery

**Source:** `Module03/task5-window-subquery.md`

```sql
SELECT COUNT(*)
FROM orders o
WHERE o.customer_id = c.customer_id
  AND o.status = 'late';
```

**Question:** Why can this become expensive when there are many customers?

---

## Curiosity 3 — Window Function

**Source:** `Module03/task5-window-subquery.md`

```sql
COUNT(*) OVER (PARTITION BY customer_id)
```

**Question:** Why does the window-function query use several co-routines in the execution plan?

---

## Curiosity 4 — Index Made the Query Slower

**Source:** `Module03/benchmark-results.md`

The `ix_orderline_order` index changed the execution plan but made the dashboard query much slower.

**Question:** Why can adding an index make a query slower instead of faster?

---

## Curiosity 5 — SQL Injection

**Source:** `Module03/injection_demo.py`

```text
' OR '1'='1
```

**Question:** Why does this input change the meaning of the SQL query when string concatenation is used, but not when a bound parameter is used?