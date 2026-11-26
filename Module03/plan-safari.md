# Module 3 — Plan Safari

`plan_safari.py` loads the Module 2 legacy fixture into an in-memory database and prints actual `EXPLAIN QUERY PLAN` details before and after adding only `ix_job_technician`.

| Predicate | Before index | After index | Rows returned |
|---|---|---|---:|
| `technician='Beier'` | `SCAN maint_job` | `SEARCH maint_job USING INDEX ix_job_technician (technician=?)` | 2 |
| `machine_name='cnc-01'` | `SCAN maint_job` | `SCAN maint_job` | 2 |
| `technician LIKE '%ei%'` | `SCAN maint_job` | `SCAN maint_job` | 2 |
| `lower(technician)='beier'` | `SCAN maint_job` | `SCAN maint_job` | 2 |

The index supports an equality predicate on its leading column. It does not help a predicate on another column. A leading wildcard prevents a conventional B-tree prefix lookup, and wrapping the indexed column in `lower()` means the query expression differs from the indexed expression. An expression index or normalized search key could address the latter case if that workload justified it. The table has only four fixture rows, so this demonstrates plan choice, not a meaningful timing benefit.

Reproduce with `python Module03/plan_safari.py` from the repository root. Results above are from this workspace's current SQLite run.
