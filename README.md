# CPS510 English Premier League DBMS

Streamlit GUI for an Oracle-backed English Premier League database
([`python-oracledb`](https://python-oracledb.readthedocs.io/) Thin mode).

## Assignment menu (rubric)

| Option | Status |
| --- | --- |
| **Home** | Landing page: top scorers, assists, recent matches |
| **Create Tables** | Full 3NF/BCNF schema DDL |
| **Populate Tables** | Expanded seed (20 clubs, 99 players P01–P99, fixtures/stats) |
| **Query Tables** | Five predefined advanced reports |
| **Table Browser** | Searchable view of all 9 schema tables |
| **Drop Tables** | Reserved for teammate |
| **Data Entry** | Reserved for teammate (insert/update/delete forms) |
| **Exit** | Closes the Oracle session |

## Requirements

- Python 3.10 or later
- Access to the course Oracle database (or local XE / Free)
- Streamlit + CS-public-VPN when using the school host

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

Create `.env` in the repository root (do not commit credentials):

```dotenv
ORACLE_USER=your_username
ORACLE_PASSWORD=your_password
ORACLE_DSN=orsrv1.cs.torontomu.ca:1521/orcldb
```

Start the app:

```bash
streamlit run src/epl_dbms/__main__.py
```

If the Oracle connection looks stale (empty errors / sudden disconnects),
reconnect in SQL Developer on the VPN, then refresh the Streamlit page.

## Recommended first run

1. **Create Tables**
2. **Populate Tables**
3. Open **Home** and **Table Browser**

Populate skips rows that already exist, so you can top up an older 4-club
database. For a completely clean reload, have your teammate run **Drop Tables**,
then Create → Populate.

## Project layout

```text
src/epl_dbms/
  __main__.py                 Streamlit entry + navigation
  settings.py                 .env / environment Oracle settings
  database.py                 Thin-mode connection helper
  data/seed.py                Populate Tables dataset
  repositories/
    schema.py                 CREATE TABLE statements
    populate.py               Seed insert logic
    dashboard.py              Home page queries
    browser.py                Table Browser queries
    queries.py                Query Tables reports
    clubs.py                  Legacy clubs SELECT
  ui/
    home.py                   Landing page
    browser.py                Table Browser UI
    queries.py                Query Tables UI
    schema_pages.py           Create / Populate / stubs
    styles.py                 GUI styling
```
