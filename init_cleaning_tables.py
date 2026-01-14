#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Initialize cleaning tables in the database
"""

from database import Database

def main():
    print("Inicializando tablas de limpieza...")
    
    try:
        db = Database()
        
        # Force database initialization (this will create all tables including cleaning ones)
        db.init_database()
        
        print("OK: Tablas de limpieza creadas")
        
        # Check if cleaning tables exist
        import sqlite3
        conn = sqlite3.connect('family_kitchen.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%cleaning%';")
        cleaning_tables = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        print(f"Tablas de limpieza encontradas: {cleaning_tables}")
        print("OK: Base de datos de limpieza inicializada correctamente")
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    main()
