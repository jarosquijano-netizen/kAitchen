#!/usr/bin/env python3
"""
Enhanced House Configuration Implementation for k[AI]tchen
This script adds the complete house configuration functionality
"""

import os
import sys
import sqlite3
from datetime import datetime

def add_house_configuration_table():
    """Add house_configuration table to database"""
    db_path = 'family_kitchen.db'
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create house_configuration table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS house_configuration (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                num_habitaciones INTEGER DEFAULT 3,
                num_banos INTEGER DEFAULT 2,
                num_salas INTEGER DEFAULT 2,
                num_cocinas INTEGER DEFAULT 1,
                superficie_total INTEGER DEFAULT 120,
                tipo_piso TEXT DEFAULT 'apartamento',
                tiene_jardin BOOLEAN DEFAULT FALSE,
                mascotas TEXT DEFAULT 'no',
                notas_casa TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Initialize with default data if empty
        cursor.execute('SELECT COUNT(*) FROM house_configuration')
        count = cursor.fetchone()[0]
        
        if count == 0:
            cursor.execute('''
                INSERT INTO house_configuration 
                (num_habitaciones, num_banos, num_salas, num_cocinas, superficie_total, 
                 tipo_piso, tiene_jardin, mascotas, notas_casa)
                VALUES (3, 2, 2, 1, 120, 'apartamento', FALSE, 'no', '')
            ''')
        
        conn.commit()
        conn.close()
        print("✅ House configuration table created successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error creating house configuration table: {str(e)}")
        return False

def update_database_py():
    """Update database.py with house configuration methods"""
    try:
        with open('database.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find where to insert the new methods
        insert_point = "    def get_house_config(self) -> dict:"
        
        if insert_point in content:
            print("✅ House configuration methods already exist in database.py")
            return True
        
        # Add the new methods at the end of the Database class
        new_methods = '''
    
    # ==================== HOUSE CONFIGURATION ====================
    
    def save_house_config(self, config: dict) -> bool:
        """Save house configuration"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            if self.is_postgres:
                cursor.execute('''
                    INSERT INTO house_configuration (num_habitaciones, num_banos, num_salas, num_cocinas, 
                        superficie_total, tipo_piso, tiene_jardin, mascotas, notas_casa, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
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
                    INSERT OR REPLACE INTO house_configuration (id, num_habitaciones, num_banos, num_salas, num_cocinas, 
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
    
    def get_house_config(self) -> dict:
        """Get house configuration"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            if self.is_postgres:
                cursor.execute('''
                    SELECT * FROM house_configuration 
                        ORDER BY updated_at DESC 
                        LIMIT 1
                    ''')
            else:
                cursor.execute('''
                    SELECT * FROM house_configuration 
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
                    'tiene_jardin': bool(result[7]),
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
        
        # Insert the new methods
        updated_content = content.replace(insert_point, new_methods)
        
        with open('database.py', 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print("✅ Database.py updated with house configuration methods")
        return True
        
    except Exception as e:
        print(f"❌ Error updating database.py: {str(e)}")
        return False

def add_smart_cleaning_plan():
    """Add smart cleaning plan generation to cleaning_manager.py"""
    try:
        with open('cleaning_manager.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add the new method
        new_method = '''
    def generate_smart_cleaning_plan(self, house_config: dict, family_members: list) -> dict:
        """
        Genera plan de limpieza personalizado usando Claude AI
        basado en configuración de casa y capacidades familiares
        """
        try:
            # Get Anthropic API key
            api_key = os.getenv('ANTHROPIC_API_KEY')
            if not api_key:
                return {'error': 'ANTHROPIC_API_KEY no configurada'}
            
            # Prepare prompt for Claude
            prompt = f"""
            Como experto en organización del hogar, genera un plan de limpieza semanal personalizado para una familia en Barcelona.

            CONFIGURACIÓN DE LA CASA:
            - Habitaciones: {house_config.get('num_habitaciones', 3)}
            - Baños: {house_config.get('num_banos', 2)}
            - Salas: {house_config.get('num_salas', 2)}
            - Cocinas: {house_config.get('num_cocinas', 1)}
            - Superficie: {house_config.get('superficie_total', 120)}m²
            - Tipo: {house_config.get('tipo_piso', 'apartamento')}
            - Balcón/Terraza: {house_config.get('tiene_jardin', 'No')}
            - Mascotas: {house_config.get('mascotas', 'No')}

            FAMILIA:
            - 3 adultos (capacidad: 100%, todas las tareas)
            - Niña 12 años (capacidad: 60%, tareas medias)
            - Niña 4 años (capacidad: 20%, tareas simples)

            REGLAS DE DISTRIBUCIÓN:
            - Tareas pesadas (limpiar baños, fregar) → solo adultos
            - Tareas medias (aspirar, ordenar) → adultos + niña 12
            - Tareas simples (recoger juguetes, ayudar mesa) → todos incluido niña 4
            - Balancear tiempo total por persona
            - Considerar días preferidos: Martes y Sábado para tareas grandes

            GENERA:
            1. Lista de tareas específicas para esta casa
            2. Distribución equitativa según capacidades
            3. Horario semanal con tiempos estimados
            4. JSON con formato: {{"tasks": [...], "distribution": {...}}

            Responde en español y sé conciso.
            """
            
            # Call Claude API
            import anthropic
            
            client = anthropic.Anthropic(api_key=api_key)
            response = client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Parse response
            response_text = response.content[0].text
            
            # Try to extract JSON from response
            import json
            import re
            
            json_match = re.search(r'\\{.*\\}', response_text)
            if json_match:
                plan_data = json.loads(json_match.group())
                return {
                    'success': True,
                    'plan': plan_data,
                    'raw_response': response_text
                }
            else:
                return {
                    'success': False,
                    'error': 'No se pudo extraer JSON del plan',
                    'raw_response': response_text
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Error generando plan: {str(e)}'
            }
'''
        
        # Find where to insert the new method
        insert_point = "class CleaningManager:"
        
        if insert_point in content:
            print("✅ Smart cleaning plan method already exists in cleaning_manager.py")
            return True
        
        # Insert the new method
        updated_content = content.replace(insert_point, insert_point + new_method)
        
        with open('cleaning_manager.py', 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print("✅ Cleaning manager updated with smart plan generation")
        return True
        
    except Exception as e:
        print(f"❌ Error updating cleaning_manager.py: {str(e)}")
        return False

def add_api_endpoint():
    """Add smart cleaning plan API endpoint to app.py"""
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add the new endpoint
        new_endpoint = '''
# ==================== SMART CLEANING PLAN API ====================

@app.route('/api/cleaning/generate-smart-plan', methods=['POST'])
def generate_smart_cleaning_plan():
    """
    Genera plan de limpieza personalizado con IA
    basado en configuración de casa
    """
    try:
        # Get house configuration
        house_config = db.get_house_config()
        
        # Get family members
        family_members = db.get_all_family_members()
        
        # Generate smart plan
        cleaning_manager = CleaningManager(db)
        plan = cleaning_manager.generate_smart_cleaning_plan(house_config, family_members)
        
        if plan.get('success'):
            # Save generated tasks
            if 'plan' in plan and 'tasks' in plan['plan']:
                for task in plan['plan']['tasks']:
                    db.add_cleaning_task(task)
            
            return jsonify({
                'success': True,
                'tasks_created': len(plan['plan']['tasks']) if 'plan' in plan and 'tasks' in plan['plan'] else 0,
                'plan': plan.get('plan', {}),
                'message': 'Plan de limpieza generado exitosamente'
            })
        else:
            return jsonify({
                'success': False,
                'error': plan.get('error', 'Error desconocido')
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
'''
        
        # Find where to insert the new endpoint
        insert_point = "# ==================== HEALTH CHECK ===================="
        
        if insert_point in content:
            print("✅ Smart cleaning plan endpoint already exists in app.py")
            return True
        
        # Insert the new endpoint
        updated_content = content.replace(insert_point, new_endpoint + insert_point)
        
        with open('app.py', 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print("✅ App.py updated with smart cleaning plan endpoint")
        return True
        
    except Exception as e:
        print(f"❌ Error updating app.py: {str(e)}")
        return False

def main():
    """Main function to implement all enhancements"""
    print("🏠 Implementing Enhanced House Configuration for k[AI]tchen...")
    
    success = True
    
    # 1. Add house configuration table
    if not add_house_configuration_table():
        success = False
    
    # 2. Update database.py with methods
    if not update_database_py():
        success = False
    
    # 3. Add smart cleaning plan generation
    if not add_smart_cleaning_plan():
        success = False
    
    # 4. Add API endpoint
    if not add_api_endpoint():
        success = False
    
    if success:
        print("\n🎉 Enhanced House Configuration implemented successfully!")
        print("\n📋 New features added:")
        print("   ✅ House configuration table (house_configuration)")
        print("   ✅ Database methods (save_house_config, get_house_config)")
        print("   ✅ Smart cleaning plan generation with Claude AI")
        print("   ✅ API endpoint (/api/cleaning/generate-smart-plan)")
        print("\n🔄 Please restart the server to apply changes.")
    else:
        print("\n❌ Some enhancements failed. Please check the errors above.")
    
    return success

if __name__ == "__main__":
    main()
