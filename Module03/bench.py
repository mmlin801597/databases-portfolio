"""Interleaved index benchmark using fresh, disposable SQLite databases."""
from pathlib import Path
from contextlib import closing
import sqlite3
import statistics
import tempfile
import time

ROOT = Path(__file__).resolve().parent
SETUP = ROOT / "setup.sql"
QUERY = """SELECT c.city, COUNT(DISTINCT c.customer_id) AS customers,
       SUM(ol.qty * p.price) AS revenue
FROM customer c JOIN orders o ON o.customer_id=c.customer_id
JOIN order_line ol ON ol.order_id=o.order_id
JOIN product p ON p.product_id=ol.product_id
WHERE o.ordered_on >= '2025-01-01' AND o.ordered_on < '2026-01-01'
GROUP BY c.city ORDER BY revenue DESC"""
VARIANTS = {
    "baseline": None,
    "orders_date": "CREATE INDEX ix_orders_ordered_on ON orders(ordered_on)",
    "line_product": "CREATE INDEX ix_orderline_product ON order_line(product_id)",
    "line_order": "CREATE INDEX ix_orderline_order ON order_line(order_id)",
}
REPEATS = 5


def main():
    with tempfile.TemporaryDirectory(prefix="module03-bench-") as temp:
        dbs = {}
        for name, index_sql in VARIANTS.items():
            path = Path(temp) / f"{name}.db"
            with closing(sqlite3.connect(path)) as conn:
                conn.executescript(SETUP.read_text(encoding="utf-8"))
                if index_sql:
                    conn.execute(index_sql)
                conn.commit()
            dbs[name] = path

        samples = {name: [] for name in VARIANTS}
        # Rotate the first variant so every configuration gets a different cache/order position.
        for round_no in range(REPEATS):
            order = list(VARIANTS)
            shift = round_no % len(order)
            order = order[shift:] + order[:shift]
            for name in order:
                with closing(sqlite3.connect(dbs[name])) as conn:
                    start = time.perf_counter()
                    conn.execute(QUERY).fetchall()
                    samples[name].append((time.perf_counter() - start) * 1000)

        print(f"Query: dashboard aggregate; {REPEATS} interleaved runs per fresh variant")
        for name, path in dbs.items():
            with closing(sqlite3.connect(path)) as conn:
                plan = conn.execute("EXPLAIN QUERY PLAN " + QUERY).fetchall()
            times = samples[name]
            print(f"\n{name}: runs_ms=" + ", ".join(f"{x:.3f}" for x in times))
            print(f"median_ms={statistics.median(times):.3f}")
            print("plan=" + " | ".join(row[3] for row in plan))


if __name__ == "__main__":
    main()
