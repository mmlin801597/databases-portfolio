import sqlite3
import statistics
import time

DB = "Module03/warehouse.db"

DASHBOARD = """
SELECT c.city,
       COUNT(DISTINCT c.customer_id) AS customers,
       SUM(ol.qty * p.price) AS revenue
FROM customer c
JOIN orders o
    ON o.customer_id = c.customer_id
JOIN order_line ol
    ON ol.order_id = o.order_id
JOIN product p
    ON p.product_id = ol.product_id
WHERE o.ordered_on >= '2025-01-01'
  AND o.ordered_on < '2026-01-01'
GROUP BY c.city
ORDER BY revenue DESC;
"""

SINGLE_DAY = """
SELECT o.order_id, o.ordered_on, c.name
FROM orders o
JOIN customer c ON c.customer_id = o.customer_id
WHERE o.ordered_on = '2026-02-14';
"""


def run_query(conn, sql, repeats=3):
    times = []

    for _ in range(repeats):
        start = time.perf_counter()
        conn.execute(sql).fetchall()
        end = time.perf_counter()
        times.append((end - start) * 1000)

    return times, statistics.median(times)


conn = sqlite3.connect(DB)

for name, query in [
    ("dashboard", DASHBOARD),
    ("single_day", SINGLE_DAY),
]:
    times, median = run_query(conn, query)

    print(f"\n{name}")
    print(f"runs (ms): {[round(t, 3) for t in times]}")
    print(f"median (ms): {median:.3f}")

conn.close()