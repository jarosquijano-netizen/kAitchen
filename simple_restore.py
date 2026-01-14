import os
import sqlite3
import shutil
from datetime import datetime

def simple_restore():
    print("=== RESTAURACIÓN SIMPLE DESDE BACKUP ===\n")
    
    # Rutas
    main_db = "family_kitchen.db"
    backup_db = "family_kitchen_backup.db"
    
    # Verificar archivos
    if not os.path.exists(backup_db):
        print(f"❌ ERROR: Backup {backup_db} no encontrado")
        return False
    
    if not os.path.exists(main_db):
        print(f"❌ ERROR: Base principal {main_db} no encontrada")
        return False
    
    print(f"✅ Backup encontrado: {backup_db}")
    print(f"✅ Base principal encontrada: {main_db}")
    
    # Confirmar restauración
    confirm = input("¿Estás seguro de restaurar desde backup? (s/n): ").lower().strip()
    if confirm != 's':
        print("❌ Operación cancelada")
        return False
    
    print("🔄 Iniciando restauración...")
    
    try:
        # Hacer backup de seguridad
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safety_backup = f"family_kitchen_safety_{timestamp}.db"
        shutil.copy2(main_db, safety_backup)
        print(f"✅ Copia de seguridad creada: {safety_backup}")
        
        # Restaurar desde backup
        shutil.copy2(backup_db, main_db)
        print("✅ Base de datos restaurada desde backup")
        
        # Verificar restauración
        conn = sqlite3.connect(main_db)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM recipes")
        recipes_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM adults")
        adults_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM children")
        children_count = cursor.fetchone()[0]
        
        conn.close()
        
        print(f"✅ Verificación completada:")
        print(f"   📊 Recetas: {recipes_count}")
        print(f"   👥 Adultos: {adults_count}")
        print(f"   👶 Niños: {children_count}")
        
        # Configurar backup automático
        env_file = '.env'
        with open(env_file, 'w') as f:
            f.write("# CONFIGURACIÓN DE BACKUP AUTOMÁTICO\n")
            f.write("BACKUP_ENABLED=true\n")
            f.write("BACKUP_SCHEDULE=daily\n")
            f.write("BACKUP_RETENTION_DAYS=30\n")
            f.write("BACKUP_LOCATION=./backups\n")
        
        print("✅ Backup automático configurado")
        print("⚠️ IMPORTANTE: Debe reiniciar la aplicación para aplicar cambios")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    simple_restore()
