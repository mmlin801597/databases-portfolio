# Recommendation to the Operations Lead

**Evidence:** [`benchmark-results.md`](benchmark-results.md), the latest local run with three interleaved dashboard and update timings per design.

Keep the transactional schema normalized to 3NF so each machine site and part price has one authoritative value. In the latest run, the denormalized dashboard median was **89.990 ms** versus **74.920 ms** for the normalized query, so the report table did not show a read-speed advantage on this dataset. The report table and its index used **14,082,048 bytes** combined (11,091,968 + 2,990,080), compared with **7,426,048 bytes** for the normalized tables and listed indexes. A site update changed 1 normalized row versus 4,000 report rows; three-run medians were **0.765 ms** and **7.220 ms**. Keep the dashboard on the normalized query for now; consider the report table only if a representative workload later demonstrates a material read benefit. If adopted, rebuild it transactionally on a schedule set by the allowed freshness window, and expose its last-refresh time so consumers can see its staleness.

**TODO — TEAM INPUT REQUIRED:** Confirm the dashboard freshness requirement and acceptable staleness with the operations stakeholder/pod, then replace this sentence with the agreed threshold.
