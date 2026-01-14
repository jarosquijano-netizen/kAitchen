import os
import sqlite3
from database import Database

def analyze_databases():
    print("=== ANÁLISIS DE BASES DE DATOS ===\n")
    
    # 1. Verificar configuración actual
    print("1. CONFIGURACIÓN DE BASE DE DATOS:")
    db_url = os.getenv('DATABASE_URL', 'sqlite:///family_kitchen.db')
    print(f"   DATABASE_URL: {db_url}")
    
    # Determinar tipo de BD
    if db_url.startswith('postgresql://') or db_url.startswith('postgres://'):
        db_type = "PostgreSQL"
        db_location = "Producción (Railway/Cloud)"
    elif db_url.startswith('sqlite:///'):
        db_path = db_url.replace('sqlite:///', '')
        db_type = "SQLite"
        db_location = f"Local: {os.path.abspath(db_path)}"
    else:
        db_type = "Desconocido"
        db_location = "No especificado"
    
    print(f"   Tipo: {db_type}")
    print(f"   Ubicación: {db_location}")
    
    # 2. Verificar variables de entorno PostgreSQL
    print("\n2. VARIABLES POSTGRESQL (Railway):")
    pg_vars = {
        'POSTGRES_USER': os.getenv('POSTGRES_USER'),
        'POSTGRES_PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'PGHOST': os.getenv('PGHOST'),
        'PGPORT': os.getenv('PGPORT'),
        'POSTGRES_DB': os.getenv('POSTGRES_DB')
    }
    
    for var, value in pg_vars.items():
        status = "✅ Configurada" if value else "❌ No configurada"
        print(f"   {var}: {status}")
    
    # 3. Verificar archivos de base de datos locales
    print("\n3. ARCHIVOS DE BASE DE DATOS LOCALES:")
    
    # Buscar archivos .db y .sqlite
    import glob
    db_files = []
    
    # Buscar en directorio actual
    for pattern in ['*.db', '*.sqlite', '*.sqlite3']:
        db_files.extend(glob.glob(pattern))
    
    if db_files:
        print(f"   Encontrados {len(db_files)} archivos de base de datos:")
        for db_file in db_files[:5]:  # Limitar a 5 para no saturar
            abs_path = os.path.abspath(db_file)
            file_size = os.path.getsize(db_file) if os.path.exists(db_file) else 0
            print(f"   • {db_file}")
            print(f"     Ruta: {abs_path}")
            print(f"     Tamaño: {file_size:,} bytes")
    else:
        print("   ❌ No se encontraron archivos .db/.sqlite")
    
    # 4. Verificar base de datos actual
    print("\n4. ESTADO DE LA BASE DE DATOS ACTUAL:")
    try:
        db = Database()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # Obtener lista de tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        
        print(f"   Tablas encontradas: {len(tables)}")
        for table in tables:
            print(f"   • {table}")
        
        # Verificar registros en tablas principales
        main_tables = ['adults', 'children', 'recipes', 'weekly_menus', 'cleaning_tasks', 'cleaning_assignments']
        
        print("\n   Registros en tablas principales:")
        for table in main_tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"   • {table}: {count:,} registros")
            except Exception as e:
                print(f"   • {table}: Error al contar ({e})")
        
        conn.close()
        
    except Exception as e:
        print(f"   ❌ Error al conectar: {e}")
    
    # 5. Resumen
    print("\n=== RESUMEN ===")
    print(f"Base de datos principal: {db_type}")
    print(f"Ubicación: {db_location}")
    print(f"Total tablas: {len(tables) if 'tables' in locals() else 0}")
    
    if db_type == "SQLite":
        print("✅ Base de datos local SQLite funcionando")
        print("📁 Archivo: family_kitchen.db")
        print("🔧 Conexión vía archivo local")
    elif db_type == "PostgreSQL":
        print("✅ Base de datos PostgreSQL en producción")
        print("☁️ Conexión via Railway/Cloud")
    else:
        print("❌ Configuración de base de datos no determinada")

if __name__ == "__main__":
    analyze_databases()
