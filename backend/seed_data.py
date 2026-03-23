# seed_data.py
# Member 1 — Sample Data Generator
# Inserts 200 realistic fake transactions
# Run AFTER database.py: python seed_data.py

import sqlite3
import random

# ── Data pools to pick from randomly ─────────────
ACCOUNTS = [
    "Revenue",
    "COGS",
    "Payroll",
    "Utilities",
    "Marketing",
    "Legal",
    "Misc Expense",
    "Capital"
]

USERS = [
    "jsmith",
    "akumar",
    "mwilson",
    "rchen",
    "patel_r",
    "batch_proc",
    "admin",      # privileged
    "SYSTEM"      # privileged
]

ENTRY_TYPES = [
    "JE",    # Journal Entry (normal)
    "AP",    # Accounts Payable (normal)
    "AR",    # Accounts Receivable (normal)
    "MJE",   # Manual Journal Entry (suspicious)
    "AUTO",  # Automated entry (normal)
    "ADJ"    # Adjustment (suspicious)
]

DESCRIPTIONS = [
    "Quarterly revenue adjustment",
    "Vendor payment processing",
    "Payroll disbursement",
    "Utility bill settlement",
    "Marketing campaign expense",
    "Legal retainer fee",
    "Miscellaneous adjustment",
    "Capital expenditure entry",
    "Manual journal correction",
    "System-generated entry",
]


def generate_one_transaction(index):
    """
    Creates one transaction with a mix of
    normal and suspicious patterns.
    """

    # ── Date: random month and day in 2024 ───────
    month = random.randint(1, 12)
    day   = random.randint(1, 28)
    txn_date = f"2024-{month:02d}-{day:02d}"

    # ── Time: mostly business hours ───────────────
    # 10% chance of suspicious late-night posting
    if random.random() < 0.10:
        hour = random.randint(22, 23)  # 10pm or 11pm
    else:
        hour = random.randint(8, 18)   # 8am to 6pm

    minute   = random.randint(0, 59)
    txn_time = f"{hour:02d}:{minute:02d}"

    # ── Amount: mostly normal, some suspicious ────
    base_amount = round(random.uniform(500, 50000), 2)

    # 12% chance: make it a round number
    if random.random() < 0.12:
        base_amount = round(base_amount / 1000) * 1000

    # 8% chance: make it very large (fraud indicator)
    if random.random() < 0.08:
        multiplier  = random.randint(10, 20)
        base_amount = base_amount * multiplier

    amount = round(base_amount, 2)

    # ── Pick account, type, user randomly ─────────
    account     = random.choice(ACCOUNTS)
    entry_type  = random.choice(ENTRY_TYPES)
    user        = random.choice(USERS)
    description = random.choice(DESCRIPTIONS)

    # ── Return as a tuple (order matches table) ───
    return (
        f"TXN-{1000 + index}",  # id
        txn_date,               # date
        txn_time,               # time
        account,                # account
        entry_type,             # type
        amount,                 # amount
        user,                   # user
        description             # description
    )


def seed():
    """
    Clears old data and inserts 200 fresh rows.
    Safe to run multiple times — starts fresh each time.
    """
    conn   = sqlite3.connect("audit.db")
    cursor = conn.cursor()

    # Clear old data first
    cursor.execute("DELETE FROM audit_results")
    cursor.execute("DELETE FROM transactions")
    print("Old data cleared")

    # Generate 200 transactions
    all_transactions = []
    for i in range(200):
        txn = generate_one_transaction(i + 1)
        all_transactions.append(txn)

    # Insert all 200 at once (faster than one by one)
    cursor.executemany("""
        INSERT INTO transactions
        (id, date, time, account,
         type, amount, user, description)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, all_transactions)

    conn.commit()

    # ── Verify insertion ──────────────────────────
    count = cursor.execute(
        "SELECT COUNT(*) FROM transactions"
    ).fetchone()[0]

    print(f"\nSuccessfully inserted {count} transactions!")

    # ── Show first 5 rows ─────────────────────────
    print("\nSample of inserted data (first 5 rows):")
    rows = cursor.execute("""
        SELECT id, date, time, account,
               type, amount, user
        FROM transactions
        LIMIT 5
    """).fetchall()

    for row in rows:
        print(f"  {row[0]}  {row[1]}  {row[2]}  "
              f"{row[3]:<12}  {row[4]}  "
              f"Rs.{row[5]:>10.0f}  {row[6]}")

    # ── Count suspicious patterns ─────────────────
    print("\nSuspicious pattern counts:")

    q1 = cursor.execute("""
        SELECT COUNT(*) FROM transactions
        WHERE CAST(substr(time,1,2) AS INTEGER) >= 22
    """).fetchone()[0]

    q2 = cursor.execute("""
        SELECT COUNT(*) FROM transactions
        WHERE CAST(substr(date,9,2) AS INTEGER) >= 28
    """).fetchone()[0]

    q3 = cursor.execute("""
        SELECT COUNT(*) FROM transactions
        WHERE amount >= 10000 AND amount % 1000 = 0
    """).fetchone()[0]

    q4 = cursor.execute("""
        SELECT COUNT(*) FROM transactions
        WHERE amount > 200000
    """).fetchone()[0]

    q5 = cursor.execute("""
        SELECT COUNT(*) FROM transactions
        WHERE type IN ('MJE','ADJ')
    """).fetchone()[0]

    q6 = cursor.execute("""
        SELECT COUNT(*) FROM transactions
        WHERE user IN ('admin','SYSTEM')
    """).fetchone()[0]

    print(f"  Late-night postings : {q1}")
    print(f"  Month-end postings  : {q2}")
    print(f"  Round numbers       : {q3}")
    print(f"  Large amounts>200K  : {q4}")
    print(f"  Manual entries      : {q5}")
    print(f"  Privileged users    : {q6}")

    conn.close()


if __name__ == "__main__":
    seed()