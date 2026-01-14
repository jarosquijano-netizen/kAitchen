import sqlite3
import os

def check_database_location():
    """Check where the application database is located and what tables it contains"""
    
    # Check current working directory
    current_dir = os.getcwd()
    print(f"📁 Current working directory: {current_dir}")
    
    # Look for database files
    db_files = []
    for file in os.listdir(current_dir):
        if file.endswith('.db'):
            size = os.path.getsize(file)
            db_files.append((file, size))
    
    print(f"🗄️ Database files found:")
    for db_file, size in db_files:
        print(f"  - {db_file} ({size} bytes)")
    
    # Check the main database file
    main_db = 'family_kitchen.db'
    if os.path.exists(main_db):
        print(f"\n🔍 Analyzing main database: {main_db}")
        
        conn = sqlite3.connect(main_db)
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = cursor.fetchall()
        
        print(f"📋 All tables in {main_db}:")
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"  - {table_name}: {count} rows")
        
        # Specifically check for cleaning tables
        cleaning_tables = [t[0] for t in tables if 'cleaning' in t[0]]
        print(f"\n🧹 Cleaning tables found: {cleaning_tables}")
        
        if len(cleaning_tables) == 3:
            print("✅ All cleaning tables are present!")
        else:
            print(f"❌ Missing cleaning tables. Expected 3, found {len(cleaning_tables)}")
        
        conn.close()
    else:
        print(f"❌ Main database file {main_db} not found!")

if __name__ == "__main__":
    check_database_location()
