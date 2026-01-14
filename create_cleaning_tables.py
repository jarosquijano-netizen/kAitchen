import sqlite3

def create_cleaning_tables():
    print("Creando tablas de limpieza manualmente...")
    
    conn = sqlite3.connect('family_kitchen.db')
    cursor = conn.cursor()
    
    try:
        # Create cleaning_tasks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cleaning_tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                area TEXT NOT NULL,
                dificultad INTEGER DEFAULT 1 CHECK (dificultad >= 1 AND dificultad <= 5),
                frecuencia TEXT NOT NULL,
                tiempo_estimado INTEGER,
                herramientas TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("OK: Tabla 'cleaning_tasks' creada")
        
        # Create cleaning_assignments table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cleaning_assignments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id INTEGER NOT NULL,
                member_id INTEGER NOT NULL,
                member_type TEXT NOT NULL,
                dia_semana TEXT NOT NULL,
                week_start DATE NOT NULL,
                completado BOOLEAN DEFAULT FALSE,
                notas TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(task_id, member_id, week_start)
            )
        ''')
        print("OK: Tabla 'cleaning_assignments' creada")
        
        # Create cleaning_preferences table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cleaning_preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                asignacion_automatica BOOLEAN DEFAULT TRUE,
                dias_trabajo TEXT DEFAULT '[]',
                areas_preferidas TEXT DEFAULT '[]',
                areas_evitar TEXT DEFAULT '[]',
                dificultad_maxima INTEGER DEFAULT 3,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("OK: Tabla 'cleaning_preferences' creada")
        
        conn.commit()
        print("OK: Tablas de limpieza creadas exitosamente")
        
        # Verify tables were created
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%cleaning%';")
        cleaning_tables = [row[0] for row in cursor.fetchall()]
        print(f"Tablas de limpieza verificadas: {cleaning_tables}")
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    create_cleaning_tables()
