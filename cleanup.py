import sqlite3
conn = sqlite3.connect('spendly.db')
conn.execute("DELETE FROM expenses WHERE category = 'Test'")
conn.commit()
print("Remaining rows:", conn.execute("SELECT COUNT(*) FROM expenses").fetchone()[0])
conn.close()