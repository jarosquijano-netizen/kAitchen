#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Check database structure
"""

import sqlite3

def check_database():
    conn = sqlite3.connect('family_kitchen.db')
    cursor = conn.cursor()
    
    # Check if weekly_menus table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='weekly_menus'")
    result = cursor.fetchone()
    print('Table weekly_menus exists:', result)
    
    if result:
        cursor.execute('PRAGMA table_info(weekly_menus)')
        columns = cursor.fetchall()
        print('Columns in weekly_menus:')
        for col in columns:
            print(f'  {col}')
    
    # Check all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print('\nAll tables in database:')
    for table in tables:
        print(f'  {table[0]}')
    
    conn.close()

if __name__ == "__main__":
    check_database()
