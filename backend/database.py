# database.py
# Member 1 — Database Setup
# This file creates audit.db with 2 tables.
# Run it ONCE: python database.py

import sqlite3

def get_db():
    """
    Returns a connection to audit.db.
    Member 2 imports this function in app.py.
    The row_factory line lets us access
    columns by name instead of index number.
    Example: row["amount"] instead of row[5]
    """
    conn = sqlite3.connect("audit.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """
    Creates both tables if they do not exist yet.
    Safe to call multiple times — uses IF NOT EXISTS
    so it will never delete existing data.
    Member 2 calls this when Flask starts up.
    """
    conn   = get_db()
    cursor = conn.cursor()

    # ── TABLE 1: transactions ─────────────────────
    # Stores the 200 raw ledger entries.
    # YOU fill this using seed_data.py.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id          TEXT PRIMARY KEY,
            date        TEXT NOT NULL,
            time        TEXT NOT NULL,
            account     TEXT NOT NULL,
            type        TEXT NOT NULL,
            amount      REAL NOT NULL,
            user        TEXT NOT NULL,
            description TEXT
        )
    """)
    print("transactions table ready")

    # ── TABLE 2: audit_results ────────────────────
    # Stores ML risk scores after analysis.
    # Member 4 fills this using analyzer.py.
    # txn_id links to transactions.id
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_results (
            txn_id      TEXT PRIMARY KEY,
            risk_score  INTEGER,
            rule_score  INTEGER,
            ml_score    INTEGER,
            flags       TEXT,
            cluster     INTEGER,
            z_score     REAL,
            is_outlier  INTEGER,
            FOREIGN KEY (txn_id)
                REFERENCES transactions(id)
        )
    """)
    print("audit_results table ready")

    conn.commit()
    conn.close()
    print("Database setup complete!")


if __name__ == "__main__":
    init_db()

    # ── Verify tables were created correctly ──────
    conn   = get_db()
    cursor = conn.cursor()

    # Show transactions columns
    cursor.execute("PRAGMA table_info(transactions)")
    cols = cursor.fetchall()
    print(f"\ntransactions table has {len(cols)} columns:")
    for col in cols:
        print(f"  {col[1]:<15} {col[2]}")

    # Show audit_results columns
    cursor.execute("PRAGMA table_info(audit_results)")
    cols = cursor.fetchall()
    print(f"\naudit_results table has {len(cols)} columns:")
    for col in cols:
        print(f"  {col[1]:<15} {col[2]}")

    conn.close()