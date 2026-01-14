# Solución definitiva del problema de base de datos

import sqlite3
import os

def fix_server_database():
    """Solucionar problema de base de datos del servidor"""
    try:
        print("🔧 SOLUCIÓN DEFINITIVA...")
        
        # 1. Verificar base de datos actual
        db_path = 'family_kitchen.db'
        
        if os.path.exists(db_path):
            print(f"📁 Base de datos encontrada: {db_path}")
            
            # 2. Conectar y verificar
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # 3. Verificar tablas
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            print("📋 Tablas existentes:")
            for table in tables:
                print(f"  ✅ {table[0]}")
            
            # 4. Verificar tablas familiares
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='adults';")
            adults_exists = cursor.fetchone()
            
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='children';")
            children_exists = cursor.fetchone()
            
            print(f"\n🔍 Estado de tablas familiares:")
            print(f"  adults: {'✅ EXISTE' if adults_exists else '❌ NO EXISTE'}")
            print(f"  children: {'✅ EXISTE' if children_exists else '❌ NO EXISTE'}")
            
            # 5. Si las tablas existen, el problema está en la conexión del servidor
            if adults_exists and children_exists:
                print("\n🎉 ¡LAS TABLAS EXISTEN!")
                print("🔍 El problema está en la conexión del servidor")
                print("📋 Solución: Reiniciar el servidor completamente")
                print("🚀 El servidor debería funcionar después de reiniciar")
                return True
            else:
                print("\n❌ LAS TABLAS NO EXISTEN")
                print("🔧 Creando tablas...")
                
                # Crear tabla adults
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
                
                # Crear tabla children
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
                
                print("✅ Tablas creadas")
                
            conn.commit()
            conn.close()
            
            print("\n🎯 CONCLUSIÓN:")
            print("✅ Base de datos reparada")
            print("🔄 Reinicia el servidor manualmente")
            print("📋 Después de reiniciar, prueba: curl http://localhost:7000/api/adults")
            
            return True
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    fix_server_database()
