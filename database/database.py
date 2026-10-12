import sqlite3
from pathlib import Path


class Database:
    def __init__(self, database_path: str | Path = "inventory.db"):
        self.database_path = Path(database_path)

    def connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.database_path)

    def create_tables(self) -> None:
        with self.connect() as con:
            con.execute(
                """
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    price REAL NOT NULL,
                    quantity INTEGER NOT NULL,
                    status TEXT NOT NULL
                )
                """
            )
            con.execute(
                """
                CREATE TABLE IF NOT EXISTS employees (
                    username TEXT PRIMARY KEY,
                    first_name TEXT NOT NULL,
                    password_hash TEXT NOT NULL,
                    role TEXT NOT NULL DEFAULT 'employee'
                )
                """
            )
            columns = [row[1] for row in con.execute("PRAGMA table_info(employees)")]
            if "role" not in columns:
                con.execute(
                    "ALTER TABLE employees ADD COLUMN role TEXT NOT NULL DEFAULT 'employee'"
                )
                con.execute("UPDATE employees SET role = 'admin' WHERE username = 'admin'")