# Module 3 SQL Curiosities

## Curiosity 1 — Temporary B-tree

**Source:** `profile.sql`

```text
USE TEMP B-TREE FOR GROUP BY
USE TEMP B-TREE FOR ORDER BY
```

**Question:** Why does SQLite need a temporary B-tree for grouping and ordering?

## Curiosity 2 — Correlated Subquery

**Source:** `task5-window-subquery.md`

```sql
SELECT COUNT(*)
FROM orders o
WHERE o.customer_id = c.customer_id
  AND o.status = 'late';
```

**Question:** How does a correlated subquery's work grow with the number of outer rows, and when can an index change that cost?

## Curiosity 3 — Window Function

**Source:** `task5-window-subquery.md`

```sql
COUNT(*) OVER (PARTITION BY customer_id)
```

**Question:** Why does the window-function query use several co-routines in the execution plan?

## Curiosity 4 — Available Index Not Chosen

**Source:** `benchmark-results.md`

The four benchmark variants had the same plan, which scanned `order_line`; SQLite did not use the added indexes for this dashboard.

**Question:** Why might the planner prefer a line-table scan for this join and filter shape, and what does the index still cost in storage and writes?

## Curiosity 5 — SQL Injection

**Source:** `injection_demo.py`

```text
' OR '1'='1
```

**Question:** Why does this input change the meaning of SQL built by string concatenation but remain data when passed as a bound parameter?

## Personal and class discussion evidence — TODO

Record which curiosity you investigated, what you can now explain, what remains unclear, and a question you actually raised in class. No discussion history is inferred from these prompts.

## Short answers supported by the checked artifacts

- SQLite reports temporary B-trees when it needs temporary sorting/grouping structures for `GROUP BY`, `ORDER BY`, or a window partition. They are not persistent schema objects.
- A correlated subquery refers to an outer-row value and can be evaluated repeatedly. The current fixture's plan and automatic-index decisions are captured by `task5_verify.py`; index benefit should be measured on the intended row distribution.
- A window function computes an aggregate across a partition while preserving each qualifying input row. The row-number filter is needed to return one row per customer.
- An available index is not automatically selected. The Module 3 dashboard plan starts from `order_line`, and the tested added indexes did not alter that plan. Indexes also consume pages and add maintenance work on writes.
- Bound parameters transmit the payload as a value, so SQL operators in that value do not become part of the statement syntax. `injection_demo.py` contrasts the vulnerable concatenated query with the parameterized form.
