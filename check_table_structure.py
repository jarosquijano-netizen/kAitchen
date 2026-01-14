# Verificar estructura exacta de las tablas

import sqlite3

def check_table_structure():
    """Verificar estructura exacta de las tablas"""
    try:
        print("🔍 VERIFICANDO ESTRUCTURA DE TABLAS...")
        
        conn = sqlite3.connect('family_kitchen.db')
        cursor = conn.cursor()
        
        # Verificar estructura de tabla adults
        cursor.execute("PRAGMA table_info(adults)")
        adults_columns = cursor.fetchall()
        
        print("\n📋 ESTRUCTURA TABLA 'adults':")
        for col in adults_columns:
            print(f"  📊 Columna {col[1]}: {col[2]} ({col[3]})")
        
        # Verificar estructura de tabla children
        cursor.execute("PRAGMA table_info(children)")
        children_columns = cursor.fetchall()
        
        print("\n📋 ESTRUCTURA TABLA 'children':")
        for col in children_columns:
            print(f"  📊 Columna {col[1]}: {col[2]} ({col[3]})")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error verificando estructura: {str(e)}")

if __name__ == "__main__":
    check_table_structure()
