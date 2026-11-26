"""Reproduce the status/date profiling plans without touching warehouse.db."""
from pathlib import Path
import sqlite3

ROOT = Path(__file__).resolve().parent
SETUP = (ROOT / "setup.sql").read_text(encoding="utf-8")
QUERY = "SELECT status, COUNT(*) AS order_count FROM orders WHERE ordered_on >= '2025-06-01' GROUP BY status"
with sqlite3.connect(":memory:") as conn:
    conn.executescript(SETUP)
    print("before index plan:", " | ".join(r[3] for r in conn.execute("EXPLAIN QUERY PLAN " + QUERY)))
    print("result counts before:", conn.execute(QUERY + " ORDER BY status").fetchall())
    conn.execute("CREATE INDEX idx_orders_ordered_on ON orders(ordered_on)")
    print("after index plan:", " | ".join(r[3] for r in conn.execute("EXPLAIN QUERY PLAN " + QUERY)))
    print("result counts after:", conn.execute(QUERY + " ORDER BY status").fetchall())
