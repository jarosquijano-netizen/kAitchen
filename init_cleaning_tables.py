#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to initialize cleaning tables with calendar support
"""

import sqlite3
import os
from datetime import datetime

def init_cleaning_tables():
    """Initialize cleaning tables with calendar support"""
    
    db_path = 'family_kitchen.db'
    
    if not os.path.exists(db_path):
        print(f"❌ Database file not found: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔄 Creating cleaning tables with calendar support...")
        
        # Create cleaning_tasks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cleaning_tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                area TEXT NOT NULL,
                dificultad INTEGER DEFAULT 1 CHECK (dificultad >= 1 AND dificultad <= 5),
                frecuencia TEXT NOT NULL,
                tiempo_estimado INTEGER,
                herramientas TEXT,
                dias_semana TEXT DEFAULT '[]',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("   ✓ cleaning_tasks table created")
        
        # Create cleaning_assignments table with calendar support
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cleaning_assignments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id INTEGER NOT NULL,
                member_id INTEGER NOT NULL,
                member_type TEXT NOT NULL,
                dia_semana TEXT NOT NULL,
                week_start DATE NOT NULL,
                fecha_especifica DATE,
                tipo_asignacion TEXT DEFAULT 'semanal',
                semana_referencia DATE,
                completado BOOLEAN DEFAULT FALSE,
                notas TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(task_id, member_id, week_start)
            )
        ''')
        print("   ✓ cleaning_assignments table created with calendar support")
        
        # Create cleaning_preferences table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cleaning_preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                asignacion_automatica BOOLEAN DEFAULT TRUE,
                dias_trabajo TEXT DEFAULT '[]',
                areas_preferidas TEXT DEFAULT '[]',
                areas_evitar TEXT DEFAULT '[]',
                dificultad_maxima INTEGER DEFAULT 3,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("   ✓ cleaning_preferences table created")
        
        # Create indexes for better performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_cleaning_assignments_fecha ON cleaning_assignments(fecha_especifica)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_cleaning_assignments_tipo ON cleaning_assignments(tipo_asignacion)")
        print("   ✓ Indexes created")
        
        # Initialize default preferences if empty
        cursor.execute('SELECT COUNT(*) FROM cleaning_preferences')
        count = cursor.fetchone()[0]
        if count == 0:
            cursor.execute('''
                INSERT INTO cleaning_preferences 
                (asignacion_automatica, dias_trabajo, areas_preferidas, areas_evitar, dificultad_maxima)
                VALUES (1, '["martes", "sábado"]', '[]', '[]', 3)
            ''')
            print("   ✓ Default preferences initialized")
        
        conn.commit()
        conn.close()
        
        print("✅ Cleaning tables with calendar support initialized successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error initializing cleaning tables: {e}")
        return False

if __name__ == "__main__":
    init_cleaning_tables()
