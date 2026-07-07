import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DB_DIR = BASE_DIR / "database"
DB_DIR.mkdir(exist_ok=True)
DB_FILE = DB_DIR / "queue.db"


class Database:
    def __init__(self):
        self.connection = sqlite3.connect(
            DB_FILE,
            check_same_thread=False
        )
        self.connection.row_factory = sqlite3.Row
        self.create_tables()

    def create_tables(self):
        cur = self.connection.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS orders(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            number INTEGER NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL,
            finished_at TEXT,
            served_at TEXT
        )
        """)

        self.connection.commit()

    def get_next_number(self):
        cur = self.connection.cursor()

        cur.execute("""
        SELECT MAX(number)
        FROM orders
        """)

        row = cur.fetchone()

        if row[0] is None:
            return 1

        return row[0] + 1

    def create_order(self, created_at):
        number = self.get_next_number()

        cur = self.connection.cursor()

        cur.execute("""
        INSERT INTO orders(
            number,
            status,
            created_at
        )
        VALUES (?, ?, ?)
        """, (
            number,
            "waiting",
            created_at
        ))

        self.connection.commit()

        return number

    def get_waiting_orders(self):
        cur = self.connection.cursor()

        cur.execute("""
        SELECT *
        FROM orders
        WHERE status = ?
        ORDER BY number ASC
        """, (
            "waiting",
        ))

        rows = cur.fetchall()

        return [dict(row) for row in rows]


db = Database()