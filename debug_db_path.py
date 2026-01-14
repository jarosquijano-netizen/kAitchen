from database import Database
import os

# Debug database path
db = Database()
print("Database URL:", repr(db.db_url))
print("Is PostgreSQL:", db.is_postgres)

if not db.is_postgres:
    db_path = db.db_url.replace('sqlite:///', '')
    print("SQLite path:", db_path)
    print("File exists:", os.path.exists(db_path))
    print("Current working directory:", os.getcwd())
    
    # Check tables
    import sqlite3
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    print("Tables:", tables)
    conn.close()
