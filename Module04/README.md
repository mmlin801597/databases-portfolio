# Module 4 — Integrity at the Edge

## Reproducible implementation

- [Fresh schema, constraints, view, and triggers](setup.sql), plus [disposable constraint verification](verify_constraints.py)
- [Constraint evidence](task1-evidence.md) and screenshot
- [Idempotent ingestion](ingest.py), [CSV fixture](readings.csv), and [Task 2 evidence](task2-evidence.md)
- [Trigger benchmark script](benchmark_triggers.py) and [measured results](task3-evidence.md)
- [Read-only connection check](access_check.py) and [access-control discussion](task4-evidence.md)
- [BEFORE INSERT experiment](task5.sql) and [interpretation](task5-evidence.md)
- [Integrity discussion prompts](integrity-notes.md)
- [Reflection prompts](../Reflections/ref04.md)

Run the schema with `sqlite3 :memory: ".read Module04/setup.sql"` from the repository root. `setup.sql` creates a clean baseline; it does not overwrite the existing `edge.db`, which contains prior local state.
