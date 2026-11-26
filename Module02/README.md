# Module 2 — Reconstruct and Repair a Database

This folder documents the legacy maintenance database, its defects, and a code-first repaired contract.

## Evidence

- [Legacy schema and sample rows](legacy-schema.sql)
- [ER reconstruction and observed cardinalities](er-audit.md)
- [Defect queries](defect-queries.sql) and [captured output](defect-results.txt)
- [Defect interpretation](defect-audit.md)
- [Pydantic and SQLAlchemy contract](contract.py), [generated DDL](contract-ddl.sql), and [constraint notes](contract-notes.md)
- [Inheritance mapping decision](inheritance-decision.md), [single-table SQL](inheritance-single-table.sql), and [separate-table SQL](inheritance-separate-tables.sql)
- [Mermaid modeling exercise](mermaid-lab.md)
- [Personal reflection](../Reflections/ref02.md)

The DDL is emitted by running `python Module02/contract.py`. Queries and captured results use the small fixture in `legacy-schema.sql`. Team or partner contributions are not asserted here; add those only from your own records.
