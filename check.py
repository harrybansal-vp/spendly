import sqlite3
conn = sqlite3.connect('spendly.db')
rows = conn.execute('SELECT id, category, amount, date FROM expenses ORDER BY id').fetchall()
for r in rows:
    print(r)
conn.close()