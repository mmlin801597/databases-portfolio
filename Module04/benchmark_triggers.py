import sqlite3
import time

DB_PATH = "Module04/edge.db"

TRIGGER_SQL = """
CREATE TRIGGER trg_vib_alarm
AFTER INSERT ON reading
FOR EACH ROW
WHEN NEW.value > 2.0
  AND (SELECT metric FROM sensor WHERE sensor_id = NEW.sensor_id) = 'vib_rms'
BEGIN
    INSERT INTO alarm(sensor_id, ts, value, reason)
    VALUES (
        NEW.sensor_id,
        NEW.ts,
        NEW.value,
        'vibration over 2.0 mm/s'
    );
END;
"""


def benchmark(with_trigger):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA foreign_keys = ON")

        conn.execute("DROP TRIGGER IF EXISTS trg_vib_alarm")

        if with_trigger:
            conn.execute(TRIGGER_SQL)

        conn.execute("DELETE FROM alarm")

        # Remove previous benchmark readings
        conn.execute(
            "DELETE FROM reading WHERE ts LIKE '2026-04-01%'"
        )
        conn.commit()

        rows = [
            (
                2,
                f"2026-04-01 00:{i // 60:02d}:{i % 60:02d}",
                2.5,
                1,
            )
            for i in range(10000)
        ]

        start = time.perf_counter()

        conn.executemany(
            """
            INSERT INTO reading(sensor_id, ts, value, interval_s)
            VALUES (?, ?, ?, ?)
            """,
            rows,
        )

        conn.commit()

        elapsed = time.perf_counter() - start

        print(
            f"{'WITH' if with_trigger else 'WITHOUT'} alarm trigger: "
            f"{elapsed * 1000:.2f} ms"
        )


benchmark(False)
benchmark(True)