#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificar datos en la tabla de recetas
"""
import sqlite3

def check_recipes():
    conn = sqlite3.connect('family_kitchen.db')
    cursor = conn.cursor()
    
    print("🍽️  VERIFICANDO TABLA DE RECETAS")
    print("=" * 40)
    
    # Verificar si la tabla existe
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='recipes'")
    table_exists = cursor.fetchone()
    
    if not table_exists:
        print("❌ La tabla 'recipes' no existe")
        conn.close()
        return
    
    # Contar recetas
    cursor.execute("SELECT COUNT(*) FROM recipes")
    count = cursor.fetchone()[0]
    print(f"📊 Total recetas: {count}")
    
    if count > 0:
        # Verificar estructura
        cursor.execute("PRAGMA table_info(recipes)")
        columns = cursor.fetchall()
        print(f"\n🏗️  Estructura de la tabla ({len(columns)} columnas):")
        for col in columns:
            print(f"   • {col[1]}: {col[2]}")
        
        # Mostrar algunas recetas
        cursor.execute("SELECT * FROM recipes LIMIT 5")
        recipes = cursor.fetchall()
        
        print(f"\n📋 Primeras {len(recipes)} recetas:")
        for i, recipe in enumerate(recipes, 1):
            print(f"\n   {i}. ID: {recipe[0]}")
            print(f"      Título: {recipe[1] if len(recipe) > 1 else 'N/A'}")
            print(f"      URL: {recipe[2] if len(recipe) > 2 else 'N/A'}")
            if len(recipe) > 3:
                print(f"      Ingredientes: {recipe[3][:100]}..." if recipe[3] else "      Ingredientes: N/A")
    else:
        print("❌ No hay recetas guardadas")
        print("\n💡 Sugerencia: Ejecuta un script para agregar recetas de ejemplo")
    
    conn.close()

if __name__ == "__main__":
    check_recipes()
