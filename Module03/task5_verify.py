"""Compare grouped, correlated, and window formulations on the module fixture."""
from pathlib import Path
import sqlite3

ROOT = Path(__file__).resolve().parent
conn = sqlite3.connect(":memory:")
conn.executescript((ROOT / "setup.sql").read_text(encoding="utf-8"))
queries = {
    "grouped": """SELECT c.customer_id,c.name,COUNT(*) AS late_orders
        FROM orders o JOIN customer c ON c.customer_id=o.customer_id
        WHERE o.status='late' GROUP BY c.customer_id,c.name""",
    "correlated": """SELECT c.customer_id,c.name,
        (SELECT COUNT(*) FROM orders o WHERE o.customer_id=c.customer_id AND o.status='late') AS late_orders
        FROM customer c WHERE EXISTS (SELECT 1 FROM orders o
        WHERE o.customer_id=c.customer_id AND o.status='late')""",
    "window": """SELECT customer_id,name,late_orders FROM (
        SELECT c.customer_id,c.name,COUNT(*) OVER(PARTITION BY c.customer_id) AS late_orders,
        ROW_NUMBER() OVER(PARTITION BY c.customer_id ORDER BY o.order_id) AS rn
        FROM orders o JOIN customer c ON c.customer_id=o.customer_id WHERE o.status='late')
        WHERE rn=1""",
}
results = {name: sorted(conn.execute(sql).fetchall()) for name, sql in queries.items()}
assert results["grouped"] == results["correlated"] == results["window"]
print("equivalent result rows:", len(results["grouped"]))
for name, sql in queries.items():
    print(name + " plan:", " | ".join(row[3] for row in conn.execute("EXPLAIN QUERY PLAN " + sql)))
conn.close()
