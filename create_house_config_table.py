#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Crear tabla para configuración de la casa
"""
import sqlite3

def create_house_config_table():
    conn = sqlite3.connect('family_kitchen.db')
    cursor = conn.cursor()
    
    # Create house_config table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS house_config (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            num_habitaciones INTEGER DEFAULT 3,
            num_banos INTEGER DEFAULT 2,
            num_salas INTEGER DEFAULT 2,
            num_cocinas INTEGER DEFAULT 1,
            superficie_total INTEGER DEFAULT 120,
            tipo_piso TEXT DEFAULT 'apartamento',
            tiene_jardin BOOLEAN DEFAULT 0,
            mascotas TEXT DEFAULT 'no',
            notas_casa TEXT DEFAULT '',
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Check if there's already a record
    cursor.execute('SELECT COUNT(*) FROM house_config')
    count = cursor.fetchone()[0]
    
    if count == 0:
        # Insert default configuration
        cursor.execute('''
            INSERT INTO house_config 
            (num_habitaciones, num_banos, num_salas, num_cocinas, superficie_total, tipo_piso, tiene_jardin, mascotas, notas_casa)
            VALUES (3, 2, 2, 1, 120, 'apartamento', 0, 'no', '')
        ''')
        print('✅ Configuración por defecto insertada')
    else:
        print('✅ Tabla house_config ya existe con datos')
    
    conn.commit()
    conn.close()
    print('✅ Tabla house_config creada correctamente')

if __name__ == "__main__":
    create_house_config_table()
