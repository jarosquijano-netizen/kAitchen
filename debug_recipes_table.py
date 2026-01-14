import sqlite3

conn = sqlite3.connect('family_kitchen.db')
cursor = conn.cursor()

# Check table structure
print("=== RECIPES TABLE STRUCTURE ===")
cursor.execute("PRAGMA table_info(recipes)")
columns = cursor.fetchall()
for col in columns:
    print(f"Column: {col}")

# Check actual data
print("\n=== ACTUAL DATA IN RECIPES ===")
cursor.execute("SELECT * FROM recipes LIMIT 3")
rows = cursor.fetchall()

for row in rows:
    print(f"Row: {row}")
    print(f"Row type: {type(row)}")
    if isinstance(row, sqlite3.Row):
        print(f"Row keys: {row.keys()}")

conn.close()
