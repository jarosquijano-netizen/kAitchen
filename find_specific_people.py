import sqlite3

def find_specific_people():
    print("=== BÚSQUEDA DE PERSONAS ESPECÍFICAS ===\n")
    
    # Personas a buscar
    search_names = ["Joe", "Xilef", "Abril", "Olivia"]
    
    # Conectar a la base de datos
    db_path = "family_kitchen.db"
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        # Buscar en tabla adults
        print("1. BÚSQUEDA EN TABLA ADULTS:")
        cursor.execute("SELECT * FROM adults")
        adults = cursor.fetchall()
        
        found_adults = []
        for adult in adults:
            if any(name.lower() in adult['nombre'].lower() for name in search_names):
                found_adults.append(adult)
        
        if found_adults:
            print(f"   Encontrados {len(found_adults)} adultos:")
            for adult in found_adults:
                print(f"\n   --- ADULTO ---")
                print(f"   ID: {adult['id']}")
                print(f"   Nombre: {adult['nombre']}")
                print(f"   Edad: {adult['edad']}")
                print(f"   Estilo alimentación: {adult.get('estilo_alimentacion', 'No especificado')}")
                print(f"   Objetivo alimentario: {adult.get('objetivo_alimentario', 'No especificado')}")
                print(f"   Alergias: {adult.get('alergias', 'No especificadas')}")
                print(f"   Intolerancias: {adult.get('intolerancias', 'No especificadas')}")
                print(f"   Nivel cocina: {adult.get('nivel_cocina', 'No especificado')}")
                print(f"   Creado: {adult.get('created_at', 'No especificado')}")
                print(f"   Actualizado: {adult.get('updated_at', 'No especificado')}")
        else:
            print("   ❌ No se encontraron adultos con esos nombres")
        
        # Buscar en tabla children
        print("\n2. BÚSQUEDA EN TABLA CHILDREN:")
        cursor.execute("SELECT * FROM children")
        children = cursor.fetchall()
        
        found_children = []
        for child in children:
            if any(name.lower() in child['nombre'].lower() for name in search_names):
                found_children.append(child)
        
        if found_children:
            print(f"   Encontrados {len(found_children)} niños:")
            for child in found_children:
                print(f"\n   --- NIÑO/A ---")
                print(f"   ID: {child['id']}")
                print(f"   Nombre: {child['nombre']}")
                print(f"   Edad: {child['edad']}")
                print(f"   Nivel exigencia: {child.get('nivel_exigencia', 'No especificado')}")
                print(f"   Acepta comida nueva: {child.get('acepta_comida_nueva', 'No especificado')}")
                print(f"   Alergias: {child.get('alergias', 'No especificadas')}")
                print(f"   Intolerancias: {child.get('intolerancias', 'No especificadas')}")
                print(f"   Ingredientes favoritos: {child.get('ingredientes_favoritos', 'No especificados')}")
                print(f"   Ingredientes rechaza: {child.get('ingredientes_rechaza', 'No especificados')}")
                print(f"   Verduras aceptadas: {child.get('verduras_aceptadas', 'No especificadas')}")
                print(f"   Verduras rechazadas: {child.get('verduras_rechazadas', 'No especificadas')}")
                print(f"   Texturas no gustan: {child.get('texturas_no_gustan', 'No especificadas')}")
                print(f"   Comentarios padres: {child.get('comentarios_padres', 'No especificados')}")
                print(f"   Creado: {child.get('created_at', 'No especificado')}")
                print(f"   Actualizado: {child.get('updated_at', 'No especificado')}")
        else:
            print("   ❌ No se encontraron niños con esos nombres")
        
        # Buscar en otras tablas (menús, limpieza, etc.)
        print("\n3. BÚSQUEDA EN OTRAS TABLAS:")
        
        # Verificar estructura de weekly_menus primero
        cursor.execute("PRAGMA table_info(weekly_menus)")
        menu_columns = [row[1] for row in cursor.fetchall()]
        print(f"   Columnas en weekly_menus: {menu_columns}")
        
        # Buscar menciones en cleaning_assignments
        cursor.execute("SELECT COUNT(*) FROM cleaning_assignments WHERE notas LIKE '%Joe%' OR notas LIKE '%Xilef%' OR notas LIKE '%Abril%' OR notas LIKE '%Olivia%'")
        cleaning_mentions = cursor.fetchone()[0]
        print(f"   Menciones en limpieza: {cleaning_mentions}")
        
        # Buscar menciones en menu_day_ratings (si existe la tabla)
        try:
            cursor.execute("SELECT COUNT(*) FROM menu_day_ratings WHERE week_start LIKE '%Joe%' OR week_start LIKE '%Xilef%' OR week_start LIKE '%Abril%' OR week_start LIKE '%Olivia%'")
            rating_mentions = cursor.fetchone()[0]
            print(f"   Menciones en ratings: {rating_mentions}")
        except:
            print("   Menciones en ratings: Tabla no existe")
        
        # 4. Análisis final
        print("\n4. ANÁLISIS FINAL:")
        total_found = len(found_adults) + len(found_children)
        print(f"   Total personas encontradas: {total_found}")
        
        if total_found > 0:
            print("   ✅ Algunas de las personas buscadas están en la base de datos actual")
            print("   ❌ Posibles escenarios:")
            print("      • Los datos fueron modificados/actualizados")
            print("      • Los datos fueron eliminados")
            print("      • Los datos están en una tabla diferente")
            print("      • Los nombres tienen formato diferente (con espacios, caracteres especiales, etc.)")
        else:
            print("   ❌ Ninguna de las personas buscadas está en la base de datos actual")
            print("   ✅ Recomendaciones:")
            print("      • Verificar si los nombres están escritos correctamente")
            print("      • Revisar si los datos fueron eliminados recientemente")
            print("      • Comprobar si hay copias de seguridad de la base de datos")
    
    except Exception as e:
        print(f"❌ Error en la búsqueda: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        conn.close()

if __name__ == "__main__":
    find_specific_people()
