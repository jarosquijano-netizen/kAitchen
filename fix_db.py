#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sqlite3

conn = sqlite3.connect('family_kitchen.db')
cursor = conn.cursor()

# Create menu_preferences table
cursor.execute('''
CREATE TABLE IF NOT EXISTS menu_preferences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    include_weekend BOOLEAN DEFAULT 1,
    include_breakfast BOOLEAN DEFAULT 1,
    include_lunch BOOLEAN DEFAULT 1,
    include_dinner BOOLEAN DEFAULT 1,
    excluded_days TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Check if table has data
cursor.execute('SELECT COUNT(*) FROM menu_preferences')
count = cursor.fetchone()[0]

if count == 0:
    cursor.execute('''
        INSERT INTO menu_preferences 
        (include_weekend, include_breakfast, include_lunch, include_dinner, excluded_days)
        VALUES (1, 1, 1, 1, '[]')
    ''')

conn.commit()
conn.close()

print("Tabla menu_preferences creada/actualizada correctamente")
