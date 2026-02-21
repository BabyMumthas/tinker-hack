import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'database.db')


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            -- Missing Person Details
            missing_full_name TEXT NOT NULL,
            gender TEXT,
            age INTEGER,
            missing_state TEXT,
            missing_city TEXT,
            pin_code TEXT,
            missing_date TEXT,
            missing_time TEXT,
            description TEXT,

            -- Image
            image_path TEXT NOT NULL,
            embedding TEXT NOT NULL,

            -- Complainant Details
            complainant_name TEXT NOT NULL,
            relationship TEXT,
            complainant_phone TEXT NOT NULL,
            address_line1 TEXT,
            address_line2 TEXT,

            -- Case Metadata
            status TEXT DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_id INTEGER,
            author_name TEXT,
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(case_id) REFERENCES cases(id)
        );
    """)

    conn.commit()
    conn.close()
