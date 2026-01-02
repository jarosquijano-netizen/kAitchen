#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para inicializar todas las tablas de la base de datos
"""
import sqlite3

conn = sqlite3.connect('family_kitchen.db')
cursor = conn.cursor()

print("Inicializando base de datos...")

# Adults profile table
cursor.execute('''
CREATE TABLE IF NOT EXISTS adults (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    edad INTEGER,
    objetivo_alimentario TEXT,
    estilo_alimentacion TEXT,
    cocinas_favoritas TEXT,
    nivel_picante TEXT,
    ingredientes_favoritos TEXT,
    ingredientes_no_gustan TEXT,
    alergias TEXT,
    intolerancias TEXT,
    restricciones_religiosas TEXT,
    flexibilidad_comer TEXT,
    preocupacion_principal TEXT,
    tiempo_max_cocinar INTEGER,
    nivel_cocina TEXT,
    tipo_desayuno TEXT,
    le_gustan_snacks BOOLEAN,
    plato_favorito TEXT,
    plato_menos_favorito TEXT,
    comentarios TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')
print("OK: Tabla 'adults' creada")

# Children profile table
cursor.execute('''
CREATE TABLE IF NOT EXISTS children (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    edad INTEGER,
    come_solo TEXT,
    nivel_exigencia TEXT,
    cocinas_gustan TEXT,
    ingredientes_favoritos TEXT,
    ingredientes_rechaza TEXT,
    texturas_no_gustan TEXT,
    alergias TEXT,
    intolerancias TEXT,
    verduras_aceptadas TEXT,
    verduras_rechazadas TEXT,
    nivel_picante TEXT,
    desayuno_preferido TEXT,
    snacks_favoritos TEXT,
    acepta_comida_nueva TEXT,
    plato_favorito TEXT,
    plato_nunca_comeria TEXT,
    comentarios_padres TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')
print("OK: Tabla 'children' creada")

# Recipes table
cursor.execute('''
CREATE TABLE IF NOT EXISTS recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    url TEXT,
    ingredients TEXT,
    instructions TEXT,
    prep_time INTEGER,
    cook_time INTEGER,
    servings INTEGER,
    cuisine_type TEXT,
    meal_type TEXT,
    difficulty TEXT,
    image_url TEXT,
    extracted_data TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')
print("OK: Tabla 'recipes' creada")

# Weekly menus table
cursor.execute('''
CREATE TABLE IF NOT EXISTS weekly_menus (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    week_start_date DATE NOT NULL,
    menu_data TEXT,
    ai_recommendations TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')
print("OK: Tabla 'weekly_menus' creada")

# Menu preferences table
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
print("OK: Tabla 'menu_preferences' creada")

# Initialize default preferences if table is empty
cursor.execute('SELECT COUNT(*) FROM menu_preferences')
count = cursor.fetchone()[0]
if count == 0:
    cursor.execute('''
        INSERT INTO menu_preferences 
        (include_weekend, include_breakfast, include_lunch, include_dinner, excluded_days)
        VALUES (1, 1, 1, 1, '[]')
    ''')
    print("OK: Preferencias por defecto insertadas")

conn.commit()

# Verify tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print(f"\nTablas en la base de datos: {len(tables)}")
for table in tables:
    print(f"  - {table[0]}")

conn.close()
print("\nOK: Base de datos inicializada correctamente")
