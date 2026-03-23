import sqlite3
import random

conn = sqlite3.connect("audit.db")
cursor = conn.cursor()

# Get all transaction IDs
cursor.execute("SELECT id FROM transactions")
transactions = cursor.fetchall()

for txn in transactions:
    txn_id = txn[0]

    # Generate fake scores
    risk_score = random.randint(10, 100)
    rule_score = random.randint(0, 50)
    ml_score = random.randint(0, 50)

    # Decide outlier
    is_outlier = 1 if risk_score > 80 else 0

    flags = "High Amount" if risk_score > 70 else "Normal"

    cursor.execute("""
        INSERT OR REPLACE INTO audit_results 
        (txn_id, risk_score, rule_score, ml_score, flags, cluster, z_score, is_outlier)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        txn_id,
        risk_score,
        rule_score,
        ml_score,
        flags,
        random.randint(1, 3),
        round(random.uniform(-3, 3), 2),
        is_outlier
    ))

conn.commit()
conn.close()

print("Dummy audit results inserted!")