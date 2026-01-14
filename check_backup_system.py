import os
import sqlite3
import glob

def check_backup_system():
    print("=== ANÁLISIS DE SISTEMA DE BACKUP ===\n")
    
    # 1. Verificar configuración actual
    print("1. CONFIGURACIÓN ACTUAL:")
    db_url = os.getenv('DATABASE_URL', 'sqlite:///family_kitchen.db')
    print(f"   DATABASE_URL: {db_url}")
    
    # 2. Buscar archivos de backup
    print("\n2. BÚSQUEDA DE ARCHIVOS DE BACKUP:")
    
    # Patrones de archivos de backup
    backup_patterns = ['*.backup', '*.bak', '*_backup*', '*.old', 'backup_*', 'copy_*', 'dump_*']
    
    all_backup_files = []
    for pattern in backup_patterns:
        all_backup_files.extend(glob.glob(pattern))
    
    # Eliminar duplicados y ordenar
    unique_backup_files = list(set(all_backup_files))
    unique_backup_files.sort()
    
    if unique_backup_files:
        print(f"   Encontrados {len(unique_backup_files)} archivos de backup:")
        for i, backup_file in enumerate(unique_backup_files, 1):
            abs_path = os.path.abspath(backup_file)
            file_size = os.path.getsize(backup_file) if os.path.exists(backup_file) else 0
            file_date = os.path.getmtime(backup_file) if os.path.exists(backup_file) else 0
            
            # Convertir timestamp a fecha legible
            import datetime
            mod_date = datetime.datetime.fromtimestamp(file_date).strftime('%Y-%m-%d %H:%M:%S')
            
            print(f"   {i}. {backup_file}")
            print(f"      Ruta: {abs_path}")
            print(f"      Tamaño: {file_size:,} bytes ({file_size/1024:.1f} KB)")
            print(f"      Modificado: {mod_date}")
            
            # Verificar si es una base de datos válida
            try:
                conn = sqlite3.connect(backup_file)
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = cursor.fetchall()
                conn.close()
                
                if tables:
                    print(f"      Tablas: {len(tables)} tablas encontradas")
                    print(f"      Válida: ✅")
                else:
                    print(f"      Tablas: 0 tablas")
                    print(f"      Válida: ❌ (vacía o corrupta)")
            except Exception as e:
                print(f"      Error al verificar: {e}")
                print(f"      Válida: ❌")
    else:
        print("   ❌ No se encontraron archivos de backup")
    
    # 3. Verificar si hay sistema de backup automático configurado
    print("\n3. SISTEMA DE BACKUP AUTOMÁTICO:")
    
    # Variables de entorno para backup
    backup_vars = {
        'BACKUP_ENABLED': os.getenv('BACKUP_ENABLED'),
        'BACKUP_SCHEDULE': os.getenv('BACKUP_SCHEDULE'),
        'BACKUP_RETENTION_DAYS': os.getenv('BACKUP_RETENTION_DAYS'),
        'BACKUP_LOCATION': os.getenv('BACKUP_LOCATION'),
        'AUTO_BACKUP': os.getenv('AUTO_BACKUP')
    }
    
    print("   Variables de entorno:")
    for var_name, var_value in backup_vars.items():
        status = "✅ Configurada" if var_value else "❌ No configurada"
        print(f"   • {var_name}: {status}")
    
    # 4. Verificar si hay scripts de backup en el código
    print("\n4. BÚSQUEDA DE SCRIPTS DE BACKUP:")
    
    # Buscar en archivos Python
    python_files = glob.glob('*.py')
    
    backup_scripts = []
    for py_file in python_files:
        with open(py_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'backup' in content.lower() or 'dump' in content.lower() or 'export' in content.lower():
                backup_scripts.append(py_file)
    
    if backup_scripts:
        print(f"   Encontrados {len(backup_scripts)} scripts de backup:")
        for script in backup_scripts:
            print(f"   • {script}")
    else:
        print("   ❌ No se encontraron scripts de backup")
    
    # 5. Verificar configuración en la aplicación
    print("\n5. CONFIGURACIÓN EN LA APLICACIÓN:")
    
    # Buscar en app.py configuración de backup
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            app_content = f.read()
            
        backup_config = {
            'backup_enabled': 'BACKUP_ENABLED' in app_content,
            'auto_backup': 'AUTO_BACKUP' in app_content,
            'backup_schedule': 'BACKUP_SCHEDULE' in app_content,
            'backup_retention': 'BACKUP_RETENTION_DAYS' in app_content
        }
        
        print("   Configuración encontrada en app.py:")
        for config_name, config_status in backup_config.items():
            status = "✅ Configurada" if config_status else "❌ No configurada"
            print(f"   • {config_name}: {status}")
    except Exception as e:
        print(f"   Error al leer app.py: {e}")
    
    # 6. Verificar si hay sistema de copias de seguridad
    print("\n6. SISTEMA DE COPIAS DE SEGURIDAD:")
    
    # Buscar archivos .git
    git_files = glob.glob('.git*')
    
    if git_files:
        print("   ✅ Sistema de control de versiones Git encontrado")
        print(f"   Archivos Git: {len(git_files)}")
    else:
        print("   ❌ No se encontró sistema de control de versiones")
    
    # 7. Verificar si hay sistema de logging
    print("\n7. SISTEMA DE LOGGING:")
    
    log_files = glob.glob('*.log')
    
    if log_files:
        print("   ✅ Sistema de logging encontrado")
        print(f"   Archivos de log: {len(log_files)}")
    else:
        print("   ❌ No se encontraron archivos de log")
    
    # 8. Verificar si hay sistema de monitoreo
    print("\n8. SISTEMA DE MONITOREO:")
    
    # Buscar archivos que puedan ser de monitoreo
    monitor_files = glob.glob('monitor*')
    
    if monitor_files:
        print("   ✅ Sistema de monitoreo encontrado")
        print(f"   Archivos de monitoreo: {len(monitor_files)}")
    else:
        print("   ❌ No se encontró sistema de monitoreo")
    
    print("\n9. ANÁLISIS FINAL:")
    
    # Resumen
    total_backups = len(unique_backup_files)
    has_backup_config = any(backup_vars[var] for var in backup_vars if backup_vars[var])
    has_backup_scripts = len(backup_scripts) > 0
    has_git = len(git_files) > 0
    has_logs = len(log_files) > 0
    has_monitor = len(monitor_files) > 0
    
    print(f"   Archivos de backup: {total_backups}")
    print(f"   Scripts de backup: {has_backup_scripts}")
    print(f"   Control de versiones: {has_git}")
    print(f"   Sistema de logging: {has_logs}")
    print(f"   Sistema de monitoreo: {has_monitor}")
    
    # Evaluación
    if total_backups > 0:
        print("   ✅ HAY SISTEMA DE BACKUP")
    else:
        print("   ❌ NO HAY SISTEMA DE BACKUP")
    
    if has_backup_config:
        print("   ✅ BACKUP CONFIGURADO")
    else:
        print("   ⚠️ BACKUP NO CONFIGURADO")
    
    print("\n10. RECOMENDACIONES:")
    
    if total_backups == 0:
        print("   📋 RECOMENDACIONES PARA IMPLEMENTAR BACKUP:")
        print("      • Configurar variables de entorno BACKUP_*")
        print("      • Crear scripts de backup automáticos")
        print("      • Implementar sistema de copias de seguridad")
        print("      • Configurar sistema de logging de cambios")
    else:
        print("   📋 RECOMENDACIONES PARA MEJORAR BACKUP:")
        print("      • Documentar el sistema de backup actual")
        print("      • Configurar retención de backups")
        print("      • Implementar monitoreo del sistema de backup")
        print("      • Revisar logs de backup regularmente")

if __name__ == "__main__":
    check_backup_system()
