# Verificación de múltiples instancias y bloqueos

import sqlite3
import os
import time

def check_database_locks():
    """Verificar si hay múltiples instancias o bloqueos"""
    try:
        print("🔍 VERIFICANDO BLOQUEOS DE BASE DE DATOS...")
        
        db_path = 'family_kitchen.db'
        
        if os.path.exists(db_path):
            # Verificar si hay archivos de bloqueo
            lock_files = [f"{db_path}-wal", f"{db_path}-shm", f"{db_path}-journal"]
            
            for lock_file in lock_files:
                if os.path.exists(lock_file):
                    print(f"⚠️ Archivo de bloqueo encontrado: {lock_file}")
            
            # Verificar si hay múltiples procesos usando la base de datos
            try:
                # Intentar abrir la base de datos en modo exclusivo
                conn = sqlite3.connect(db_path, timeout=5)
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM adults")
                count = cursor.fetchone()[0]
                conn.close()
                print(f"📊 Conexión exclusiva exitosa: {count} adultos")
                
            except sqlite3.Error as e:
                print(f"❌ Error de conexión exclusiva: {str(e)}")
                
        else:
            print("❌ Base de datos no encontrada")
            
    except Exception as e:
        print(f"❌ Error verificando bloqueos: {str(e)}")

if __name__ == "__main__":
    check_database_locks()
