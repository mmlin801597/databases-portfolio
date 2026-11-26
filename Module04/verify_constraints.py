"""Exercise Module 4 constraints and audit protections on a disposable DB."""
from contextlib import closing
from pathlib import Path
import sqlite3
import tempfile

SETUP = Path(__file__).with_name("setup.sql").read_text(encoding="utf-8")


def rejected(conn, sql, parameters=()):
    try:
        conn.execute(sql, parameters)
    except sqlite3.IntegrityError as error:
        return str(error)
    raise AssertionError(f"Expected integrity rejection: {sql}")


with tempfile.TemporaryDirectory(prefix="module04-constraints-") as temp:
    path = Path(temp) / "check.db"
    with closing(sqlite3.connect(path)) as conn:
        conn.executescript(SETUP)
        conn.execute("PRAGMA foreign_keys=ON")
        conn.execute("INSERT INTO reading(sensor_id,ts,value,interval_s) VALUES(1,'2026-05-01 00:00:00',41.5,1)")
        energy = conn.execute("SELECT energy_j FROM reading WHERE ts='2026-05-01 00:00:00'").fetchone()[0]
        assert energy == 41.5
        print("generated energy_j:", energy)
        checks = [
            ("range CHECK", "INSERT INTO reading(sensor_id,ts,value,interval_s) VALUES(1,'2026-05-01 00:00:01',5001,1)", ()),
            ("STRICT REAL", "INSERT INTO reading(sensor_id,ts,value,interval_s) VALUES(1,'2026-05-01 00:00:02','not-real',1)", ()),
            ("foreign key", "INSERT INTO reading(sensor_id,ts,value,interval_s) VALUES(99,'2026-05-01 00:00:03',1,1)", ()),
            ("unique sensor metric", "INSERT INTO sensor VALUES(3,'cnc-01','temp_c','degC')", ()),
            ("unique reading key", "INSERT INTO reading(sensor_id,ts,value,interval_s) VALUES(1,'2026-03-01 08:00:00',42,1)", ()),
        ]
        for label, sql, params in checks:
            print(label + " rejected:", rejected(conn, sql, params))
        conn.execute("UPDATE reading SET value=42 WHERE ts='2026-05-01 00:00:00'")
        print("audit rows after value update:", conn.execute("SELECT COUNT(*) FROM audit").fetchone()[0])
        print("audit update rejected:", rejected(conn, "UPDATE audit SET new_value=99 WHERE audit_id=1"))
        print("audit delete rejected:", rejected(conn, "DELETE FROM audit WHERE audit_id=1"))
        print("foreign_key_check:", conn.execute("PRAGMA foreign_key_check").fetchall())
