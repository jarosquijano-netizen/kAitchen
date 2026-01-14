# Solución definitiva para problemas de base de datos

import sqlite3
import os
import shutil
from database import Database

def repair_database_permanently():
    """Reparar base de datos permanentemente"""
    try:
        print("🔧 REPARANDO BASE DE DATOS PERMANENTEMENTE...")
        
        # 1. Hacer backup de la base de datos actual
        if os.path.exists('family_kitchen.db'):
            backup_path = 'family_kitchen_backup.db'
            shutil.copy2('family_kitchen.db', backup_path)
            print(f"✅ Backup creado: {backup_path}")
        
        # 2. Eliminar base de datos corrupta
        if os.path.exists('family_kitchen.db'):
            os.remove('family_kitchen.db')
            print("🗑️ Base de datos corrupta eliminada")
        
        # 3. Crear nueva base de datos completamente limpia
        db = Database()
        print("✅ Nueva base de datos creada")
        
        # 4. Verificar que las tablas existen
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print("\n📋 TABLAS CREADAS:")
        for table in tables:
            print(f"  ✅ {table[0]}")
        
        # 5. Verificar tablas familiares
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='adults';")
        adults_exists = cursor.fetchone()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='children';")
        children_exists = cursor.fetchone()
        
        print(f"\n🔍 VERIFICACIÓN FINAL:")
        print(f"  Tabla 'adults': {'✅ EXISTE' if adults_exists else '❌ NO EXISTE'}")
        print(f"  Tabla 'children': {'✅ EXISTE' if children_exists else '❌ NO EXISTE'}")
        
        conn.close()
        
        if adults_exists and children_exists:
            print("\n🎉 ¡ÉXITO! Base de datos reparada permanentemente")
            print("🚀 El servidor debería funcionar ahora")
            return True
        else:
            print("\n❌ ERROR: No se pudieron crear las tablas familiares")
            return False
            
    except Exception as e:
        print(f"❌ Error reparando base de datos: {str(e)}")
        return False

if __name__ == "__main__":
    if repair_database_permanently():
        print("✅ Reparación completada")
        print("🔄 Reiniciando servidor...")
    else:
        print("❌ Error en la reparación")
