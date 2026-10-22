"""Optional: fill the database with the sample found reports so you can try the app.
Run once:  python seed_data.py
"""
import csv
from pathlib import Path

import db

db.init_db()
with open(Path(__file__).parent / "data" / "found_reports.csv", newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        db.add_item("found", row["category"], row["color"], row["brand"], row["description"],
                    row["location"], row["event_time"], storage_place="Faculty room",
                    private_detail="(sample data)")
print("Sample found items added.")
