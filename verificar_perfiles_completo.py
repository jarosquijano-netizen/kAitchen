#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificación completa del sistema de perfiles de familia
"""
import sqlite3
import os
from datetime import datetime

def verificar_perfiles_completo():
    print("🔍 VERIFICACIÓN COMPLETA DEL SISTEMA DE PERFILES")
    print("=" * 60)
    
    # 1. Verificar base de datos principal
    print("\n1. 📁 BASE DE DATOS PRINCIPAL:")
    db_path = 'family_kitchen.db'
    if os.path.exists(db_path):
        size = os.path.getsize(db_path)
        mod_time = os.path.getmtime(db_path)
        mod_date = datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d %H:%M:%S')
        print(f"   ✅ Base de datos: {db_path}")
        print(f"   📊 Tamaño: {size:,} bytes ({size/1024:.1f} KB)")
        print(f"   📅 Modificado: {mod_date}")
    else:
        print(f"   ❌ Base de datos no encontrada: {db_path}")
        return
    
    # 2. Conectar y verificar tablas
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar tablas existentes
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        print(f"\n2. 📋 TABLAS ENCONTRADAS ({len(tables)}):")
        for table in sorted(tables):
            print(f"   ✅ {table}")
        
        # 3. Verificar tablas de perfiles
        profile_tables = ['adults', 'children']
        print(f"\n3. 👪 TABLAS DE PERFILES:")
        
        for table in profile_tables:
            if table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"   ✅ {table}: {count} registros")
            else:
                print(f"   ❌ {table}: No encontrada")
        
        # 4. Verificar estructura de perfiles
        print(f"\n4. 🏗️  ESTRUCTURA DE PERFILES:")
        
        # Estructura adults
        cursor.execute("PRAGMA table_info(adults)")
        adults_cols = cursor.fetchall()
        print(f"   📊 Tabla 'adults' ({len(adults_cols)} columnas):")
        for col in adults_cols:
            print(f"      • {col[1]}: {col[2]}")
        
        # Estructura children
        cursor.execute("PRAGMA table_info(children)")
        children_cols = cursor.fetchall()
        print(f"   📊 Tabla 'children' ({len(children_cols)} columnas):")
        for col in children_cols:
            print(f"      • {col[1]}: {col[2]}")
        
        # 5. Verificar datos de perfiles
        print(f"\n5. 👨‍👩‍👧‍👦 DATOS DE PERFILES:")
        
        # Adultos
        cursor.execute("SELECT id, nombre, edad, objetivo_alimentario FROM adults ORDER BY id")
        adults = cursor.fetchall()
        print(f"   👨‍👩‍👦 Adultos ({len(adults)}):")
        for adult in adults:
            print(f"      • ID {adult[0]}: {adult[1]} ({adult[2]} años) - {adult[3] or 'Sin objetivo'}")
        
        # Niños
        cursor.execute("SELECT id, nombre, edad, nivel_exigencia FROM children ORDER BY id")
        children = cursor.fetchall()
        print(f"   👧👦 Niños ({len(children)}):")
        for child in children:
            print(f"      • ID {child[0]}: {child[1]} ({child[2]} años) - {child[3] or 'Sin nivel'}")
        
        # 6. Verificar integridad de datos
        print(f"\n6. 🔍 INTEGRIDAD DE DATOS:")
        
        # Verificar IDs únicos
        cursor.execute("SELECT id, COUNT(*) FROM adults GROUP BY id HAVING COUNT(*) > 1")
        duplicate_adults = cursor.fetchall()
        if duplicate_adults:
            print(f"   ⚠️  Adultos con IDs duplicados: {duplicate_adults}")
        else:
            print(f"   ✅ Sin IDs duplicados en adults")
        
        cursor.execute("SELECT id, COUNT(*) FROM children GROUP BY id HAVING COUNT(*) > 1")
        duplicate_children = cursor.fetchall()
        if duplicate_children:
            print(f"   ⚠️  Niños con IDs duplicados: {duplicate_children}")
        else:
            print(f"   ✅ Sin IDs duplicados en children")
        
        # Verificar nombres no vacíos
        cursor.execute("SELECT COUNT(*) FROM adults WHERE nombre IS NULL OR nombre = ''")
        empty_names_adults = cursor.fetchone()[0]
        if empty_names_adults > 0:
            print(f"   ⚠️  Adultos con nombres vacíos: {empty_names_adults}")
        else:
            print(f"   ✅ Todos los adultos tienen nombres")
        
        cursor.execute("SELECT COUNT(*) FROM children WHERE nombre IS NULL OR nombre = ''")
        empty_names_children = cursor.fetchone()[0]
        if empty_names_children > 0:
            print(f"   ⚠️  Niños con nombres vacíos: {empty_names_children}")
        else:
            print(f"   ✅ Todos los niños tienen nombres")
        
        # 7. Resumen
        print(f"\n7. 📊 RESUMEN:")
        total_profiles = len(adults) + len(children)
        print(f"   👪 Total perfiles: {total_profiles}")
        print(f"   👨‍👩‍👦 Adultos: {len(adults)}")
        print(f"   👧👦 Niños: {len(children)}")
        print(f"   📋 Tablas totales: {len(tables)}")
        
        if total_profiles > 0:
            print(f"   ✅ Sistema de perfiles funcionando correctamente")
        else:
            print(f"   ⚠️  No hay perfiles en el sistema")
        
        conn.close()
        
    except Exception as e:
        print(f"   ❌ Error verificando base de datos: {e}")
        return
    
    print(f"\n🎉 VERIFICACIÓN COMPLETADA")

if __name__ == "__main__":
    verificar_perfiles_completo()
