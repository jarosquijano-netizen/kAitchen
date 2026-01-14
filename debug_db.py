import sqlite3
import os

def debug_database():
    """Debug database connection issues"""
    db_path = 'family_kitchen.db'
    
    print(f"=== DEBUGGING DATABASE: {db_path} ===")
    
    # Check if file exists
    if os.path.exists(db_path):
        print(f"✅ Database file exists: {os.path.getsize(db_path)} bytes")
    else:
        print(f"❌ Database file does not exist!")
        return
    
    # Connect and check tables
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # List all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        all_tables = cursor.fetchall()
        print(f"📋 All tables: {[t[0] for t in all_tables]}")
        
        # Check cleaning tables specifically
        cleaning_tables = [t[0] for t in all_tables if 'cleaning' in t[0]]
        print(f"🧹 Cleaning tables: {cleaning_tables}")
        
        # Check each cleaning table structure
        for table in cleaning_tables:
            cursor.execute(f"PRAGMA table_info({table})")
            columns = cursor.fetchall()
            print(f"📊 Table {table} columns: {[col[1] for col in columns]}")
            
            # Check row count
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"📈 Table {table} rows: {count}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Database error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_database()
