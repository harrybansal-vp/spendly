import sqlite3

conn = sqlite3.connect('spendly.db')
print('Tables:', [row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")])
print('Users:', conn.execute('SELECT * FROM users').fetchall())
print('Expenses:', conn.execute('SELECT * FROM expenses').fetchall())
conn.close()