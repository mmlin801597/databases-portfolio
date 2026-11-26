import csv
import argparse
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description="Idempotently ingest the Module 4 readings CSV")
parser.add_argument("--db", type=Path, default=ROOT / "edge.db", help="SQLite database path")
parser.add_argument("--csv", type=Path, default=ROOT / "readings.csv", help="input CSV path")
args = parser.parse_args()

UPSERT_SQL = """
INSERT INTO reading(sensor_id, ts, value, interval_s)
VALUES (?, ?, ?, ?)
ON CONFLICT(sensor_id, ts)
DO UPDATE SET value = excluded.value
WHERE reading.value IS NOT excluded.value;
"""

with sqlite3.connect(args.db) as conn:
    conn.execute("PRAGMA foreign_keys = ON")
    with args.csv.open(newline="", encoding="utf-8") as f:
        rows = csv.DictReader(f)

        data = [
            (
                int(row["sensor_id"]),
                row["ts"],
                float(row["value"]),
                int(row["interval_s"]),
            )
            for row in rows
        ]

        conn.executemany(UPSERT_SQL, data)

print(f"Processed {len(data)} readings.")
