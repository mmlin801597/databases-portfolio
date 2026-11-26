"""Demonstrate read-only SQLite access using a disposable database."""
from pathlib import Path
from contextlib import closing
import sqlite3
import tempfile

SETUP = Path(__file__).with_name("setup.sql").read_text(encoding="utf-8")
with tempfile.TemporaryDirectory(prefix="module04-readonly-") as temp:
    path = Path(temp) / "edge.db"
    conn = sqlite3.connect(path)
    conn.executescript(SETUP)
    conn.execute("INSERT INTO reading(sensor_id,ts,value,interval_s) VALUES(1,'2026-05-01 00:00:00',41.5,1)")
    conn.commit()
    conn.close()
    uri = path.as_uri() + "?mode=ro"
    with closing(sqlite3.connect(uri, uri=True)) as ro:
        print("read-only view rows:", ro.execute("SELECT * FROM machine_health").fetchall())
        try:
            ro.execute("INSERT INTO reading(sensor_id,ts,value,interval_s) VALUES(1,'2026-05-01 00:00:01',42,1)")
            ro.commit()
        except sqlite3.OperationalError as error:
            print("write rejected:", error)
