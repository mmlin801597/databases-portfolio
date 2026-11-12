# Module04 — Task 2: Idempotent Edge Ingestion

## UPSERT

The reading table uses `(sensor_id, ts)` as a natural key.

The UPSERT updates an existing reading when the same sensor and timestamp are replayed.

## Python Ingestion

The Python script uses `executemany()` with the same UPSERT statement.

The CSV was processed twice.

## Result

The CSV contains 3 readings.

After running the ingestion script twice, the database still contains:

**3 readings**

This proves that replayed readings were not duplicated.

The existing reading was updated from `41.7` to `42.0`.

## Evidence

- `ingest.py` — Python ingestion script
- `readings.csv` — test input
- `edge.db` — SQLite database
- Final row count: **3**