# House Configuration Methods - to be added at the end of database.py

def save_house_config(self, config: Dict) -> bool:
    """Save house configuration"""
    conn = self.get_connection()
    cursor = conn.cursor()
    
    try:
        if self.is_postgres:
            cursor.execute('''
                INSERT INTO house_config (num_habitaciones, num_banos, num_salas, num_cocinas, 
                    superficie_total, tipo_piso, tiene_jardin, mascotas, notas_casa, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
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
                config.get('tiene_jardin', 'no'),
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
                config.get('tiene_jardin', 'no'),
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

def get_house_config(self) -> Dict:
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
                'tiene_jardin': 'no',
                'mascotas': 'no',
                'notas_casa': ''
            }
            
    except Exception as e:
        print(f"Error getting house config: {str(e)}")
        if conn:
            self._close_connection(conn)
        return {}
