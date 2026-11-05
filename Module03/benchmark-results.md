# Module03 Task 2 — Index Benchmark

## Baseline — No Additional Indexes

### Dashboard Query

Runs:

- 102.631 ms
- 96.950 ms
- 96.296 ms

Median: **96.950 ms**

### Single-Day Query

Runs:

- 0.701 ms
- 0.136 ms
- 0.106 ms

Median: **0.136 ms**

The first run was slower because the database file was being loaded into the cache. Therefore, the median is used for comparison.

## Single-Day Lookup

### Before `ix_orders_ordered_on`

Plan:

```text
|--SCAN o
`--SEARCH c USING INTEGER PRIMARY KEY (rowid=?)
```

Median: **2.459 ms**

### After `ix_orders_ordered_on`

Runs:

- 0.753 ms
- 0.208 ms
- 0.198 ms

Median: **0.208 ms**

Plan:

```text
|--SEARCH o USING INDEX ix_orders_ordered_on (ordered_on=?)
`--SEARCH c USING INTEGER PRIMARY KEY (rowid=?)
```

The index reduced the median execution time from **2.459 ms to 0.208 ms**, showing a strong improvement for the selective single-day lookup.

## Index Usefulness — `ix_orderline_product`

For the dashboard query, `ix_orderline_product` was not useful because SQLite reaches the `product` table using the product primary key.

However, a query that directly filters `order_line.product_id` uses the index.

### Before the Index

```text
SCAN order_line
```

### After the Index

```text
SEARCH order_line USING INDEX ix_orderline_product (product_id=?)
```

This proves that `ix_orderline_product` is useful for queries that directly filter `order_line.product_id`. However, it does not help the dashboard query because the dashboard reaches the product table through its primary key.

## Final Summary

| Test | Result | Conclusion |
|---|---|---|
| Baseline dashboard | Median 96.950 ms | Full scan of `order_line` |
| `ix_orders_ordered_on` | Dashboard median 86.266 ms; plan unchanged | Small timing improvement, but SQLite did not use the index for the dashboard |
| `ix_orderline_order` | Dashboard became much slower | Index changed the plan but hurt performance |
| `ix_orderline_product` | Dashboard did not use it | Not useful for this dashboard query |
| Single-day lookup | 2.459 ms → 0.208 ms | Strong improvement for selective date lookup |
| Direct `product_id` filter | `SCAN order_line` → `SEARCH order_line USING INDEX` | Useful for this specific query |

## Conclusion

The benchmark shows that indexes do not automatically make every query faster. Their usefulness depends on the query and the amount of data being searched. The single-day lookup clearly benefited from `ix_orders_ordered_on`, reducing the median execution time from **2.459 ms to 0.208 ms**. In contrast, the aggregate dashboard query remained expensive and became much slower with `ix_orderline_order`. The `ix_orderline_product` index was not useful for the dashboard, but it was useful for a query that directly filtered `order_line.product_id`.