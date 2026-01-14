from database import Database

db = Database()
conn = db.get_connection()
cursor = conn.cursor()

# List all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("Tables in database:")
for table in tables:
    print(f"  - {table[0]}")

# Check specifically for cleaning_tasks
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='cleaning_tasks'")
cleaning_table = cursor.fetchall()
print(f"\nCleaning tasks table exists: {len(cleaning_table) > 0}")

# Check specifically for cleaning_assignments
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='cleaning_assignments'")
assignments_table = cursor.fetchall()
print(f"Cleaning assignments table exists: {len(assignments_table) > 0}")

# Check specifically for cleaning_preferences
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='cleaning_preferences'")
preferences_table = cursor.fetchall()
print(f"Cleaning preferences table exists: {len(preferences_table) > 0}")

if len(cleaning_table) == 0:
    print("\nERROR: cleaning tables were not created!")
    print("Let's check what went wrong...")
else:
    print("\nSUCCESS: cleaning tables exist")

conn.close()
