"""SQLite helpers. The database file (findit.db) is created automatically."""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "findit.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kind TEXT NOT NULL CHECK (kind IN ('lost', 'found')),
    category TEXT NOT NULL,
    color TEXT,
    brand TEXT,
    description TEXT NOT NULL,
    location TEXT NOT NULL,
    event_time TEXT NOT NULL,          -- when it was lost / found (ISO text)
    contact TEXT,                      -- lost reports only: how to reach the owner
    storage_place TEXT,                -- found items only: where it is kept
    private_detail TEXT,               -- found items only: hidden detail staff use to verify
    status TEXT NOT NULL DEFAULT 'open' CHECK (status IN ('open', 'returned', 'unclaimed')),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS claims (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lost_id INTEGER NOT NULL REFERENCES items(id),
    found_id INTEGER NOT NULL REFERENCES items(id),
    outcome TEXT NOT NULL CHECK (outcome IN ('Verified', 'Not Verified', 'Pending')),
    notes TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_conn() as conn:
        conn.executescript(SCHEMA)


def add_item(kind, category, color, brand, description, location, event_time,
             contact=None, storage_place=None, private_detail=None):
    with get_conn() as conn:
        cur = conn.execute(
            """INSERT INTO items (kind, category, color, brand, description, location,
                                  event_time, contact, storage_place, private_detail)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (kind, category, color, brand, description, location, event_time,
             contact, storage_place, private_detail),
        )
        return cur.lastrowid


def get_item(item_id):
    with get_conn() as conn:
        return conn.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()


def list_items(kind, status="open"):
    with get_conn() as conn:
        return conn.execute(
            "SELECT * FROM items WHERE kind = ? AND status = ? ORDER BY event_time DESC",
            (kind, status),
        ).fetchall()


def record_claim(lost_id, found_id, outcome, notes=""):
    """Save the staff's verification result. 'Verified' closes both records as returned."""
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO claims (lost_id, found_id, outcome, notes) VALUES (?, ?, ?, ?)",
            (lost_id, found_id, outcome, notes),
        )
        if outcome == "Verified":
            conn.execute("UPDATE items SET status = 'returned' WHERE id IN (?, ?)",
                         (lost_id, found_id))
