# Añadir datos de prueba con estructura correcta

import sqlite3

def add_test_data_correct():
    """Añadir datos de prueba con el número correcto de columnas"""
    try:
        print("🔧 AÑADIENDO DATOS DE PRUEBA...")
        
        conn = sqlite3.connect('family_kitchen.db')
        cursor = conn.cursor()
        
        # Añadir un adulto de prueba con todas las columnas
        cursor.execute('''
            INSERT INTO adults (id, nombre, edad, objetivo_alimentario, estilo_alimentacion, 
                cocinas_favoritas, nivel_picante, ingredientes_favoritos, ingredientes_no_gustan,
                alergias, intolerancias, restricciones_religiosas, flexibilidad_comer,
                preocupacion_principal, tiempo_max_cocinar, nivel_cocina, tipo_desayuno,
                le_gustan_snacks, plato_favorito, plato_menos_favorito, comentarios, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ''', (
            1, 'Juan Pérez', 35, 'Mantener peso', 'Mediterráneo', 
            'Italiana, Mexicana', 'Medio', 'Pasta, Pizza',
            'Ninguna', 'Lactosa', 'Ninguna', 'Católico',
            'Flexible', 'Trabajo', '30 minutos', 'Medio', 'Continental',
            'Sí', 'Lasaña', 'Pizza', 'Ensalada'
        ))
        
        # Añadir un niño de prueba con todas las columnas
        cursor.execute('''
            INSERT INTO children (id, nombre, edad, come_solo, nivel_exigencia, cocinas_gustan,
                ingredientes_favoritos, ingredientes_rechaza, texturas_no_gustan, alergias,
                intolerancias, verduras_aceptadas, verduras_rechazadas, nivel_picante,
                desayuno_preferido, snacks_favoritos, acepta_comida_nueva,
                plato_favorito, plato_nunca_comeria, comentarios_padres, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ''', (
            1, 'María García', 12, 'Sí', 'Medio', 'Comida casera',
            'Pasta, Pollo', 'Frutas', 'Ninguna', 'Ninguna', 'Alta',
            'Flexible', 'Le gusta probar', 'Cereal con leche',
            'Galletas', 'Sí', 'Pollo frito', 'Helado'
        ))
        
        conn.commit()
        conn.close()
        
        print("✅ Datos de prueba añadidos correctamente")
        print("📊 Adultos: 1 registro")
        print("📊 Niños: 1 registro")
        print("🚀 El servidor debería poder consultar las tablas ahora")
        
        return True
        
    except Exception as e:
        print(f"❌ Error añadiendo datos de prueba: {str(e)}")
        return False

if __name__ == "__main__":
    if add_test_data_correct():
        print("✅ Sistema listo para pruebas")
        print("📋 Prueba los endpoints:")
        print("  - curl http://localhost:7000/api/adults")
        print("  - curl http://localhost:7000/api/children")
        print("  - curl http://localhost:7000/api/house/config")
    else:
        print("❌ Error añadiendo datos de prueba")
