# Module 5 Benchmark Results

## Method

Run `Module05/benchmark.py` with the repository's existing Python environment. The runner creates a fresh database under a system temporary directory, loads `setup.sql`, checks row counts, bidirectional value equivalence, and foreign keys, captures both query plans, then measures three interleaved executions per design with `time.perf_counter()`. It also measures three interleaved updates per design inside rollback-only transactions, obtains page sizes from SQLite `dbstat`, and compares indexed/no-index report query runs in alternating order using a savepoint to restore the index. The temporary database is removed when the process exits; it does not open or overwrite the Module 2â€“4 databases.

**Observed environment:** Windows workspace, Python 3.14.9, SQLite 3.53.1. Cache state is local to this run. Each comparison has three runs per case in one benchmark session on one machine, not a cross-machine result.

## Integrity and row counts

| Table | Rows |
|---|---:|
| `flat_jobpart` | 200,000 |
| `machine` | 50 |
| `part` | 10 |
| `job` | 20,000 |
| `job_part` | 200,000 |
| `report_jobpart` | 200,000 |

The normalized join reproduced **200,000** flat rows. Bidirectional attribute comparison reported **0** rows missing or mismatched in either direction. `PRAGMA foreign_key_check` returned **0** errors.

The disposable anomaly examples reported: update touched **3** duplicated `cnc-01` rows; the flat insert created **1** placeholder with a NULL job ID, while the normalized insert created **1** independent part used by **0** jobs; deleting the only `P-0002` flat row deleted **1** row and left **0** flat rows, while the normalized part record remained.

## Query plans

Normalized query:

```text
SCAN jp
SEARCH p USING INDEX sqlite_autoindex_part_1 (part_no=?)
SEARCH j USING INTEGER PRIMARY KEY (rowid=?)
SEARCH m USING INDEX sqlite_autoindex_machine_1 (machine_id=?)
USE TEMP B-TREE FOR GROUP BY
```

Denormalized query:

```text
SCAN report_jobpart USING INDEX ix_report_machine
USE TEMP B-TREE FOR GROUP BY
```

The report plan still scans the report index and groups into a temporary B-tree. In this workload the four-table query was not slower than the single-table scan.

## Measured reads

| Design | Three runs (ms) | Median (ms) |
|---|---|---:|
| Normalized | 74.310, 80.206, 74.920 | 74.920 |
| Denormalized | 89.618, 89.990, 90.684 | 89.990 |

## Update fan-out and timing

Each rollback-only site update affected **1** normalized `machine` row and **4,000** `report_jobpart` rows. Three interleaved update runs (ms) and medians:

| Design | Runs (ms) | Median (ms) |
|---|---|---:|
| Normalized | 7.222, 0.765, 0.644 | 0.765 |
| Denormalized | 13.187, 7.161, 7.220 | 7.220 |

The first update for each design includes setup/cache effects; the median summarizes this short local run, not a stable latency guarantee.

## Storage and index experiment

| Objects | Bytes |
|---|---:|
| Normalized tables (`machine`, `part`, `job`, `job_part`) | 4,071,424 |
| Normalized indexes (`ix_job_done_on`, `ix_job_part_part_no`) | 3,354,624 |
| `report_jobpart` table | 11,091,968 |
| `ix_report_machine` | 2,990,080 |

The report query with/without its index used alternating order across three pairs. Times and medians:

| Case | Runs (ms) | Median (ms) |
|---|---|---:|
| With `ix_report_machine` | 89.031, 94.229, 90.039 | 90.039 |
| Without the index | 57.483, 54.124, 54.410 | 54.410 |

The no-index scan was faster in this run. This comparison is still a short local experiment; cache and planner behavior may vary on other systems or data sizes.

## Reproduction

```powershell
.\.venv\Scripts\python.exe Module05\benchmark.py
```


