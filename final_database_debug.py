# Verificación final de la base de datos

import sqlite3
import os

def final_database_debug():
    """Verificación final de la base de datos"""
    try:
        print("🔍 VERIFICACIÓN FINAL DE LA BASE DE DATOS...")
        
        db_path = 'family_kitchen.db'
        
        print(f"📁 Ruta absoluta: {os.path.abspath(db_path)}")
        print(f"📊 Tamaño: {os.path.getsize(db_path)} bytes")
        print(f"📊 Última modificación: {os.path.getmtime(db_path)}")
        
        if os.path.exists(db_path):
            # Conectar y verificar tablas
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Verificar tablas
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            print("\n📋 TABLAS EN LA BASE DE DATOS:")
            for table in tables:
                print(f"  ✅ {table[0]}")
            
            # Verificar tablas familiares
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='adults';")
            adults_exists = cursor.fetchone()
            
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='children';")
            children_exists = cursor.fetchone()
            
            print(f"\n🔍 ESTADO DE TABLAS FAMILIARES:")
            print(f"  Tabla 'adults': {'✅ EXISTE' if adults_exists else '❌ NO EXISTE'}")
            print(f"  Tabla 'children': {'✅ EXISTE' if children_exists else '❌ NO EXISTE'}")
            
            # Verificar datos
            if adults_exists:
                cursor.execute("SELECT COUNT(*) FROM adults")
                adults_count = cursor.fetchone()[0]
                print(f"  📊 Registros en 'adults': {adults_count}")
                
                # Mostrar algunos datos
                cursor.execute("SELECT nombre, edad FROM adults LIMIT 3")
                adults_data = cursor.fetchall()
                print(f"  📊 Datos en 'adults': {adults_data}")
                
            if children_exists:
                cursor.execute("SELECT COUNT(*) FROM children")
                children_count = cursor.fetchone()[0]
                print(f"  📊 Registros en 'children': {children_count}")
                
                # Mostrar algunos datos
                cursor.execute("SELECT nombre, edad FROM children LIMIT 3")
                children_data = cursor.fetchall()
                print(f"  📊 Datos en 'children': {children_data}")
            
            conn.close()
            
            print(f"\n🎯 CONCLUSIÓN:")
            if adults_exists and children_exists:
                print("✅ Base de datos accesible correctamente")
                print("🚀 El problema debe estar en la conexión del servidor")
            else:
                print("❌ Tablas familiares no encontradas")
                
        else:
            print("❌ Base de datos no encontrada")
            
    except Exception as e:
        print(f"❌ Error en la verificación: {str(e)}")

if __name__ == "__main__":
    final_database_debug()
