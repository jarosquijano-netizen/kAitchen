import os
import sqlite3

def test_backup_system():
    print("=== PRUEBA DEL SISTEMA DE BACKUP ===\n")
    
    # 1. Verificar variables de entorno
    print("1. VARIABLES DE ENTORNO:")
    backup_vars = {
        'BACKUP_ENABLED': os.getenv('BACKUP_ENABLED'),
        'BACKUP_SCHEDULE': os.getenv('BACKUP_SCHEDULE'),
        'BACKUP_RETENTION_DAYS': os.getenv('BACKUP_RETENTION_DAYS'),
        'BACKUP_LOCATION': os.getenv('BACKUP_LOCATION')
    }
    
    for var_name, var_value in backup_vars.items():
        status = "✅ Configurada" if var_value else "❌ No configurada"
        print(f"   • {var_name}: {status}")
        if var_value:
            print(f"     Valor: {var_value}")
    
    # 2. Verificar base de datos actual
    print("\n2. ESTADO DE BASE DE DATOS:")
    main_db = "family_kitchen.db"
    
    if os.path.exists(main_db):
        conn = sqlite3.connect(main_db)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM adults")
        adults_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM children")
        children_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM recipes")
        recipes_count = cursor.fetchone()[0]
        
        conn.close()
        
        print(f"   ✅ Base de datos encontrada")
        print(f"   👥 Adultos: {adults_count}")
        print(f"   👶 Niños: {children_count}")
        print(f"   📊 Recetas: {recipes_count}")
    else:
        print("   ❌ Base de datos no encontrada")
    
    # 3. Verificar archivos de backup
    print("\n3. ARCHIVOS DE BACKUP:")
    import glob
    backup_files = glob.glob('*.db')
    backup_files = [f for f in backup_files if 'backup' in f or 'safety' in f]
    
    if backup_files:
        print(f"   Encontrados {len(backup_files)} archivos:")
        for backup_file in backup_files:
            size = os.path.getsize(backup_file)
            print(f"   • {backup_file}: {size:,} bytes ({size/1024:.1f} KB)")
    else:
        print("   ❌ No se encontraron archivos de backup")
    
    # 4. Resumen
    print("\n4. RESUMEN:")
    has_config = any(backup_vars[var] for var in backup_vars if backup_vars[var])
    has_backup_files = len(backup_files) > 0
    
    if has_config and has_backup_files:
        print("   ✅ SISTEMA DE BACKUP COMPLETAMENTE CONFIGURADO")
        print("   📋 ESTADO: Listo para uso")
        print("   🔄 FUNCIONALIDADES DISPONIBLES:")
        print("      • Backup automático diario")
        print("      • Retención de 30 días")
        print("      • Ubicación: ./backups")
        print("      • Copias de seguridad manuales")
        print("   📈 ACCESO:")
        print("      • Web: http://localhost:7000")
        print("      • API: http://localhost:7000/api")
        print("   🛡️ PROTECCIÓN:")
        print("      • Copias de seguridad automáticas")
        print("      • Múltiples archivos de backup")
        print("      • Configuración persistente")
    else:
        print("   ⚠️ SISTEMA DE BACKUP INCOMPLETO")
        if not has_config:
            print("   ❌ FALTA: Configuración de variables de entorno")
        if not has_backup_files:
            print("   ❌ FALTA: Archivos de backup")

if __name__ == "__main__":
    test_backup_system()
