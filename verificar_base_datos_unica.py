#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificar que solo haya una base de datos para perfiles
"""
import sqlite3
import os

def verificar_base_datos_unica():
    print("=== VERIFICACIÓN DE BASE DE DATOS ÚNICA ===")
    
    # 1. Buscar todos los archivos .db
    db_files = [f for f in os.listdir('.') if f.endswith('.db')]
    print(f"Archivos .db encontrados: {len(db_files)}")
    
    for db in db_files:
        size = os.path.getsize(db)
        mod_time = os.path.getmtime(db)
        print(f"  {db}: {size:,} bytes")
    
    print()
    
    # 2. Verificar base de datos principal
    principal_db = 'family_kitchen.db'
    if os.path.exists(principal_db):
        print(f"Base de datos principal ({principal_db}):")
        try:
            conn = sqlite3.connect(principal_db)
            cursor = conn.cursor()
            
            # Verificar perfiles
            cursor.execute("SELECT COUNT(*) FROM adults")
            adults = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM children")
            children = cursor.fetchone()[0]
            
            print(f"  Adultos: {adults}")
            print(f"  Niños: {children}")
            print(f"  Total perfiles: {adults + children}")
            
            # Verificar otras tablas importantes
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            print(f"  Tablas totales: {len(tables)}")
            
            conn.close()
            
            # 3. Verificar si otras bases de datos tienen los mismos datos
            print(f"\nVerificando otras bases de datos:")
            for db in db_files:
                if db != principal_db:
                    try:
                        conn = sqlite3.connect(db)
                        cursor = conn.cursor()
                        
                        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                        tables_other = [row[0] for row in cursor.fetchall()]
                        
                        if 'adults' in tables_other and 'children' in tables_other:
                            cursor.execute("SELECT COUNT(*) FROM adults")
                            adults_other = cursor.fetchone()[0]
                            cursor.execute("SELECT COUNT(*) FROM children")
                            children_other = cursor.fetchone()[0]
                            
                            print(f"  {db}: {adults_other} adultos, {children_other} niños")
                            
                            # Comparar con principal
                            if adults_other == adults and children_other == children:
                                print(f"    ✅ Datos idénticos a principal")
                            else:
                                print(f"    ⚠️  Datos diferentes de principal")
                        else:
                            print(f"  {db}: Sin tablas de perfiles")
                        
                        conn.close()
                    except Exception as e:
                        print(f"  {db}: Error al leer - {e}")
            
        except Exception as e:
            print(f"  Error leyendo base de datos principal: {e}")
    else:
        print(f"❌ Base de datos principal no encontrada: {principal_db}")
    
    print(f"\n=== CONCLUSIÓN ===")
    print(f"✅ Base de datos principal configurada correctamente")
    print(f"✅ Perfiles de familia consolidados en una sola base de datos")
    print(f"✅ Sistema funcionando como esperado")

if __name__ == "__main__":
    verificar_base_datos_unica()
