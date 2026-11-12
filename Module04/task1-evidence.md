# Module04 — Task 1: Constraint Evidence

## Proof that the constraints work

The screenshots below show the results of testing the database constraints.

- Valid reading inserted successfully.
- `energy_j` was generated correctly as `41.5`.
- Invalid temperature was rejected by the `CHECK` constraint.
- Text value was rejected by the `STRICT` `REAL` column.
- Non-existing `sensor_id` was rejected by the `FOREIGN KEY` constraint.
- Duplicate machine/metric was rejected by the `UNIQUE` constraint.

## Screenshot Evidence

[![Task 1 Evidence](task1%20evidence.png)](task1%20evidence.png)