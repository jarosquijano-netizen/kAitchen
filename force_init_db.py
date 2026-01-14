# Forzar la inicialización completa de la base de datos

from database import Database

# Crear instancia de Database y forzar inicialización
print("🔧 Forzando inicialización completa de la base de datos...")

try:
    db = Database()
    print("✅ Base de datos inicializada correctamente")
    
    # Verificar tablas creadas
    conn = db.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print("\n📋 Tablas disponibles:")
    for table in tables:
        print(f"  ✅ {table[0]}")
    
    # Verificar específicamente adults y children
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='adults';")
    adults_exists = cursor.fetchone()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='children';")
    children_exists = cursor.fetchone()
    
    print(f"\n🔍 Verificación de tablas familiares:")
    print(f"  Tabla 'adults': {'✅ EXISTE' if adults_exists else '❌ NO EXISTE'}")
    print(f"  Tabla 'children': {'✅ EXISTE' if children_exists else '❌ NO EXISTE'}")
    
    conn.close()
    
    if adults_exists and children_exists:
        print("\n🎉 ¡ÉXITO! Todas las tablas están disponibles.")
        print("🔄 Reiniciando servidor...")
    else:
        print("\n❌ ERROR: Las tablas familiares no se crearon correctamente.")
    
except Exception as e:
    print(f"❌ Error: {str(e)}")

print("\n📋 Instrucciones:")
print("1. Si las tablas existen, el servidor debería funcionar correctamente")
print("2. Si no existen, ejecuta: python -c \"from database import Database; db = Database(); db.init_database()\"")
print("3. Luego reinicia el servidor: python app.py")
