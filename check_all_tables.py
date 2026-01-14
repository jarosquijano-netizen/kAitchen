import sqlite3

conn = sqlite3.connect('family_kitchen.db')
cursor = conn.cursor()

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
all_tables = [row[0] for row in cursor.fetchall()]

print("Todas las tablas en la base de datos:")
for table in all_tables:
    print(f"  - {table}")

print(f"\nTotal de tablas: {len(all_tables)}")

# Check specifically for cleaning tables
cleaning_tables = [table for table in all_tables if 'cleaning' in table.lower()]
print(f"\nTablas de limpieza: {cleaning_tables}")

conn.close()
