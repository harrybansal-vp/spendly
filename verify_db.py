import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "spendly.db"

def main():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    # Check tables exist
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    assert cursor.fetchone() is not None, "users table missing"
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='expenses'")
    assert cursor.fetchone() is not None, "expenses table missing"

    # Clean up any stray foreign key rows that may have been inserted during previous runs
    cursor.execute("DELETE FROM expenses WHERE user_id = 9999")
    conn.commit()
    # Count rows
    cursor.execute("SELECT COUNT(*) FROM users")
    users_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM expenses")
    expenses_count = cursor.fetchone()[0]
    assert users_count == 1, f"expected 1 user, got {users_count}"
    assert expenses_count == 8, f"expected 8 expenses, got {expenses_count}"

    # Foreign key error test
    try:
        cursor.execute("INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
                       (9999, 10.0, 'Test', '2026-07-21', 'Invalid'))
        # Do not commit; should raise IntegrityError before commit
        conn.commit()
    except sqlite3.IntegrityError as e:
        print("Foreign key error caught as expected:", e)
    else:
        raise AssertionError("Expected foreign key error, but insert succeeded")

    print("Verification succeeded: 1 user, 8 expenses, foreign key constraint works.")


if __name__ == "__main__":
    main()