# Module03 Query Profiling

## Query

The query counts orders by status for orders placed from 1 June 2025:

```sql
SELECT
    status,
    COUNT(*) AS order_count
FROM orders
WHERE ordered_on >= '2025-06-01'
GROUP BY status;