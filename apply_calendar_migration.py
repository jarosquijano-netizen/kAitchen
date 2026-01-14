#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to apply calendar migration to cleaning_assignments table
"""

import sqlite3
import os
from datetime import datetime

def apply_migration():
    """Apply the calendar migration to the database"""
    
    # Get database path
    db_path = 'family_kitchen.db'
    
    if not os.path.exists(db_path):
        print(f"❌ Database file not found: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔄 Applying calendar migration to cleaning_assignments table...")
        
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(cleaning_assignments)")
        columns = [row[1] for row in cursor.fetchall()]
        
        # Add fecha_especifica column if it doesn't exist
        if 'fecha_especifica' not in columns:
            print("   Adding fecha_especifica column...")
            cursor.execute("ALTER TABLE cleaning_assignments ADD COLUMN fecha_especifica DATE")
        else:
            print("   ✓ fecha_especifica column already exists")
        
        # Add tipo_asignacion column if it doesn't exist
        if 'tipo_asignacion' not in columns:
            print("   Adding tipo_asignacion column...")
            cursor.execute("ALTER TABLE cleaning_assignments ADD COLUMN tipo_asignacion TEXT DEFAULT 'semanal'")
        else:
            print("   ✓ tipo_asignacion column already exists")
        
        # Add semana_referencia column if it doesn't exist
        if 'semana_referencia' not in columns:
            print("   Adding semana_referencia column...")
            cursor.execute("ALTER TABLE cleaning_assignments ADD COLUMN semana_referencia DATE")
        else:
            print("   ✓ semana_referencia column already exists")
        
        # Update existing records
        print("   Updating existing records...")
        cursor.execute("""
            UPDATE cleaning_assignments SET 
                tipo_asignacion = 'semanal',
                semana_referencia = week_start,
                fecha_especifica = NULL
            WHERE tipo_asignacion IS NULL OR tipo_asignacion = ''
        """)
        
        # Create indexes
        print("   Creating indexes...")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_cleaning_assignments_fecha ON cleaning_assignments(fecha_especifica)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_cleaning_assignments_tipo ON cleaning_assignments(tipo_asignacion)")
        
        conn.commit()
        conn.close()
        
        print("✅ Calendar migration applied successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error applying migration: {e}")
        return False

if __name__ == "__main__":
    apply_migration()
