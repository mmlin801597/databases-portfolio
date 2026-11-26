"""Capture EXPLAIN QUERY PLAN behavior for the Module 2 legacy fixture."""
from pathlib import Path
import sqlite3

ROOT = Path(__file__).resolve().parent.parent
LEGACY = ROOT / "Module02" / "legacy-schema.sql"
QUERIES = {
    "technician equality": "SELECT * FROM maint_job WHERE technician='Beier'",
    "machine equality": "SELECT * FROM maint_job WHERE machine_name='cnc-01'",
    "leading-wildcard LIKE": "SELECT * FROM maint_job WHERE technician LIKE '%ei%'",
    "wrapped equality": "SELECT * FROM maint_job WHERE lower(technician)='beier'",
}

conn = sqlite3.connect(":memory:")
conn.executescript(LEGACY.read_text(encoding="cp1252"))
for phase in ("before index", "after technician index"):
    if phase.startswith("after"):
        conn.execute("CREATE INDEX ix_job_technician ON maint_job(technician)")
    print(f"\n## {phase}")
    for label, sql in QUERIES.items():
        plan = conn.execute("EXPLAIN QUERY PLAN " + sql).fetchall()
        rows = conn.execute(sql).fetchall()
        print(f"{label}: " + " | ".join(row[3] for row in plan))
        print(f"  rows={len(rows)}")
conn.close()
