import sqlite3
conn = sqlite3.connect('family_kitchen.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%cleaning%';")
tables = [row[0] for row in cursor.fetchall()]
print("Cleaning tables:", tables)

# Check all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
all_tables = [row[0] for row in cursor.fetchall()]
print("All tables:", all_tables)
conn.close()
