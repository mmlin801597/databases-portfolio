# Task 2: Integrity Defects

## Defect 1: Orphan maintenance jobs
**Evidence:** Job 3 references machine `cnc-05`, which does not exist in the machine table.

**Production impact:** The maintenance job cannot be reliably linked to a machine or site.

## Defect 2: Duplicate part numbers
**Evidence:** Part number `P-1003` appears twice.

**Production impact:** Duplicate part records can lead to incorrect inventory counts and purchasing reports.

## Defect 3: Prices stored as text
**Evidence:** The query compares text values with `'15'`, so SQLite compares them lexically. It returns `P-1001` (`12.50`) but misses `P-1003` (`9.90`): the first character `'9'` sorts after `'1'`, even though 9.90 is numerically less than 15. A numeric cast returns both distinct parts below 15. The duplicate `P-1003` rows are a separate defect.

**Production impact:** Text-based price comparisons can omit valid low-priced parts from financial reports. Store prices as a numeric type and compare numeric values.

## Defect 4: Invalid installation date
**Evidence:** Machine `RANDOM-NAME` has the installation date `unknown`.

**Production impact:** Invalid dates can break equipment-age calculations and maintenance schedules.

## Defect 5: Comma-separated part list
**Evidence:** Job 1 uses `P-1001,P-1002`, but the join does not return that job.

**Production impact:** Maintenance reports can omit jobs that use multiple parts.

## Evidence files
- `defect-queries.sql` — the five SQL queries.
- `defect-results.txt` — their saved results.
