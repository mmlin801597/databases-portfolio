# Task 1: Reconstruct the ER Model

## 1. Entities, Attributes, and Intended Primary Keys

### Machine
- **Attributes:** machine_name, serial_no, site, installed
- **Intended primary key:** machine_name
- Each machine should have a unique name and serial number.

### Part
- **Attributes:** part_no, description, unit_price
- **Intended primary key:** part_no
- Each part should have a unique part number.

### MaintenanceJob
- **Attributes:** job_id, machine_name, technician, done_on, parts_used
- **Intended primary key:** job_id
- Each maintenance job should have a unique ID and refer to one machine and one technician.

### Technician
- **Attributes:** technician_name
- **Intended primary key:** technician_name
- A technician can perform many maintenance jobs.

### JobPart (associative entity)
- **Attributes:** job_id, part_no
- **Intended composite primary key:** (job_id, part_no)
- This entity connects maintenance jobs and parts because one job can use multiple parts and one part can be used in multiple jobs.

## 2. Reconstructed ER Diagram

```mermaid
erDiagram
    MACHINE ||--o{ MAINTENANCE_JOB : has
    TECHNICIAN ||--o{ MAINTENANCE_JOB : performs
    MAINTENANCE_JOB ||--o{ JOB_PART : includes
    PART ||--o{ JOB_PART : used_in

    MACHINE {
        string machine_name PK
        string serial_no
        string site
        date installed
    }

    TECHNICIAN {
        string technician_name PK
    }

    MAINTENANCE_JOB {
        int job_id PK
        string machine_name FK
        string technician_name FK
        date done_on
    }

    PART {
        string part_no PK
        string description
        decimal unit_price
    }

    JOB_PART {
        int job_id PK, FK
        string part_no PK, FK
    }
```

## 3. Cardinality Findings

The database contains:
- **Machines:** 4 rows
- **Parts:** 4 rows, but only 3 distinct part numbers because P-1003 is duplicated.
- **Maintenance jobs:** 4 rows
- **Jobs using multiple parts:** Job 1 uses P-1001 and P-1002, so at least one job has multiple parts.
- **Invalid machine reference:** Job 3 refers to cnc-05, which is not present in the machine table.

### Query evidence

The counts below were checked from the four-row fixture in `legacy-schema.sql`:

```sql
SELECT machine_name, COUNT(*) AS jobs FROM maint_job GROUP BY machine_name;
SELECT technician, COUNT(*) AS jobs FROM maint_job GROUP BY technician;
SELECT COUNT(*) AS orphan_jobs FROM maint_job m LEFT JOIN machine x
  ON x.machine_name=m.machine_name WHERE x.machine_name IS NULL;
SELECT part_no, COUNT(*) AS copies FROM part GROUP BY part_no;
```

Observed grouped counts: `cnc-01=2`, `cnc-02=1`, `cnc-05=1`; `Beier=2`, `Klaas=1`, `Werther=1`; one orphan job; `P-1001=1`, `P-1002=1`, `P-1003=2`. `cnc-05` is the invalid reference, and the duplicated part identifier is `P-1003`.

## 4. Relationship Types

- **1:1:** No clear one-to-one relationship is represented by the current data or schema.
- **1:n:** The schema implies that one machine can have many maintenance jobs, and one technician can perform many jobs.
- **m:n:** The relationship between maintenance jobs and parts is hidden inside the comma-separated `parts_used` column. It should be represented by an associative entity such as JobPart.

## 5. Problems in the Legacy Schema

- Primary keys and foreign keys are not declared.
- The part number P-1003 appears twice.
- `unit_price` is stored as text instead of a numeric type.
- `installed` and `done_on` are stored as text without date validation.
- `parts_used` contains multiple values in one column, violating First Normal Form (1NF).
- Job 3 refers to a machine that does not exist.
- The technician is stored as text rather than being represented by a separate entity.
