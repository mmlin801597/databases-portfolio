# Module 3 — Reproducible Index Benchmark

## Method

`bench.py` creates four fresh databases from `setup.sql`, adds at most one index to each comparison database, then measures the dashboard aggregate five times per variant in interleaved order. Each timed query fetches all result rows. The script reports the median and `EXPLAIN QUERY PLAN`; it does not touch `warehouse.db`. Values below are one run on this machine, so they are observations rather than portable performance guarantees.

## Measured results

| Variant | Runs (ms) | Median (ms) | Plan uses added index? |
|---|---|---:|---|
| Baseline | 122.201, 103.376, 107.483, 102.458, 108.534 | 107.483 | No |
| `ix_orders_ordered_on` | 157.430, 111.307, 104.429, 102.336, 104.418 | 104.429 | No |
| `ix_orderline_product` | 130.276, 126.121, 107.507, 104.000, 104.029 | 107.507 | No |
| `ix_orderline_order` | 122.495, 103.756, 104.222, 102.311, 102.622 | 103.756 | No |

All four plans scanned `ol`, searched `orders`, `customer`, and `product` by their integer primary keys, and used temporary B-trees for grouping, `COUNT(DISTINCT)`, and ordering. The added indexes did not change this plan. The small timing differences and slower first samples show variation in this short local benchmark; the measurements do not support claiming a meaningful speedup or slowdown.

## Reproduction

Run `python Module03/bench.py` from the repository root. The script prints the measured values and plans. These results came from the successful run after correcting the fixture's damaged city-name characters.
