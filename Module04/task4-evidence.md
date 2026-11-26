# Module04 — Task 4: Access Control Without a Server

SQLite does not provide server roles and `GRANT`/`REVOKE`. A safe view can limit the columns and rows exposed by an application, while a read-only connection opened with `mode=ro` prevents writes through that connection. The `machine_health` view is included in the reproducible schema in `setup.sql`.

Run `python Module04/access_check.py` to create a disposable database, read the view, and confirm that an insert through a read-only URI is rejected. This does not change the tracked `edge.db`.

A read-only connection does not replace operating-system file permissions. SQLite file access is not per-user database authorization, so a multi-tenant service should keep the database file behind a trusted application or use a server database with roles.

## Personal evidence still needed

- [ ] If the coursework requires a file-permission experiment, add a screenshot or terminal transcript from your own OS showing the permission change and restoration. The current repository does not preserve evidence that this was actually performed.
- [ ] The tracked `edge.db` currently contains 10,005 readings. Earlier draft evidence said 10,004; that saved count is inconsistent with the current file and should not be treated as the reproducible setup result.
