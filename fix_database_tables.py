# Verificar qué base de datos está usando el servidor

import sqlite3

def check_database():
    """Verificar qué base de datos está usando el servidor"""
    try:
        # Conectar a la base de datos que usa el servidor
        conn = sqlite3.connect('family_kitchen.db')
        cursor = conn.cursor()
        
        # Verificar tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print("📋 TABLAS EN LA BASE DE DATOS ACTUAL:")
        for table in tables:
            print(f"  ✅ {table[0]}")
        
        # Verificar específicamente adults y children
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='adults';")
        adults_exists = cursor.fetchone()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='children';")
        children_exists = cursor.fetchone()
        
        print(f"\n🔍 VERIFICACIÓN DE TABLAS FAMILIARES:")
        print(f"  Tabla 'adults': {'✅ EXISTE' if adults_exists else '❌ NO EXISTE'}")
        print(f"  Tabla 'children': {'✅ EXISTE' if children_exists else '❌ NO EXISTE'}")
        
        if not adults_exists:
            print("\n🔧 CREANDO TABLA 'adults'...")
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
            print("✅ Tabla 'adults' creada correctamente")
        
        if not children_exists:
            print("\n🔧 CREANDO TABLA 'children'...")
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
            print("✅ Tabla 'children' creada correctamente")
        
        conn.commit()
        conn.close()
        
        print("\n🎉 VERIFICACIÓN COMPLETADA")
        print("🔄 Reiniciando servidor...")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    check_database()
