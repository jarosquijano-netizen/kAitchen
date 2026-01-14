import os
import sqlite3

# Force recreate database with all tables
db_path = 'family_kitchen.db'

# Remove existing database
if os.path.exists(db_path):
    os.remove(db_path)
    print(f"Removed existing database: {db_path}")

# Import and initialize database
from database import Database

print("Initializing fresh database...")
db = Database()

# Verify cleaning tables exist
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check cleaning tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'cleaning_%'")
cleaning_tables = cursor.fetchall()
print(f"Cleaning tables found: {[t[0] for t in cleaning_tables]}")

# Check if tables have data
for table_name in [t[0] for t in cleaning_tables]:
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cursor.fetchone()[0]
    print(f"Table {table_name}: {count} rows")

conn.close()
print("Database initialization complete!")
