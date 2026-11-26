# Module 5 Harvest — Curiosities

These are individual questions to take to the harvest. No pod discussion is claimed here.

1. **Why does `CROSS JOIN` produce 200,000 rows?** Source: [`setup.sql`](setup.sql). The 20,000 job numbers combine with 10 part numbers each.
2. **Why is `part_price` text in the flat table?** Source: [`setup.sql`](setup.sql). `printf('%.2f', ...)` creates a text value, so numeric comparisons need explicit conversion.
3. **What does a `dbstat` page size include?** Source: [`benchmark.py`](benchmark.py). The virtual table attributes database pages to tables and indexes.
4. **Why can a full index scan be slower than a table scan?** Source: [`benchmark.py`](benchmark.py). A non-covering index can require extra table lookups.
5. **What assumption does `SELECT DISTINCT` make during decomposition?** Source: [`setup.sql`](setup.sql). It assumes each job maps to one machine, technician, and date.

Sources for the concepts: [SQLite `dbstat`](https://www.sqlite.org/dbstat.html), [SQLite query plans](https://www.sqlite.org/eqp.html), and [SQLite foreign keys](https://www.sqlite.org/foreignkeys.html).

**TODO — TEAM INPUT REQUIRED:** Add the questions or surprising findings contributed by the pod, and note any unresolved item shared with the class.
