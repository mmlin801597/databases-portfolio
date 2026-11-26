"""Build an isolated Module 5 database and measure read, update, and storage costs."""

import statistics
import sqlite3
import tempfile
import time
from pathlib import Path

SETUP = Path(__file__).with_name("setup.sql")
NORMALIZED = """SELECT m.machine_id, m.site, j.technician,
       SUM(p.part_price) AS cost
FROM job AS j
JOIN machine AS m ON m.machine_id = j.machine_id
JOIN job_part AS jp ON jp.job_id = j.job_id
JOIN part AS p ON p.part_no = jp.part_no
WHERE j.done_on >= date('2026-03-01')
GROUP BY m.machine_id, j.technician"""
DENORMALIZED = """SELECT machine_id, site, technician,
       SUM(part_price) AS cost
FROM report_jobpart
WHERE done_on >= date('2026-03-01')
GROUP BY machine_id, technician"""


def elapsed_ms(conn: sqlite3.Connection, sql: str) -> float:
    start = time.perf_counter()
    conn.execute(sql).fetchall()
    return (time.perf_counter() - start) * 1000


def table_bytes(conn: sqlite3.Connection, names: tuple[str, ...]) -> int | None:
    try:
        marks = ",".join("?" for _ in names)
        row = conn.execute(
            f"SELECT COALESCE(SUM(pgsize), 0) FROM dbstat WHERE name IN ({marks})",
            names,
        ).fetchone()
        return int(row[0])
    except sqlite3.OperationalError:
        return None


with tempfile.TemporaryDirectory(prefix="module05-") as temp_dir:
    db_path = Path(temp_dir) / "benchmark.db"
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SETUP.read_text(encoding="utf-8"))

    counts = {
        name: conn.execute(f"SELECT COUNT(*) FROM {name}").fetchone()[0]
        for name in ("flat_jobpart", "machine", "part", "job", "job_part", "report_jobpart")
    }
    joined = conn.execute(
        "SELECT COUNT(*) FROM job AS j JOIN job_part AS jp USING(job_id) "
        "JOIN part AS p USING(part_no) JOIN machine AS m USING(machine_id)"
    ).fetchone()[0]
    flat_only = conn.execute("""
        SELECT COUNT(*) FROM flat_jobpart AS f
        LEFT JOIN job_part AS jp ON jp.job_id = f.job_id AND jp.part_no = f.part_no
        LEFT JOIN job AS j ON j.job_id = jp.job_id
        LEFT JOIN machine AS m ON m.machine_id = j.machine_id
        LEFT JOIN part AS p ON p.part_no = jp.part_no
        WHERE jp.job_id IS NULL OR j.job_id IS NULL OR m.machine_id IS NULL
           OR p.part_no IS NULL OR f.machine_id IS NOT j.machine_id
           OR f.site IS NOT m.site OR f.technician IS NOT j.technician
           OR CAST(f.part_price AS REAL) IS NOT p.part_price OR f.done_on IS NOT j.done_on
    """).fetchone()[0]
    normalized_only = conn.execute("""
        SELECT COUNT(*) FROM job_part AS jp
        JOIN job AS j ON j.job_id = jp.job_id
        JOIN machine AS m ON m.machine_id = j.machine_id
        JOIN part AS p ON p.part_no = jp.part_no
        LEFT JOIN flat_jobpart AS f ON f.job_id = jp.job_id AND f.part_no = jp.part_no
        WHERE f.job_id IS NULL OR f.machine_id IS NOT j.machine_id
           OR f.site IS NOT m.site OR f.technician IS NOT j.technician
           OR CAST(f.part_price AS REAL) IS NOT p.part_price OR f.done_on IS NOT j.done_on
    """).fetchone()[0]
    fk_errors = conn.execute("PRAGMA foreign_key_check").fetchall()
    print("ROWS", counts)
    print("FLAT_VS_JOINED", counts["flat_jobpart"], joined)
    print("VALUE_MISMATCHES", {"flat_not_in_normalized": flat_only,
                               "normalized_not_in_flat": normalized_only})
    print("FOREIGN_KEY_ERRORS", len(fk_errors))

    # Run the three anomaly examples only in this disposable database.
    conn.executescript("""
        CREATE TABLE flat5 (
            job_id INTEGER, machine_id TEXT, site TEXT,
            technician TEXT, part_no TEXT, part_price REAL
        );
        INSERT INTO flat5 VALUES
            (1, 'cnc-01', 'Gütersloh', 'tech-0', 'P-0001', 6.00),
            (1, 'cnc-01', 'Gütersloh', 'tech-0', 'P-0002', 7.00),
            (2, 'cnc-02', 'Gütersloh', 'tech-1', 'P-0001', 6.00),
            (2, 'cnc-02', 'Gütersloh', 'tech-1', 'P-0003', 8.50),
            (3, 'cnc-01', 'Gütersloh', 'tech-0', 'P-0003', 8.50);
    """)
    conn.execute("UPDATE flat5 SET site='Bielefeld' WHERE machine_id='cnc-01'")
    print("ANOMALY_UPDATE", {"rows_touched": conn.execute("SELECT changes()").fetchone()[0],
                              "sites_after": conn.execute("SELECT DISTINCT site FROM flat5 WHERE machine_id='cnc-01'").fetchall()})
    conn.execute("INSERT INTO part(part_no, part_price) VALUES ('P-NEW', 9.25)")
    print("ANOMALY_NORMALIZED_INSERT", {
        "inserted_part_rows": conn.execute("SELECT changes()").fetchone()[0],
        "jobs_using_new_part": conn.execute("SELECT COUNT(*) FROM job_part WHERE part_no='P-NEW'").fetchone()[0],
    })
    conn.execute("DELETE FROM part WHERE part_no='P-NEW'")
    conn.execute("INSERT INTO flat5 VALUES (NULL,NULL,NULL,NULL,'P-0004',9.25)")
    print("ANOMALY_INSERT", {"placeholder_rows": conn.execute("SELECT COUNT(*) FROM flat5 WHERE part_no='P-0004'").fetchone()[0],
                              "rows_without_job": conn.execute("SELECT COUNT(*) FROM flat5 WHERE part_no='P-0004' AND job_id IS NULL").fetchone()[0]})
    conn.execute("DELETE FROM flat5 WHERE job_id=1 AND part_no='P-0002'")
    print("ANOMALY_DELETE", {"deleted_rows": conn.execute("SELECT changes()").fetchone()[0],
                              "remaining_flat_rows_for_part": conn.execute("SELECT COUNT(*) FROM flat5 WHERE part_no='P-0002'").fetchone()[0],
                              "normalized_part_record_remains": conn.execute("SELECT COUNT(*) FROM part WHERE part_no='P-0002'").fetchone()[0]})
    conn.execute("DROP TABLE flat5")
    conn.commit()

    plans = {}
    for label, sql in (("normalized", NORMALIZED), ("denormalized", DENORMALIZED)):
        plans[label] = conn.execute("EXPLAIN QUERY PLAN " + sql).fetchall()
        print("PLAN", label)
        for row in plans[label]:
            print(" ", row[-1])

    # Warm each query, then interleave three timed observations.
    conn.execute(NORMALIZED).fetchall()
    conn.execute(DENORMALIZED).fetchall()
    timings = {"normalized": [], "denormalized": []}
    for _ in range(3):
        for label, sql in (("normalized", NORMALIZED), ("denormalized", DENORMALIZED)):
            timings[label].append(elapsed_ms(conn, sql))
    print("READ_TIMES_MS", {k: [round(x, 3) for x in v] for k, v in timings.items()})
    print("READ_MEDIANS_MS", {k: round(statistics.median(v), 3) for k, v in timings.items()})

    # Interleave three rollback-only updates per design and report medians.
    update_sql = {
        "normalized": "UPDATE machine SET site='Bielefeld' WHERE machine_id='cnc-02'",
        "denormalized": "UPDATE report_jobpart SET site='Bielefeld' WHERE machine_id='cnc-02'",
    }
    update_timings = {"normalized": [], "denormalized": []}
    update_rows = {}
    for _ in range(3):
        for label, sql in update_sql.items():
            conn.execute("BEGIN")
            start = time.perf_counter()
            conn.execute(sql)
            update_timings[label].append((time.perf_counter() - start) * 1000)
            update_rows[label] = conn.execute("SELECT changes()").fetchone()[0]
            conn.rollback()
    print("UPDATE_ROWS", update_rows)
    print("UPDATE_RUNS_MS", {k: [round(x, 3) for x in v] for k, v in update_timings.items()})
    print("UPDATE_MEDIANS_MS", {k: round(statistics.median(v), 3) for k, v in update_timings.items()})

    normalized_bytes = table_bytes(conn, ("machine", "part", "job", "job_part"))
    normalized_index_bytes = table_bytes(conn, ("ix_job_done_on", "ix_job_part_part_no"))
    report_bytes = table_bytes(conn, ("report_jobpart",))
    report_index_bytes = table_bytes(conn, ("ix_report_machine",))
    print("STORAGE_BYTES", {
        "normalized_tables": normalized_bytes,
        "normalized_indexes": normalized_index_bytes,
        "report_table": report_bytes,
        "report_index": report_index_bytes,
    })

    # Compare index/scan with alternating order and rollback-safe index restoration.
    conn.execute(DENORMALIZED).fetchall()
    index_timings = {"with_index": [], "without_index": []}
    for run in range(3):
        order = ("with_index", "without_index") if run % 2 == 0 else ("without_index", "with_index")
        for variant in order:
            if variant == "with_index":
                index_timings[variant].append(elapsed_ms(conn, DENORMALIZED))
            else:
                conn.execute("SAVEPOINT index_test")
                conn.execute("DROP INDEX ix_report_machine")
                index_timings[variant].append(elapsed_ms(conn, DENORMALIZED))
                conn.execute("ROLLBACK TO index_test")
                conn.execute("RELEASE index_test")
    print("REPORT_INDEX_RUNS_MS", {
        k: [round(x, 3) for x in v] for k, v in index_timings.items()
    })
    print("REPORT_INDEX_MEDIANS_MS", {
        k: round(statistics.median(v), 3) for k, v in index_timings.items()
    })
    conn.close()
