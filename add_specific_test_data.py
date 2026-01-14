# Añadir datos de prueba con columnas específicas

import sqlite3

def add_specific_test_data():
    """Añadir datos de prueba con columnas específicas"""
    try:
        print("🔧 AÑADIENDO DATOS DE PRUEBA...")
        
        conn = sqlite3.connect('family_kitchen.db')
        cursor = conn.cursor()
        
        # Añadir un adulto de prueba - solo columnas obligatorias
        cursor.execute('''
            INSERT INTO adults (nombre, edad)
            VALUES (?, ?)
        ''', (
            'Juan Pérez', 35
        ))
        
        # Añadir un niño de prueba - solo columnas obligatorias
        cursor.execute('''
            INSERT INTO children (nombre, edad)
            VALUES (?, ?)
        ''', (
            'María García', 12
        ))
        
        conn.commit()
        conn.close()
        
        print("✅ Datos de prueba añadidos correctamente")
        print("📊 Adultos: 1 registro")
        print("📊 Niños: 1 registro")
        print("🚀 El servidor debería poder consultar las tablas ahora")
        
        return True
        
    except Exception as e:
        print(f"❌ Error añadiendo datos de prueba: {str(e)}")
        return False

if __name__ == "__main__":
    if add_specific_test_data():
        print("✅ Sistema listo para pruebas")
        print("📋 Prueba los endpoints:")
        print("  - curl http://localhost:7000/api/adults")
        print("  - curl http://localhost:7000/api/children")
        print("  - curl http://localhost:7000/api/house/config")
    else:
        print("❌ Error añadiendo datos de prueba")
