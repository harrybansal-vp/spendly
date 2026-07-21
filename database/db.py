"""Database helper module for the Spendly application.

This module provides three public functions used throughout the
application:

``get_db``
    Returns a SQLite connection configured with ``row_factory`` set to
    :class:`sqlite3.Row` and foreign‑key enforcement enabled.

``init_db``
    Creates the ``users`` and ``expenses`` tables if they do not already
    exist.  The schema matches the specification in
    ``.vscode/specs/01-database-setup.md``.

``seed_db``
    Inserts a demo user and eight sample expenses.  The function is
    idempotent – it will not duplicate data on subsequent calls.
"""

from __future__ import annotations

import os
import sqlite3
from datetime import date, datetime
from pathlib import Path
from typing import Iterable

from werkzeug.security import generate_password_hash

# Path to the SQLite database file – located in the project root.
DB_PATH = Path(__file__).resolve().parent.parent / "spendly.db"

def close_db(conn: sqlite3.Connection) -> None:
    """Close the given SQLite connection.

    This helper is used by the Flask application teardown to ensure
    connections are properly closed after each request.
    """
    if conn:
        conn.close()


def get_db() -> sqlite3.Connection:
    """Return a SQLite connection with row factory and FK enforcement.

    The connection is created lazily; callers are responsible for closing it.
    """
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    """Create the ``users`` and ``expenses`` tables if they do not exist.

    The function is safe to call multiple times – ``IF NOT EXISTS`` guards
    against duplicate table creation.
    """
    conn = get_db()
    cursor = conn.cursor()
    cursor.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
        """
    )
    conn.commit()
    conn.close()


def _demo_user_exists(conn: sqlite3.Connection) -> bool:
    cur = conn.execute("SELECT 1 FROM users WHERE email = ?", ("demo@spendly.com",))
    return cur.fetchone() is not None


def seed_db() -> None:
    """Insert demo data if the database is empty.

    The function checks for an existing demo user and returns early if
    found.  Otherwise it inserts a single demo user and eight expenses
    covering all required categories.
    """
    conn = get_db()
    if _demo_user_exists(conn):
        conn.close()
        return

    # Insert demo user
    password_hash = generate_password_hash("demo123")
    conn.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Demo User", "demo@spendly.com", password_hash),
    )
    user_id = conn.execute("SELECT id FROM users WHERE email = ?", ("demo@spendly.com",)).fetchone()["id"]

    # Sample expenses – one per category
    categories = [
        "Food",
        "Transport",
        "Bills",
        "Health",
        "Entertainment",
        "Shopping",
        "Other",
    ]
    today = date.today()
    expenses: Iterable[tuple] = [
        (user_id, 12.50, "Food", (today.replace(day=1)).isoformat(), "Lunch"),
        (user_id, 3.75, "Transport", (today.replace(day=2)).isoformat(), "Bus fare"),
        (user_id, 45.00, "Bills", (today.replace(day=3)).isoformat(), "Electricity"),
        (user_id, 20.00, "Health", (today.replace(day=4)).isoformat(), "Medicine"),
        (user_id, 15.00, "Entertainment", (today.replace(day=5)).isoformat(), "Movie"),
        (user_id, 60.00, "Shopping", (today.replace(day=6)).isoformat(), "Clothes"),
        (user_id, 5.00, "Other", (today.replace(day=7)).isoformat(), "Misc"),
        (user_id, 8.00, "Food", (today.replace(day=8)).isoformat(), "Coffee"),
    ]
    conn.executemany(
        "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
        expenses,
    )
    conn.commit()
    conn.close()

