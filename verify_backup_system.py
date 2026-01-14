import os
import sqlite3

def verify_backup_system():
    print("=== VERIFICACIÓN DEL SISTEMA DE BACKUP ===\n")
    
    # 1. Verificar archivo .env
    print("1. VERIFICACIÓN DE ARCHIVO .ENV:")
    env_file = '.env'
    
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            content = f.read()
            print("   ✅ Archivo .env encontrado")
            print("   Contenido:")
            for line in content.strip().split('\n'):
                if line.strip():
                    print(f"   • {line}")
    else:
        print("   ❌ Archivo .env no encontrado")
    
    # 2. Verificar base de datos actual
    print("\n2. VERIFICACIÓN DE BASE DE DATOS ACTUAL:")
    main_db = "family_kitchen.db"
    
    if os.path.exists(main_db):
        conn = sqlite3.connect(main_db)
        cursor = conn.cursor()
        
        # Verificar tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print(f"   ✅ Base de datos encontrada: {len(tables)} tablas")
        
        # Contar registros en tablas principales
        main_tables = ['adults', 'children', 'recipes', 'weekly_menus', 'cleaning_tasks']
        
        for table in main_tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"   • {table}: {count} registros")
            except:
                print(f"   • {table}: No existe")
        
        conn.close()
    else:
        print("   ❌ Base de datos no encontrada")
    
    # 3. Verificar archivos de backup
    print("\n3. VERIFICACIÓN DE ARCHIVOS DE BACKUP:")
    
    import glob
    backup_files = glob.glob('*.db')
    backup_files = [f for f in backup_files if 'backup' in f or 'safety' in f]
    
    if backup_files:
        print(f"   Encontrados {len(backup_files)} archivos de backup:")
        for backup_file in backup_files:
            size = os.path.getsize(backup_file)
            print(f"   • {backup_file}: {size:,} bytes ({size/1024:.1f} KB)")
    else:
        print("   ❌ No se encontraron archivos de backup")
    
    # 4. Verificar configuración de backup
    print("\n4. VERIFICACIÓN DE CONFIGURACIÓN DE BACKUP:")
    
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
    
    # 5. Resumen
    print("\n5. RESUMEN:")
    
    has_env_config = any(backup_vars[var] for var in backup_vars if backup_vars[var])
    has_backup_files = len(backup_files) > 0
    
    print(f"   Configuración .env: {'✅' if has_env_config else '❌'}")
    print(f"   Archivos de backup: {'✅' if has_backup_files else '❌'}")
    
    if has_env_config and has_backup_files:
        print("   ✅ SISTEMA DE BACKUP CONFIGURADO")
        print("   📋 ESTADO: Listo para uso")
        print("   🔄 PRÓXIMO PASO: Reiniciar aplicación para aplicar configuración")
    else:
        print("   ⚠️ SISTEMA DE BACKUP INCOMPLETO")
        if not has_env_config:
            print("   ❌ FALTA: Configuración en .env")
        if not has_backup_files:
            print("   ❌ FALTA: Archivos de backup")

if __name__ == "__main__":
    verify_backup_system()
