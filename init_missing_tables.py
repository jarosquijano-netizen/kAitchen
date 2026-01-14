# Script para inicializar tablas faltantes en la base de datos

import sqlite3
from database import Database

def initialize_missing_tables():
    """Inicializar tablas faltantes en la base de datos"""
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect('family_kitchen.db')
        cursor = conn.cursor()
        
        # Verificar si la tabla adults existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='adults';")
        adults_exists = cursor.fetchone()
        
        if not adults_exists:
            print("🔧 Creando tabla 'adults'...")
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS adults (
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
        
        # Verificar si la tabla children existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='children';")
        children_exists = cursor.fetchone()
        
        if not children_exists:
            print("🔧 Creando tabla 'children'...")
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS children (
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
        
        # Guardar cambios
        conn.commit()
        conn.close()
        
        print("\n🎉 Tablas inicializadas correctamente!")
        print("🔄 Reiniciando servidor para aplicar cambios...")
        
    except Exception as e:
        print(f"❌ Error inicializando tablas: {str(e)}")

if __name__ == "__main__":
    initialize_missing_tables()
