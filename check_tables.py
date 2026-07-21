import sqlite3

conn = sqlite3.connect('spendly.db')
tables = [row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")]
print(tables)
conn.close()