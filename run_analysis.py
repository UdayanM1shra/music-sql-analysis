# sets up the sqlite db, loads csvs, runs queries
# usage:
#python3 run_analysis.py           # run all queries
#python3 run_analysis.py --query 3 # run just query 3
#python3 run_analysis.py --setup   # rebuild db only

import sqlite3
import csv
import sys
import argparse
from pathlib import Path

ROOT = Path(__file__).parent
DB_PATH = ROOT / "music.db"
DATA_DIR = ROOT / "data"
SQL_DIR = ROOT / "sql"


def setup_database():
    if DB_PATH.exists():
        DB_PATH.unlink()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    schema = (SQL_DIR / "00_schema.sql").read_text()
    cur.executescript(schema)

    # load tables in order so foreign keys are satisfied
    for table in ("artists", "songs", "users", "plays"):
        with open(DATA_DIR / f"{table}.csv") as f:
            reader = csv.reader(f)
            headers = next(reader)
            rows = list(reader)
            placeholders = ",".join(["?"] * len(headers))
            cur.executemany(
                f"INSERT INTO {table} ({','.join(headers)}) VALUES ({placeholders})",
                rows,
            )
            print(f"  loaded {len(rows):,} rows into {table}")

    conn.commit()
    conn.close()
    print(f"database ready: {DB_PATH}")


def run_query(query_num):
    sql_files = sorted(SQL_DIR.glob("[0-9][0-9]_*.sql"))
    sql_files = [f for f in sql_files if not f.name.startswith("00_")]

    if query_num is not None:
        sql_files = [f for f in sql_files
                     if f.name.startswith(f"{query_num:02d}_")]
        if not sql_files:
            print(f"no query {query_num} found.")
            return

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    for sf in sql_files:
        title = sf.stem.replace("_", " ")
        print(f"\n{'=' * 70}")
        print(f"  {title}")
        print('=' * 70)

        sql = sf.read_text()
        try:
            cur.execute(sql)
        except sqlite3.Error as e:
            print(f"  error: {e}")
            continue

        cols = [d[0] for d in cur.description]
        rows = cur.fetchall()

        widths = [max(len(str(c)), max((len(str(r[i])) for r in rows),
                                       default=0)) for i, c in enumerate(cols)]
        line = " | ".join(c.ljust(widths[i]) for i, c in enumerate(cols))
        print("  " + line)
        print("  " + "-" * len(line))
        for r in rows:
            print("  " + " | ".join(str(r[i]).ljust(widths[i])
                                    for i in range(len(cols))))
        print(f"  ({len(rows)} rows)")

    conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--setup", action="store_true")
    parser.add_argument("--query", type=int, default=None)
    args = parser.parse_args()

    if not DB_PATH.exists() or args.setup:
        print("setting up database...")
        setup_database()

    if args.setup:
        sys.exit(0)

    run_query(args.query)
