# Implementation Plan for Database Setup

## Overview
This plan outlines the steps to implement the database setup as per the specifications in `.vscode/specs/01-database-setup.md`. The goal is to create a functional SQLite database with `users` and `expenses` tables, seed demo data, and integrate it into the app.

## Implementation Steps

### 1. Implement `get_db()` in `database/db.py`
- Connect to the database file (`spendly.db` or `expense_tracker.db`) in the project root.
- Set `row_factory = sqlite3.Row` for dictionary-like row access.
- Enable foreign key constraints with `PRAGMA foreign_keys = ON`.
- Return the database connection.

### 2. Implement `init_db()` in `database/db.py`
- Create `users` and `expenses` tables using `CREATE TABLE IF NOT EXISTS`.
- Ensure schema matches specifications:
  - `users`: `id`, `name`, `email`, `password_hash`, `created_at`.
  - `expenses`: `id`, `user_id`, `amount`, `category`, `date`, `description`, `created_at`.
- Safe to call multiple times without errors.

### 3. Implement `seed_db()` in `database/db.py`
- Check if `users` table already contains data to prevent duplication.
- Insert a demo user:
  - Name: `Demo User`
  - Email: `demo@spendly.com`
  - Password: Hashed using `werkzeug.security.generate_password_hash("demo123")`.
- Insert 8 sample expenses:
  - Cover all categories: Food, Transport, Bills, Health, Entertainment, Shopping, Other.
  - Dates spread across the current month.
  - At least one expense per category.
- Ensure all dates are in `YYYY-MM-DD` format.

### 4. Update `app.py`
- Import `get_db`, `init_db`, and `seed_db` from `database.db`.
- Call `init_db()` and `seed_db()` within `app.app_context()` on startup.
- Ensure the database is initialized before any routes are used.

## Dependencies
- No new packages required (uses `sqlite3` and `werkzeug.security`, already installed).

## Testing
- Verify the database file exists and is accessible.
- Check that tables are created with the correct schema.
- Confirm the demo user and 8 expenses are present.
- Test foreign key constraints by inserting an invalid `user_id`.

## Notes
- Use parameterized queries to prevent SQL injection.
- Handle errors (e.g., unique email constraint violations) gracefully.