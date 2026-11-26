
-- Defect 1: Orphan maintenance jobs
SELECT m.job_id, m.machine_name
FROM maint_job m
LEFT JOIN machine x ON m.machine_name = x.machine_name
WHERE x.machine_name IS NULL;

-- Defect 2: Duplicate part numbers
SELECT part_no, COUNT(*) AS copies
FROM part
GROUP BY part_no
HAVING COUNT(*) > 1;

-- Defect 3: Text-based price comparison
SELECT part_no, unit_price
FROM part
WHERE unit_price < '15';

-- Supplemental comparison: cast explicitly to numeric to avoid text ordering.
SELECT DISTINCT part_no, unit_price
FROM part
WHERE CAST(unit_price AS NUMERIC) < 15
ORDER BY part_no;

-- Defect 4: Invalid installed dates
SELECT machine_name, installed
FROM machine
WHERE installed NOT GLOB
'[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]';

-- Defect 5: Joining against a comma-separated list
SELECT j.job_id, p.description
FROM maint_job j
JOIN part p ON p.part_no = j.parts_used;
