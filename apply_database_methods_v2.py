# Añadir métodos de configuración de casa a la clase Database

# Método 1: Añadir al final de la clase Database
database_methods = '''
    # ==================== HOUSE CONFIGURATION ====================
    
    def save_house_config(self, config: dict) -> bool:
        """Save house configuration"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            if self.is_postgres:
                cursor.execute('''
                    INSERT INTO house_config (num_habitaciones, num_banos, num_salas, num_cocinas, 
                        superficie_total, tipo_piso, tiene_jardin, mascotas, notas_casa, updated_at)
                    VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                    ON CONFLICT (id) DO UPDATE SET
                        num_habitaciones = EXCLUDED.num_habitaciones,
                        num_banos = EXCLUDED.num_banos,
                        num_salas = EXCLUDED.num_salas,
                        num_cocinas = EXCLUDED.num_cocinas,
                        superficie_total = EXCLUDED.superficie_total,
                        tipo_piso = EXCLUDED.tipo_piso,
                        tiene_jardin = EXCLUDED.tiene_jardin,
                        mascotas = EXCLUDED.mascotas,
                        notas_casa = EXCLUDED.notas_casa,
                        updated_at = CURRENT_TIMESTAMP
                ''', (
                    config.get('num_habitaciones', 3),
                    config.get('num_banos', 2),
                    config.get('num_salas', 2),
                    config.get('num_cocinas', 1),
                    config.get('superficie_total', 120),
                    config.get('tipo_piso', 'apartamento'),
                    config.get('tiene_jardin', False),
                    config.get('mascotas', 'no'),
                    config.get('notas_casa', '')
                ))
            else:
                cursor.execute('''
                    INSERT OR REPLACE INTO house_config (id, num_habitaciones, num_banos, num_salas, num_cocinas, 
                        superficie_total, tipo_piso, tiene_jardin, mascotas, notas_casa, updated_at)
                    VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                ''', (
                    config.get('num_habitaciones', 3),
                    config.get('num_banos', 2),
                    config.get('num_salas', 2),
                    config.get('num_cocinas', 1),
                    config.get('superficie_total', 120),
                    config.get('tipo_piso', 'apartamento'),
                    config.get('tiene_jardin', False),
                    config.get('mascotas', 'no'),
                    config.get('notas_casa', '')
                ))
            
            conn.commit()
            self._close_connection(conn)
            return True
            
        except Exception as e:
            print(f"Error saving house config: {str(e)}")
            if conn:
                conn.rollback()
                self._close_connection(conn)
            return False

    def get_house_config(self) -> dict:
        """Get house configuration"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            if self.is_postgres:
                cursor.execute('''
                    SELECT * FROM house_config 
                        ORDER BY updated_at DESC 
                        LIMIT 1
                ''')
            else:
                cursor.execute('''
                    SELECT * FROM house_config 
                        ORDER BY updated_at DESC 
                        LIMIT 1
                ''')
            
            result = cursor.fetchone()
            self._close_connection(conn)
            
            if result:
                return {
                    'id': result[0],
                    'num_habitaciones': result[1],
                    'num_banos': result[2],
                    'num_salas': result[3],
                    'num_cocinas': result[4],
                    'superficie_total': result[5],
                    'tipo_piso': result[6],
                    'tiene_jardin': result[7],
                    'mascotas': result[8],
                    'notas_casa': result[9],
                    'created_at': result[10],
                    'updated_at': result[11]
                }
            else:
                # Return default configuration if no record exists
                return {
                    'num_habitaciones': 3,
                    'num_banos': 2,
                    'num_salas': 2,
                    'num_cocinas': 1,
                    'superficie_total': 120,
                    'tipo_piso': 'apartamento',
                    'tiene_jardin': False,
                    'mascotas': 'no',
                    'notas_casa': ''
                }
            
        except Exception as e:
            print(f"Error getting house config: {str(e)}")
            if conn:
                self._close_connection(conn)
            return {}
'''

# Método 2: Modificar la clase Database dinámicamente
def add_methods_to_database_class():
    """Añadir métodos de configuración de casa a la clase Database"""
    try:
        # Leer el archivo database.py
        with open('database.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Buscar dónde insertar los nuevos métodos
        insert_point = "    def get_all_family_members(self) -> List[Dict]:"
        
        if insert_point in content:
            # Insertar después del método existente
            lines = content.split('\n')
            insert_index = -1
            for i, line in enumerate(lines):
                if insert_point in line:
                    insert_index = i
                    break
            
            # Insertar los nuevos métodos
            lines.insert(insert_index + 1, database_methods)
            
            # Escribir el archivo actualizado
            with open('database.py', 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))
            
        print("✅ Métodos de configuración de casa añadidos a database.py")
        return True
        
    except Exception as e:
        print(f"Error añadiendo métodos: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔧 Aplicando métodos de configuración de casa a la clase Database...")
    if add_methods_to_database_class():
        print("✅ Métodos añadidos correctamente")
    else:
        print("❌ Error al añadir métodos")
'''

print("📋 Instrucciones:")
print("1. El servidor se reiniciará automáticamente para aplicar los cambios")
print("2. Si los cambios no se aplican, ejecuta manualmente: python -c \"import database; exec(open('database.py').read().replace('class Database:', 'class Database:' + database_methods + '\n'))\"")
print("3. Verifica que los métodos estén disponibles en: http://localhost:7000/api/house/config")
