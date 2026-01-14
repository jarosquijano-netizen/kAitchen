# Verificación final de la base de datos

import sqlite3
import os

def debug_database_connection():
    """Verificación final de la conexión a la base de datos"""
    try:
        print("🔍 VERIFICACIÓN FINAL DE LA CONEXIÓN A LA BASE DE DATOS...")
        
        # Verificar qué base de datos está usando el servidor
        db_path = 'family_kitchen.db'
        
        print(f"📁 Ruta absoluta: {os.path.abspath(db_path)}")
        print(f"📊 Tamaño: {os.path.getsize(db_path)} bytes")
        
        if os.path.exists(db_path):
            # Conectar y verificar integridad
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                
                # Verificar integridad
                cursor.execute("PRAGMA integrity_check")
                integrity = cursor.fetchone()
                
                if integrity[0] == 'ok':
                    print("✅ Integridad de la base de datos: OK")
                else:
                    print(f"❌ Integridad de la base de datos: {integrity[0]}")
                
                # Verificar tablas
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                
                print("\n📋 Tablas en la base de datos:")
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
                
                # Intentar hacer una consulta simple
                if adults_exists:
                    cursor.execute("SELECT COUNT(*) FROM adults")
                    count = cursor.fetchone()[0]
                    print(f"  📊 Registros en 'adults': {count}")
                
                conn.close()
                
            except sqlite3.Error as e:
                print(f"❌ Error de conexión: {str(e)}")
                
        else:
            print("❌ Base de datos no encontrada")
            
    except Exception as e:
        print(f"❌ Error en la verificación: {str(e)}")

if __name__ == "__main__":
    debug_database_connection()
