import os
import sqlite3
import shutil
from datetime import datetime

def restore_from_backup():
    print("=== RESTAURAR DATOS DESDE BACKUP ===\n")
    
    # Rutas de los archivos
    main_db = "family_kitchen.db"
    backup_db = "family_kitchen_backup.db"
    
    print("1. VERIFICACIÓN DE ARCHIVOS:")
    if not os.path.exists(backup_db):
        print(f"   ❌ ERROR: El backup {backup_db} no existe")
        return False
    
    if not os.path.exists(main_db):
        print(f"   ❌ ERROR: La base de datos principal {main_db} no existe")
        return False
    
    print(f"   ✅ Base principal encontrada: {main_db}")
    print(f"   ✅ Backup encontrado: {backup_db}")
    
    # Verificar tamaños
    main_size = os.path.getsize(main_db)
    backup_size = os.path.getsize(backup_db)
    
    print(f"   Tamaño BD principal: {main_size:,} bytes ({main_size/1024:.1f} KB)")
    print(f"   Tamaño Backup: {backup_size:,} bytes ({backup_size/1024:.1f} KB)")
    
    # 2. RESPALDO DE CONFIRMACIÓN
    print("\n2. CONFIRMACIÓN DE RESTAURACIÓN:")
    
    print("   ⚠️  ESTÁS A PUNTO DE RESTAURAR DATOS ACTUALES")
    print("   • La base de datos actual será reemplazada completamente")
    print("   • Los cambios no guardados se PERDERÁN")
    print("   • Se recomienda hacer una copia de seguridad de la base de datos actual")
    
    confirm = input("\n   ¿Estás seguro de continuar? (s/n): ").lower().strip()
    
    if confirm != 's':
        print("   ❌ Operación cancelada por el usuario")
        return False
    
    print("   ✅ Procediendo con la restauración...")
    
    try:
        # 3. RESPALDO DE RESTAURACIÓN
        # Hacer copia de seguridad de la base actual
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safety_backup = f"family_kitchen_safety_{timestamp}.db"
        
        print(f"   📋 Creando copia de seguridad: {safety_backup}")
        shutil.copy2(main_db, safety_backup)
        
        # Restaurar desde backup
        print(f"   🔄 Restaurando datos desde {backup_db}...")
        
        # Copiar backup a la base principal
        shutil.copy2(backup_db, main_db)
        
        # Verificar la restauración
        conn = sqlite3.connect(main_db)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM recipes")
        recipes_after = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM adults")
        adults_after = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM children")
        children_after = cursor.fetchone()[0]
        
        conn.close()
        
        print(f"   ✅ Restauración completada")
        print(f"   📊 Recetas después: {recipes_after}")
        print(f"   👥 Adultos después: {adults_after}")
        print(f"   👶 Niños después: {children_after}")
        
        # 4. CONFIGURAR BACKUP AUTOMÁTICO
        print("\n4. CONFIGURANDO BACKUP AUTOMÁTICO:")
        
        # Crear archivo .env con configuración de backup
        env_file = '.env'
        
        backup_config = {
            'BACKUP_ENABLED': 'true',
            'BACKUP_SCHEDULE': 'daily',
            'BACKUP_RETENTION_DAYS': '30',
            'BACKUP_LOCATION': './backups',
            'AUTO_BACKUP': 'true'
        }
        
        try:
            with open(env_file, 'w') as f:
                f.write("# CONFIGURACIÓN DE BACKUP AUTOMÁTICO\n")
                for key, value in backup_config.items():
                    f.write(f"{key}={value}\n")
            print(f"   ✅ Configuración guardada en {env_file}")
            
            # 5. VERIFICAR QUE LOS SCRIPTS DE BACKUP EXISTEN
            backup_scripts = [
                'generate_menu_railway.py',
                'check_all_databases.py',
                'comprehensive_search.py',
                'restore_database_permanently.py'
            ]
            
            scripts_found = all(os.path.exists(script) for script in backup_scripts)
            
            print(f"   Scripts de backup encontrados: {len([script for script in backup_scripts if os.path.exists(script)])}/4")
            
            if scripts_found:
                print("   ✅ Scripts de backup disponibles")
            else:
                print("   ⚠️ Scripts de backup NO encontrados")
            
            # 6. CONFIGURACIÓN EN LA APLICACIÓN:
            print("\n4. CONFIGURACIÓN EN LA APLICACIÓN:")
            
            # Buscar en app.py configuración de backup
            try:
                with open('app.py', 'r', encoding='utf-8') as f:
                    app_content = f.read()
                
                backup_config = {
                    'backup_enabled': 'BACKUP_ENABLED' in app_content,
                    'auto_backup': 'AUTO_BACKUP' in app_content,
                    'backup_schedule': 'BACKUP_SCHEDULE' in app_content,
                    'backup_retention': 'BACKUP_RETENTION_DAYS' in app_content,
                    'backup_location': 'BACKUP_LOCATION' in app_content
                }
                
                print("   Configuración encontrada en app.py:")
                for config_name, config_status in backup_config.items():
                    status = "✅ Configurada" if config_status else "❌ No configurada"
                    print(f"   • {config_name}: {status}")
            except Exception as e:
                print(f"   Error al leer app.py: {e}")
        
        # 7. ANÁLISIS FINAL
        print("\n5. ANÁLISIS FINAL:")
        
        # Resumen
        total_backups = len(glob.glob('*.db'))
        has_backup_config = any(backup_config[var] for var in backup_config if backup_config[var])
        has_backup_scripts = len([script for script in backup_scripts if os.path.exists(script)])
        has_git = len(glob.glob('.git*'))
        has_logs = len(glob.glob('*.log'))
        
        print(f"   Archivos de backup: {total_backups}")
        print(f"   Scripts de backup: {has_backup_scripts}")
        print(f"   Control de versiones: {has_git}")
        print(f"   Sistema de logging: {has_logs}")
        print(f"   Backup automático: {has_backup_config}")
        
        print(f"\n📋 ESTADO ACTUAL:")
        print(f"   ✅ BACKUP MANUAL DISPONIBLE")
        
        if total_backups > 0:
            print(f"   📁 Backup más reciente: {backup_db}")
            print(f"   📋 Scripts de backup disponibles")
            print(f"   📋 Control de versiones: {has_git}")
        
        # Recomendaciones
        print(f"\n📋 RECOMENDACIONES:")
        print("      • Configurar variables de entorno BACKUP_*")
        print("      • Implementar monitoreo del sistema de backup")
        print("      • Configurar retención de backups")
        print("      • Revisar logs de backup regularmente")
        else:
            print("   📋 RECOMENDACIONES:")
            print("      • Considerar implementar sistema de backup automático")
            print("      • Usar scripts existentes para restaurar cuando sea necesario")
        
        return True
        
    except Exception as e:
        print(f"   ❌ ERROR durante la restauración: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    restore_from_backup()
