# Module04 — Task 4: Access Control Without a Server

## Access Control Evidence

SQLite does not have `GRANT` and `REVOKE` like PostgreSQL. Instead, access can be controlled using a safe view, file permissions, and a read-only database connection.

The `machine_health` view exposes only the required machine health information instead of giving report readers direct access to all tables.

With PostgreSQL, access control is managed by the database server using users, roles, and privileges such as `GRANT` and `REVOKE`. PostgreSQL is better suited for a multi-tenant web application because different users can have different database permissions while the database server controls access. File-permission-based control is acceptable for a local SQLite application because the database is a local file, but it is not sufficient for a multi-tenant web app because users must not be able to access or modify the database file directly.

## Evidence

- `machine_health` view created successfully.
- Read-only connection successfully returned **10,004** readings.
- Write attempt using `mode=ro` failed with `attempt to write a readonly database`.
- File write access was restored afterward.