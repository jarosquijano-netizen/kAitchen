# Verificación y solución final de la base de datos

import sqlite3
import os

def fix_database_connection():
    """Solucionar problema de conexión a base de datos"""
    try:
        print("🔧 Verificando conexión a base de datos...")
        
        # Verificar qué base de datos está usando el servidor
        db_path = 'family_kitchen.db'
        
        if os.path.exists(db_path):
            print(f"📁 Base de datos encontrada: {db_path}")
            
            # Conectar y verificar tablas
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Verificar todas las tablas
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            print("📋 Tablas existentes:")
            for table in tables:
                print(f"  ✅ {table[0]}")
            
            # Verificar específicamente adults y children
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='adults';")
            adults_exists = cursor.fetchone()
            
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='children';")
            children_exists = cursor.fetchone()
            
            print(f"\n🔍 Estado de tablas familiares:")
            print(f"  adults: {'✅ EXISTE' if adults_exists else '❌ NO EXISTE'}")
            print(f"  children: {'✅ EXISTE' if children_exists else '❌ NO EXISTE'}")
            
            # Si no existen, crearlas
            if not adults_exists:
                print("\n🔧 Creando tabla adults...")
                cursor.execute('''
                    CREATE TABLE adults (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT NOT NULL,
                        edad INTEGER,
                        objetivo_alimentario TEXT,
                        estilo_alimentacion TEXT,
                        cocinas_favoritas TEXT,
                        nivel_picante TEXT,
                        ingredientes_favoritos TEXT,
                        ingredientes_no_gustan TEXT,
                        alergias TEXT,
                        intolerancias TEXT,
                        restricciones_religiosas TEXT,
                        flexibilidad_comer TEXT,
                        preocupacion_principal TEXT,
                        tiempo_max_cocinar INTEGER,
                        nivel_cocina TEXT,
                        tipo_desayuno TEXT,
                        le_gustan_snacks BOOLEAN,
                        plato_favorito TEXT,
                        plato_menos_favorito TEXT,
                        comentarios TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                print("✅ Tabla adults creada")
            
            if not children_exists:
                print("\n🔧 Creando tabla children...")
                cursor.execute('''
                    CREATE TABLE children (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT NOT NULL,
                        edad INTEGER,
                        come_solo TEXT,
                        nivel_exigencia TEXT,
                        cocinas_gustan TEXT,
                        ingredientes_favoritos TEXT,
                        ingredientes_rechaza TEXT,
                        texturas_no_gustan TEXT,
                        alergias TEXT,
                        intolerancias TEXT,
                        verduras_aceptadas TEXT,
                        verduras_rechazadas TEXT,
                        nivel_picante TEXT,
                        desayuno_preferido TEXT,
                        snacks_favoritos TEXT,
                        acepta_comida_nueva TEXT,
                        plato_favorito TEXT,
                        plato_nunca_comeria TEXT,
                        comentarios_padres TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                print("✅ Tabla children creada")
            
            conn.commit()
            conn.close()
            
            print("\n🎉 ¡BASE DE DATOS ARREGLADA!")
            print("🔄 Reiniciando servidor...")
            return True
        else:
            print(f"❌ Base de datos no encontrada: {db_path}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    if fix_database_connection():
        print("✅ Base de datos arreglada correctamente")
        print("🚀 El servidor debería funcionar ahora")
        print("📋 Prueba los endpoints:")
        print("  - curl http://localhost:7000/api/adults")
        print("  - curl http://localhost:7000/api/children")
        print("  - curl http://localhost:7000/api/house/config")
    else:
        print("❌ No se pudo arreglar la base de datos")
