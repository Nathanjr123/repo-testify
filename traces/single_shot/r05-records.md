# Single-shot trajectory: r05-records (proof `single-shot-baseline-1788167374`)

Repository https://github.com/kennethreitz/records @ `ea4273695cee`. Buyer question: _We are evaluating records as the SQL layer for an internal analytics tool — do its connection-string examples, transaction API, and export features still work against a current SQLAlchemy, or will writes silently be lost?_

This is the **fair execution baseline** (arms/single_shot): one agent is handed the repository and all the claims, writes **one** bash script, runs it **once** in the same sandbox, and returns **one** judgment. It can run code, but it has none of the pipeline's structure (one probe per claim, VERDICT_LINE contract, per-claim adjudication, escalation). This trace exists to make that contrast follow-able.

## Step 1: instructions
See `arms/PROMPTS.md` (single-shot arm). Claims given to the agent:

- **c1** (install): The package 'records' with pandas support can be installed with the recommended command `pipenv install records[pandas]` (equivalently `pip install "records[pandas]"`), after which `import records` succeeds.
- **c2** (quickstart): In Python with 'records' installed, a database connection can be opened with a 'postgres://' URL scheme exactly as shown: `records.Database('postgres://...')`.
- **c3** (quickstart): In Python with 'records' installed, `db.query('select ...')` against a SQLite database returns rows that can be indexed (`rows[0]`) and iterated, with fields accessible as `row.name`, `row['name']`, and by integer index.
- **c4** (interface): In Python with 'records' installed, INSERT/UPDATE statements executed via `db.query(...)` (and `db.bulk_query(...)`) are durably committed to the database — data written through records is not lost when the connection closes.
- **c5** (interface): In Python with 'records' installed, transactions work via the documented API `t = Database.transaction(); t.commit()`.
- **c6** (interface): In Python with 'records' installed, query results expose `rows.first()` returning a single Record, and `rows.all()` returning a list of Records.
- **c7** (interface): In Python with 'records' installed, `rows.export('csv')` returns the result set serialized as CSV text with a header row.
- **c8** (interface): In Python with 'records' and pandas installed, `rows.export('df')` returns a pandas DataFrame of the result set.
- **c9** (interface): The 'records' package supports MS-SQL databases (with an appropriate driver installed): a records.Database using an mssql+pyodbc/pymssql URL can run queries that work through plain SQLAlchemy.
- **c10** (quantitative): The records README's PyPI badge asserts that 'records' is published on PyPI (latest release 0.6.0).
- **c11** (interface): In Python with 'records' installed, `records.Database()` with no argument reads the connection URL from the $DATABASE_URL environment variable.

## Step 2: the ONE script the agent wrote (executed once, in the sandbox)

```bash
grep -iE "does not provide the extra|pip_exit" /tmp/audit/install.log; pip show records 2>/dev/null | grep -iE "^(Name|Version|Requires)" && printf '%s\n' 'import os, sys, tempfile, sqlite3, subprocess, importlib.metadata' 'def out(cid, ok, reason):' '    print("CLAIM %s: %s %s" % (cid, "PASS" if ok
STDOUT pip_exit=0
Name: records
Version: 0.6.0
Requires: docopt, openpyxl, SQLAlchemy, tablib
CLAIM c1: PASS pip install records[pandas] ok; import records ok; records=0.6.0 pandas=3.0.5
INFO sqlalchemy=2.0.52 records=0.6.0 python=3.11.16
CLAIM c2: FAIL postgres:// -> NoSuchModuleError: Can't load plugin: sqlalchemy.dialects:postgres | postgresql:// -> ModuleNotFoundError: No module named 'psycopg2' (no server; URL scheme resolution only)
CLAIM c3: PASS rows[0]=<Record {"name": "Ada", "email": "ada@x.org", "active": 0}> attr/key/idx=('Ada', 'Ada', 'Ada') iter=['Ada', 'Henry Ford']
CLAIM c4: FAIL INSERT via db.query/bulk_query raised: OperationalError: (sqlite3.OperationalError) database is locked
CLAIM c5: FAIL t = db.transaction(); t.commit() -> AttributeError: '_GeneratorContextManager' object has no attribute 'commit' (db.transaction() returns _GeneratorContextManager)
INFO with db.transaction() as conn: INSERT persisted rows=0/1
CLAIM c6: PASS first()=<Record {"name": "Ada"}> (Record); all() -> list of 2 x Record
CLAIM c7: PASS export(csv) type=str header='name,email,active' data_rows=2
CLAIM c8: PASS export(df) -> DataFrame shape=(2, 3) cols=['name', 'email', 'active']
CLAIM c9: FAIL UNVERIFIABLE here (no MS-SQL server, no driver, network none) - escalate to human; mssql+pyodbc: dialect registered, records.Database -> ModuleNotFoundError: No module named 'pyodbc' | mssql+pymssql: dialect registered, records.Database -> ModuleNotFoundError: No module named 'pymssql'
CLAIM c10: PASS records resolved from PyPI by pip at version 0.6.0 (badge image not fetched: network none)
CLAIM c11: PASS DATABASE_URL set: rc=0 stdout='2' stderr='' | unset: rc=1 stderr='ValueError: You must provide a db_url.'

STDERR 
EXIT 0
```

## Step 3: the ONE judgment (all claims adjudicated together, from that single run)

| claim | verdict | conf | evidence excerpt |
|---|---|---|---|
| c1 | **verified** | high | CLAIM c1: PASS pip install records[pandas] ok; import records ok; records=0.6.0 pandas=3.0.5 |
| c2 | **refuted** | high | CLAIM c2: FAIL postgres:// -> NoSuchModuleError: Can't load plugin: sqlalchemy.dialects:postgres / postgresql: |
| c3 | **verified** | high | CLAIM c3: PASS rows[0]=<Record {"name": "Ada", "email": "ada@x.org", "active": 0}> attr/key/idx=('Ada', 'Ada', |
| c4 | **refuted** | low | CLAIM c4: FAIL INSERT via db.query/bulk_query raised: OperationalError: (sqlite3.OperationalError) database is |
| c5 | **refuted** | high | CLAIM c5: FAIL t = db.transaction(); t.commit() -> AttributeError: '_GeneratorContextManager' object has no at |
| c6 | **verified** | high | CLAIM c6: PASS first()=<Record {"name": "Ada"}> (Record); all() -> list of 2 x Record |
| c7 | **verified** | high | CLAIM c7: PASS export(csv) type=str header='name,email,active' data_rows=2 |
| c8 | **verified** | high | CLAIM c8: PASS export(df) -> DataFrame shape=(2, 3) cols=['name', 'email', 'active'] |
| c9 | **unverifiable** | low | CLAIM c9: FAIL UNVERIFIABLE here (no MS-SQL server, no driver, network none) - escalate to human; mssql+pyodbc |
| c10 | **verified** | low | CLAIM c10: PASS records resolved from PyPI by pip at version 0.6.0 (badge image not fetched: network none) |
| c11 | **verified** | high | CLAIM c11: PASS DATABASE_URL set: rc=0 stdout='2' stderr='' / unset: rc=1 stderr='ValueError: You must provide |

## Step 4: outcome
7 verified, 3 refuted, 1 unverifiable/escalated. Verdict accuracy vs audited truth: **0.91**. Contrast with the pipeline trajectory for the same repository in `traces/pipeline/` — where a single monolithic script stalls or mis-handles one claim, every downstream claim inherits the failure, which is the structural weakness the per-claim pipeline removes.
