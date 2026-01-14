import os
import sqlite3
import glob

def check_all_databases():
    print("=== ANÁLISIS COMPLETO DE BASES DE DATOS ===\n")
    
    # 1. Verificar configuración actual
    print("1. CONFIGURACIÓN ACTUAL:")
    db_url = os.getenv('DATABASE_URL', 'sqlite:///family_kitchen.db')
    print(f"   DATABASE_URL: {db_url}")
    
    # 2. Buscar todos los archivos de bases de datos en el directorio
    print("\n2. ARCHIVOS DE BASES DE DATOS ENCONTRADOS:")
    
    # Patrones de archivos de base de datos comunes
    db_patterns = ['*.db', '*.sqlite', '*.sqlite3', '*.bak', '*.backup']
    
    all_db_files = []
    for pattern in db_patterns:
        all_db_files.extend(glob.glob(pattern))
    
    # Eliminar duplicados y ordenar
    unique_db_files = list(set(all_db_files))
    unique_db_files.sort()
    
    if unique_db_files:
        print(f"   Encontrados {len(unique_db_files)} archivos de bases de datos:")
        for i, db_file in enumerate(unique_db_files, 1):
            abs_path = os.path.abspath(db_file)
            file_size = os.path.getsize(db_file) if os.path.exists(db_file) else 0
            file_date = os.path.getmtime(db_file) if os.path.exists(db_file) else 0
            
            # Convertir timestamp a fecha legible
            import datetime
            mod_date = datetime.datetime.fromtimestamp(file_date).strftime('%Y-%m-%d %H:%M:%S')
            
            print(f"   {i}. {db_file}")
            print(f"      Ruta: {abs_path}")
            print(f"      Tamaño: {file_size:,} bytes ({file_size/1024:.1f} KB)")
            print(f"      Modificado: {mod_date}")
            
            # Verificar si es una base de datos válida (tiene tablas)
            try:
                conn = sqlite3.connect(db_file)
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
        print("   ❌ No se encontraron archivos de bases de datos")
    
    # 3. Verificar variables de entorno para otras bases de datos
    print("\n3. VARIABLES DE ENTORNO PARA OTRAS BD:")
    
    env_db_vars = {
        'DATABASE_URL': os.getenv('DATABASE_URL'),
        'POSTGRES_DB': os.getenv('POSTGRES_DB'),
        'POSTGRES_USER': os.getenv('POSTGRES_USER'),
        'POSTGRES_PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'PGHOST': os.getenv('PGHOST'),
        'PGPORT': os.getenv('PGPORT'),
        'TEST_DATABASE_URL': os.getenv('TEST_DATABASE_URL'),
        'DEV_DATABASE_URL': os.getenv('DEV_DATABASE_URL')
    }
    
    print("   Variables configuradas:")
    for var_name, var_value in env_db_vars.items():
        status = "✅ Configurada" if var_value else "❌ No configurada"
        print(f"   • {var_name}: {status}")
    
    # 4. Verificar si hay múltiples instancias de bases de datos
    print("\n4. CONEXIONES A BASES DE DATOS:")
    
    # Verificar archivos .db que podrían estar en uso
    active_db_files = []
    for db_file in unique_db_files:
        if db_file.endswith('.db') and not any(x in db_file for x in ['.backup', '.bak', '.old']):
            active_db_files.append(db_file)
    
    print(f"   Posibles bases de datos activas: {len(active_db_files)}")
    for i, db_file in enumerate(active_db_files, 1):
        print(f"   {i}. {db_file}")
        
        # Verificar cuál está conectada actualmente
        try:
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
            table_count = cursor.fetchone()[0]
            conn.close()
            
            # La base de datos actual tiene 11 tablas (según análisis anterior)
            if table_count >= 10:  # Considerar "activa" si tiene varias tablas
                print(f"      Tablas: {table_count} (posiblemente activa)")
            else:
                print(f"      Tablas: {table_count} (posiblemente inactiva)")
        except:
            print(f"      Error al verificar {db_file}")
    
    # 5. Resumen y conclusiones
    print("\n5. RESUMEN Y CONCLUSIONES:")
    
    if len(unique_db_files) == 0:
        print("   ❌ No hay archivos de base de datos en el directorio")
        print("   🤔 ESTADO: Sistema sin base de datos local")
    elif len(unique_db_files) == 1:
        print("   ✅ Hay exactamente un archivo de base de datos principal")
        print("   🏠 ESTADO: Sistema con base de datos única local")
        print("   📁 ARCHIVO PRINCIPAL: family_kitchen.db")
    else:
        print("   ⚠️ Hay múltiples archivos de base de datos")
        print("   🤔 ESTADO: Sistema con múltiples bases de datos")
        print("   📋 POSIBLES ESCENARIOS:")
        print("      • Backups automáticos del sistema")
        print("      • Exportaciones de datos manuales")
        print("      • Migraciones o actualizaciones de la base de datos")
        print("      • Copias de seguridad manuales")
    
    # 6. Verificar conexión actual
    print("\n6. ESTADO DE CONEXIÓN ACTUAL:")
    current_db_type = "SQLite" if db_url.startswith('sqlite') else "PostgreSQL" if db_url.startswith('postgres') else "Desconocido"
    print(f"   Tipo: {current_db_type}")
    print(f"   URL: {db_url}")
    
    if current_db_type == "SQLite":
        if os.path.exists("family_kitchen.db"):
            print("   ✅ Base de datos principal encontrada y accesible")
        else:
            print("   ❌ Base de datos principal no encontrada")

if __name__ == "__main__":
    check_all_databases()
