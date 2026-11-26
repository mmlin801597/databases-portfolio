# Module04 — Task 3: Trigger Cost Measurement

## Method

`benchmark_triggers.py` creates a fresh in-memory database from `setup.sql` for each sample. It inserts 10,000 valid vibration readings with and without `trg_vib_alarm`, alternates configuration order over five paired runs, and reports medians. The existing `edge.db` is never opened or changed.

## Measured results

| Configuration | Runs (ms) | Median (ms) | Alarm rows |
|---|---|---:|---:|
| Without trigger | 12.041, 12.320, 14.011, 11.726, 12.083 | 12.083 | 0 |
| With trigger | 31.971, 31.615, 31.506, 38.529, 31.078 | 31.615 | 10,000 |

In this run the trigger added about **19.532 ms** to the median batch time. It correctly created one alarm for each above-threshold vibration row. This is a local measurement, not a general performance guarantee.

Reproduce with `python Module04/benchmark_triggers.py` from the repository root.

## Screenshot Evidence

`task3-triggers.png` is a separate visual demonstration of trigger behavior; these timings are from the reproducible script above.
