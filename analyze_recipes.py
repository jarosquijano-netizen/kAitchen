import sqlite3
import json
from datetime import datetime

def analyze_recipes():
    print("=== ANÁLISIS COMPLETO DE RECETAS ===\n")
    
    # Conectar a la base de datos
    db_path = "family_kitchen.db"
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        # 1. Verificar estructura de la tabla recipes
        print("1. ESTRUCTURA DE LA TABLA RECIPES:")
        cursor.execute("PRAGMA table_info(recipes)")
        columns = cursor.fetchall()
        
        print("   Columnas encontradas:")
        for col in columns:
            print(f"   • {col[1]} ({col[2]}) - {'NOT NULL' if col[3] == 1 else 'NULL'}")
        
        # 2. Contar recetas totales
        print("\n2. ESTADÍSTICAS GENERALES:")
        cursor.execute("SELECT COUNT(*) FROM recipes")
        total_recipes = cursor.fetchone()[0]
        print(f"   Total de recetas: {total_recipes}")
        
        # 3. Analizar recetas por creador
        print("\n3. ANÁLISIS POR CREADOR:")
        cursor.execute("""
            SELECT 
                created_at,
                COUNT(*) as count,
                GROUP_CONCAT(title, ', ') as recipes
            FROM recipes 
            GROUP BY created_at
            ORDER BY created_at
        """)
        
        creator_stats = cursor.fetchall()
        
        if creator_stats:
            print(f"   Recetas agrupadas por fecha de creación: {len(creator_stats)}")
            
            total_analyzed = 0
            for stat in creator_stats:
                created_at = stat['created_at']
                count = stat['count']
                recipes_list = stat['recipes'].split(', ')[:5]  # Primeras 5 recetas
                
                total_analyzed += count
                print(f"\n   --- Creado: {created_at} ---")
                print(f"   Cantidad: {count} recetas")
                print(f"   Recetas: {recipes_list}")
                print(f"   Porcentaje: {(count/total_recipes*100):.1f}% del total")
        
            print(f"\n   Total recetas analizadas: {total_analyzed}")
        
        # 4. Verificar si hay campo de creador
        print("\n4. BÚSQUEDA DE CAMPO CREADOR:")
        cursor.execute("PRAGMA table_info(recipes)")
        columns = [row[1] for row in cursor.fetchall()]
        
        creator_field = None
        for col in columns:
            if 'creat' in col[1].lower() or 'author' in col[1].lower() or 'user' in col[1].lower():
                creator_field = col[1]
                break
        
        if creator_field:
            print(f"   Campo de creador encontrado: {creator_field}")
            
            cursor.execute(f"SELECT {creator_field}, COUNT(*) FROM recipes GROUP BY {creator_field}")
            creator_data = cursor.fetchall()
            
            print("   Recetas por creador:")
            for row in creator_data:
                creator = row[0] if row[0] else 'Sin nombre'
                count = row[1]
                print(f"   • {creator}: {count} recetas")
        else:
            print("   ❌ No se encontró campo de creador específico")
        
        # 5. Análisis detallado de recetas recientes
        print("\n5. RECETAS RECIENTES (ÚLTIMAS 10):")
        cursor.execute("""
            SELECT 
                id,
                title,
                created_at,
                ingredients,
                prep_time,
                cook_time,
                difficulty
            FROM recipes 
            ORDER BY created_at DESC 
            LIMIT 10
        """)
        
        recent_recipes = cursor.fetchall()
        
        for i, recipe in enumerate(recent_recipes, 1):
            print(f"\n   --- Receta {i} ---")
            print(f"   ID: {recipe['id']}")
            print(f"   Nombre: {recipe['title']}")
            print(f"   Creado: {recipe['created_at']}")
            
            # Analizar ingredientes
            ingredients = recipe['ingredients'] if recipe['ingredients'] else 'No especificados'
            if ingredients and ingredients != 'No especificados':
                try:
                    if isinstance(ingredients, str):
                        ing_list = json.loads(ingredients)
                        print(f"   Ingredientes: {len(ing_list)} ingredientes")
                    else:
                        print(f"   Ingredientes: {ingredients}")
                except:
                    print(f"   Ingredientes: Error al parsear")
            else:
                print(f"   Ingredientes: No especificados")
            
            print(f"   Tiempo preparación: {recipe['prep_time'] if recipe['prep_time'] else 'No especificado'} minutos")
            print(f"   Tiempo cocción: {recipe['cook_time'] if recipe['cook_time'] else 'No especificado'} minutos")
            print(f"   Dificultad: {recipe['difficulty'] if recipe['difficulty'] else 'No especificado'}")
        
        # 6. Búsqueda de recetas específicas si hay alguna referencia
        print("\n6. BÚSQUEDA DE RECETAS ESPECÍFICAS:")
        
        # Buscar recetas que puedan ser las que mencionaste
        search_terms = ['joe', 'xilef', 'abril', 'olivia', 'test', 'update', 'edit']
        
        found_recipes = []
        for term in search_terms:
            cursor.execute("SELECT id, title FROM recipes WHERE LOWER(title) LIKE LOWER(?)", (f'%{term}%',))
            matches = cursor.fetchall()
            for match in matches:
                found_recipes.append({
                    'termino': term,
                    'id': match[0],
                    'title': match[1]
                })
        
        if found_recipes:
            print("   Recetas encontradas con términos de búsqueda:")
            for found in found_recipes:
                print(f"   • '{found['termino']}' -> ID {found['id']}: '{found['title']}'")
        else:
            print("   ❌ No se encontraron recetas con los términos de búsqueda")
        
        # 7. Análisis de calidad de datos
        print("\n7. CALIDAD DE DATOS:")
        cursor.execute("SELECT COUNT(*) FROM recipes WHERE title IS NULL OR title = ''")
        empty_names = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM recipes WHERE ingredients IS NULL OR ingredients = ''")
        empty_ingredients = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM recipes WHERE prep_time IS NULL OR prep_time = ''")
        empty_prep_time = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM recipes WHERE cook_time IS NULL OR cook_time = ''")
        empty_cook_time = cursor.fetchone()[0]
        
        print(f"   Recetas sin título: {empty_names}")
        print(f"   Recetas sin ingredientes: {empty_ingredients}")
        print(f"   Recetas sin tiempo prep: {empty_prep_time}")
        print(f"   Recetas sin tiempo cocción: {empty_cook_time}")
        
        # 8. Timestamps
        print("\n8. ANÁLISIS TEMPORAL:")
        cursor.execute("SELECT MIN(created_at), MAX(created_at) FROM recipes")
        time_range = cursor.fetchone()
        
        if time_range[0] and time_range[1]:
            print(f"   Primera receta: {time_range[0]}")
            print(f"   Última receta: {time_range[1]}")
            
            # Calcular diferencia
            try:
                first_date = datetime.strptime(time_range[0], '%Y-%m-%d %H:%M:%S')
                last_date = datetime.strptime(time_range[1], '%Y-%m-%d %H:%M:%S')
                diff = last_date - first_date
                print(f"   Período de creación: {diff.days} días")
            except:
                print(f"   Error al calcular período")
        
        print("\n9. CONCLUSIONES:")
        print("   📊 ESTADO ACTUAL DE RECETAS:")
        print(f"   • Total recetas en BD: {total_recipes}")
        print(f"   • Base de datos: SQLite local")
        print(f"   • Tabla recipes: Estructura completa")
        
        if total_recipes == 0:
            print("   ❌ RESULTADO: No hay recetas en la base de datos")
            print("   🔄 ESTADO: Sistema sin recetas")
        elif total_recipes < 10:
            print("   ⚠️ RESULTADO: Pocas recetas encontradas")
            print("   📝 RECOMENDACIÓN: Agregar más recetas al sistema")
        else:
            print("   ✅ RESULTADO: Recetas encontradas y analizadas")
            print("   📝 DATOS DISPONIBLES PARA USUARIO")
    
    except Exception as e:
        print(f"❌ Error en el análisis: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        conn.close()

if __name__ == "__main__":
    analyze_recipes()
