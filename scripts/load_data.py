import sqlite3
import pandas as pd
from pathlib import Path

DB = Path(__file__).resolve().parents[1] / "data.db"


def load_csv_to_sqlite(csv_path: str, table_name: str = "claims"):
    df = pd.read_csv(csv_path)
    # normalize column names
    df.columns = [c.strip() for c in df.columns]
    conn = sqlite3.connect(str(DB))
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: load_data.py <path-to-csv>")
        raise SystemExit(1)
    load_csv_to_sqlite(sys.argv[1])
    print("Loaded CSV into data.db (table 'claims')")
