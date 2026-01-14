# Creación completa de base de datos nueva

from database import Database

def create_complete_database():
    """Crear base de datos completamente nueva"""
    try:
        print("🔧 Creando base de datos completamente nueva...")
        
        # Eliminar base de datos antigua si existe
        import os
        if os.path.exists('family_kitchen.db'):
            os.remove('family_kitchen.db')
            print("🗑️ Base de datos antigua eliminada")
        
        # Crear nueva instancia de Database (esto creará todas las tablas)
        db = Database()
        print("✅ Base de datos creada con todas las tablas")
        
        # Verificar que las tablas se crearon correctamente
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print("\n📋 TABLAS CREADAS:")
        for table in tables:
            print(f"  ✅ {table[0]}")
        
        # Verificar tablas familiares
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='adults';")
        adults_exists = cursor.fetchone()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='children';")
        children_exists = cursor.fetchone()
        
        print(f"\n🔍 VERIFICACIÓN FINAL:")
        print(f"  Tabla 'adults': {'✅ CREADA' if adults_exists else '❌ NO CREADA'}")
        print(f"  Tabla 'children': {'✅ CREADA' if children_exists else '❌ NO CREADA'}")
        
        conn.close()
        
        if adults_exists and children_exists:
            print("\n🎉 ¡ÉXITO! Base de datos creada correctamente")
            print("🔄 Reiniciando servidor...")
            return True
        else:
            print("\n❌ ERROR: No se pudieron crear todas las tablas")
            return False
        
    except Exception as e:
        print(f"❌ Error creando base de datos: {str(e)}")
        return False

if __name__ == "__main__":
    if create_complete_database():
        print("✅ Base de datos lista para usar")
        print("🚀 Inicia el servidor con: python app.py")
    else:
        print("❌ Error al crear base de datos")
