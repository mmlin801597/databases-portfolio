# Module03 Query Profiling

## Query

The query counts orders by status for orders placed from 1 June 2025:

```sql
SELECT status, COUNT(*) AS order_count
FROM orders
WHERE ordered_on >= '2025-06-01'
GROUP BY status;
```

## Observed plan and result

`profile_verify.py` runs the query on a fresh in-memory copy of `setup.sql`, before and after adding `idx_orders_ordered_on`. It prints `EXPLAIN QUERY PLAN` details and grouped counts. The current run reported a full `SCAN orders` before the index, then `SEARCH orders USING INDEX idx_orders_ordered_on (ordered_on>?)` afterward. The result counts were unchanged.

The index can narrow the date range, while SQLite still groups the qualifying orders by status. The selectivity of the date predicate matters: if most rows qualify, a table scan can be competitive. `benchmark-results.md` contains a separate interleaved benchmark for the dashboard query; those measurements do not quantify this profile query.

Reproduce with `python Module03/profile_verify.py` from the repository root. The script does not access `warehouse.db`.
