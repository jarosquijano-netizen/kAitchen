#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Crear tabla para capacidades de limpieza por tipo de miembro
"""
import sqlite3

def create_cleaning_capacity_table():
    conn = sqlite3.connect('family_kitchen.db')
    cursor = conn.cursor()
    
    # Create cleaning_capacity table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cleaning_capacity (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_type TEXT NOT NULL,  -- 'adulto' o 'niño'
            max_daily_percentage INTEGER DEFAULT 100,  -- Máximo % diario que puede hacer
            max_weekly_hours INTEGER DEFAULT 40,  -- Máximo horas semanales
            task_difficulty_max INTEGER DEFAULT 5,  -- Dificultad máxima de tareas
            preferred_areas TEXT DEFAULT '',  -- Áreas preferidas (JSON)
            can_do_complex_tasks BOOLEAN DEFAULT 0,  -- Puede hacer tareas complejas
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Insert default capacities
    default_capacities = [
        {
            'member_type': 'niño',
            'max_daily_percentage': 10,  # Los niños solo pueden hacer 10% de las tareas
            'max_weekly_hours': 10,  # Máximo 10 horas semanales
            'task_difficulty_max': 2,  # Solo tareas básicas (dificultad 1-2)
            'preferred_areas': '["habitacion", "juguetes"]',  # Tareas preferidas para niños
            'can_do_complex_tasks': 0  # No pueden hacer tareas complejas
        },
        {
            'member_type': 'adulto',
            'max_daily_percentage': 90,  # Los adultos hacen 90% de las tareas
            'max_weekly_hours': 40,  # Máximo 40 horas semanales
            'task_difficulty_max': 5,  # Pueden hacer tareas complejas (dificultad 1-5)
            'preferred_areas': '["cocina", "banos", "sala", "exterior"]',  # Todas las áreas
            'can_do_complex_tasks': 1  # Pueden hacer tareas complejas
        }
    ]
    
    # Check if capacities already exist
    cursor.execute('SELECT COUNT(*) FROM cleaning_capacity')
    count = cursor.fetchone()[0]
    
    if count == 0:
        # Insert default capacities
        for capacity in default_capacities:
            cursor.execute('''
                INSERT INTO cleaning_capacity 
                (member_type, max_daily_percentage, max_weekly_hours, task_difficulty_max, preferred_areas, can_do_complex_tasks)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                capacity['member_type'],
                capacity['max_daily_percentage'],
                capacity['max_weekly_hours'],
                capacity['task_difficulty_max'],
                capacity['preferred_areas'],
                capacity['can_do_complex_tasks']
            ))
        print('✅ Capacidades de limpieza por defecto insertadas')
    else:
        print('✅ Tabla cleaning_capacity ya existe con datos')
    
    conn.commit()
    conn.close()
    print('✅ Tabla cleaning_capacity creada correctamente')

if __name__ == "__main__":
    create_cleaning_capacity_table()
