# Module 5 — Normalization vs. Denormalization

This module builds the 200,000-row flat relation, decomposes it into 3NF, and compares a normalized dashboard query with a denormalized reporting table.

## Evidence

- [Functional dependencies, key, normal forms, ER sketches, anomalies](normalization-notes.md)
- [SQLite setup and decomposition](setup.sql)
- [Isolated benchmark runner](benchmark.py) and [measured results](benchmark-results.md)
- [Recommendation memo](recommendation.md)
- [Harvest curiosities](curiosities.md)
- [Reflection prompts](../Reflections/ref05.md)
- [Official module specification](../Course_Materials/05-normalization-vs-denormalization.md)

## Reproduce

From the repository root, run:

```powershell
.\.venv\Scripts\python.exe Module05\benchmark.py
```

The runner creates its database in a temporary directory, reports counts, foreign-key checks, plans, timings, update fan-out, and page sizes, then removes the temporary database. It does not use the existing Module 2–4 databases.
