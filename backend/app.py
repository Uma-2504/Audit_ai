from flask import Flask, jsonify, send_file
from flask_cors import CORS
import sqlite3
import json
import csv

app = Flask(__name__)
CORS(app)

DB_NAME = "audit.db"

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/api/stats")
def stats():
    conn = get_db()
    cursor = conn.cursor()

    total = cursor.execute(
        "SELECT COUNT(*) FROM transactions"
    ).fetchone()[0]

    high = cursor.execute(
        "SELECT COUNT(*) FROM audit_results WHERE risk_score >= 80"
    ).fetchone()[0]

    medium = cursor.execute(
        "SELECT COUNT(*) FROM audit_results WHERE risk_score >= 50 AND risk_score < 80"
    ).fetchone()[0]

    outliers = cursor.execute(
        "SELECT COUNT(*) FROM audit_results WHERE is_outlier = 1"
    ).fetchone()[0]

    conn.close()

    return jsonify({
        "total": total,
        "high": high,
        "medium": medium,
        "outliers": outliers
    })
@app.route("/api/audit_results")
def audit_results():
    conn = get_db()
    cursor = conn.cursor()

    rows = cursor.execute("SELECT * FROM audit_results").fetchall()
    columns = [col[0] for col in cursor.description]

    data = []
    for row in rows:
        item = dict(zip(columns, row))
        item['flags'] = json.loads(item['flags']) if item['flags'] else []
        data.append(item)

    conn.close()
    return jsonify(data)

@app.route("/api/analyze", methods=["POST"])
def analyze():
    return jsonify({"message": "analyzer.py not ready yet"})

@app.route("/api/export")
def export_csv():
    conn = get_db()
    cursor = conn.cursor()

    rows = cursor.execute("SELECT * FROM audit_results").fetchall()
    columns = [col[0] for col in cursor.description]

    file_path = "export.csv"
    with open(file_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(columns)
        writer.writerows(rows)

    conn.close()
    return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)