# Método save_house_config para añadir a database.py

def save_house_config(self, config: dict) -> bool:
    """Save house configuration"""
    conn = self.get_connection()
    cursor = conn.cursor()
    
    try:
        if self.is_postgres:
            cursor.execute('''
                INSERT INTO house_config (num_habitaciones, num_banos, num_salas, num_cocinas, 
                        superficie_total, tipo_piso, tiene_jardin, mascotas, notas_casa, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
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
                    VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
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

print("✅ Método save_house_config creado correctamente")
print("📋 Instrucciones:")
print("1. Copia este método y pégalo al final del archivo database.py")
print("2. Reemplaza la línea 'Database.save_house_config = save_house_config' existente")
print("3. Reinicia el servidor para que cargue el nuevo método")
