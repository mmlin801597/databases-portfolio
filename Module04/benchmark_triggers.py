"""Compare vibration-trigger overhead on fresh in-memory databases."""
from datetime import datetime, timedelta
import statistics
import sqlite3
import time
from pathlib import Path

SETUP = Path(__file__).with_name("setup.sql").read_text(encoding="utf-8")
COUNT = 10_000
REPEATS = 5


def measure(with_trigger):
    conn = sqlite3.connect(":memory:")
    conn.executescript(SETUP)
    conn.execute("PRAGMA foreign_keys=ON")
    if not with_trigger:
        conn.execute("DROP TRIGGER trg_vib_alarm")
    base = datetime(2026, 4, 1)
    rows = [(2, (base + timedelta(seconds=i)).strftime("%Y-%m-%d %H:%M:%S"), 2.5, 1)
            for i in range(COUNT)]
    start = time.perf_counter()
    conn.executemany(
        "INSERT INTO reading(sensor_id,ts,value,interval_s) VALUES(?,?,?,?)", rows
    )
    conn.commit()
    elapsed = (time.perf_counter() - start) * 1000
    alarms = conn.execute("SELECT COUNT(*) FROM alarm").fetchone()[0]
    conn.close()
    return elapsed, alarms


def main():
    samples = {False: [], True: []}
    alarms = {}
    for i in range(REPEATS):
        order = [False, True] if i % 2 == 0 else [True, False]
        for enabled in order:
            elapsed, alarm_count = measure(enabled)
            samples[enabled].append(elapsed)
            alarms[enabled] = alarm_count
    print(f"Fresh in-memory database; {COUNT} valid vibration rows per run; {REPEATS} interleaved pairs")
    for enabled in (False, True):
        label = "with trigger" if enabled else "without trigger"
        vals = samples[enabled]
        print(f"{label}: runs_ms=" + ", ".join(f"{x:.3f}" for x in vals))
        print(f"{label}: median_ms={statistics.median(vals):.3f}; alarm_rows={alarms[enabled]}")


if __name__ == "__main__":
    main()
