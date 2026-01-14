# Creación manual de tablas familiares

import sqlite3

def create_family_tables():
    """Crear tablas adults y children manualmente"""
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect('family_kitchen.db')
        cursor = conn.cursor()
        
        print("🔧 Creando manualmente tabla 'adults'...")
        
        # Crear tabla adults
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
        
        print("🔧 Creando manualmente tabla 'children'...")
        
        # Crear tabla children
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
        
        # Guardar cambios
        conn.commit()
        conn.close()
        
        print("✅ Tablas 'adults' y 'children' creadas manualmente")
        print("🔄 Reiniciando servidor...")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    create_family_tables()
