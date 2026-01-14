# Verificación de base de datos actual

import sqlite3
import os

def check_current_database():
    """Verificar qué base de datos está usando el servidor"""
    try:
        # Verificar qué base de datos está configurada
        db_path = 'family_kitchen.db'
        
        print("🔍 VERIFICACIÓN DE BASE DE DATOS ACTUAL:")
        print(f"📁 Ruta de la base de datos: {os.path.abspath(db_path)}")
        
        if os.path.exists(db_path):
            print(f"📊 Tamaño del archivo: {os.path.getsize(db_path)} bytes")
            
            # Conectar y verificar tablas
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Verificar todas las tablas
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            print("\n📋 TABLAS EN LA BASE DE DATOS ACTUAL:")
            for table in tables:
                print(f"  ✅ {table[0]}")
            
            # Verificar específicamente adults y children
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='adults';")
            adults_exists = cursor.fetchone()
            
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='children';")
            children_exists = cursor.fetchone()
            
            print(f"\n🔍 ESTADO DE TABLAS FAMILIARES:")
            print(f"  Tabla 'adults': {'✅ EXISTE' if adults_exists else '❌ NO EXISTE'}")
            print(f"  Tabla 'children': {'✅ EXISTE' if children_exists else '❌ NO EXISTE'}")
            
            # Verificar si hay datos en las tablas
            if adults_exists:
                cursor.execute("SELECT COUNT(*) FROM adults")
                adults_count = cursor.fetchone()[0]
                print(f"  📊 Registros en 'adults': {adults_count}")
            
            if children_exists:
                cursor.execute("SELECT COUNT(*) FROM children")
                children_count = cursor.fetchone()[0]
                print(f"  📊 Registros en 'children': {children_count}")
            
            conn.close()
            
            print(f"\n🎯 CONCLUSIÓN:")
            if adults_exists and children_exists:
                print("✅ Base de datos configurada correctamente")
                print("🚀 El servidor debería poder acceder a las tablas")
            else:
                print("❌ Base de datos con problemas")
                print("🔧 Se necesita reparación")
                
        else:
            print("❌ Base de datos no encontrada")
            
    except Exception as e:
        print(f"❌ Error verificando base de datos: {str(e)}")

if __name__ == "__main__":
    check_current_database()
