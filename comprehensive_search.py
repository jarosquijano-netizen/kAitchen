import sqlite3

def comprehensive_search():
    print("=== BÚSQUEDA COMPLETA DE PERSONAS ===\n")
    
    # Conectar a la base de datos
    db_path = "family_kitchen.db"
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        # Personas a buscar (con variaciones)
        search_variations = {
            "Joe": ["joe", "Joe", "JOE", "joe "],
            "Xilef": ["xilef", "Xilef", "XILEF", "xilef "],
            "Abril": ["abril", "Abril", "ABRIL", "abril "],
            "Olivia": ["olivia", "Olivia", "OLIVIA", "olivia "]
        }
        
        print("1. BÚSQUEDA EN TABLA ADULTS:")
        cursor.execute("SELECT * FROM adults")
        adults = cursor.fetchall()
        
        found_adults = []
        for adult in adults:
            adult_name = adult['nombre'].strip().lower()
            
            # Buscar coincidencias parciales y exactas
            for target_name, variations in search_variations.items():
                if any(variation.lower() in adult_name or adult_name in variation.lower() for variation in variations):
                    found_adults.append({
                        'id': adult['id'],
                        'nombre': adult['nombre'],
                        'edad': adult['edad'],
                        'coincidencia': target_name,
                        'tipo': 'exacta' if adult_name == target_name else 'parcial'
                    })
                    break
        
        if found_adults:
            print(f"   Encontrados {len(found_adults)} adultos:")
            for found in found_adults:
                print(f"\n   --- ADULTO ENCONTRADO ---")
                print(f"   ID: {found['id']}")
                print(f"   Nombre: '{found['nombre']}'")
                print(f"   Edad: {found['edad']}")
                print(f"   Coincidencia con: {found['coincidencia']} ({found['tipo']})")
        else:
            print("   ❌ No se encontraron adultos")
        
        print("\n2. BÚSQUEDA EN TABLA CHILDREN:")
        cursor.execute("SELECT * FROM children")
        children = cursor.fetchall()
        
        found_children = []
        for child in children:
            child_name = child['nombre'].strip().lower()
            
            for target_name, variations in search_variations.items():
                if any(variation.lower() in child_name or child_name in variation.lower() for variation in variations):
                    found_children.append({
                        'id': child['id'],
                        'nombre': child['nombre'],
                        'edad': child['edad'],
                        'coincidencia': target_name,
                        'tipo': 'exacta' if child_name == target_name else 'parcial'
                    })
                    break
        
        if found_children:
            print(f"   Encontrados {len(found_children)} niños:")
            for found in found_children:
                print(f"\n   --- NIÑO/A ENCONTRADO ---")
                print(f"   ID: {found['id']}")
                print(f"   Nombre: '{found['nombre']}'")
                print(f"   Edad: {found['edad']}")
                print(f"   Coincidencia con: {found['coincidencia']} ({found['tipo']})")
        else:
            print("   ❌ No se encontraron niños")
        
        print("\n3. BÚSQUEDA EN TODOS LOS CAMPOS DE TEXTO:")
        print("   Buscando menciones en todos los campos de texto...")
        
        # Buscar en todos los campos de texto de ambas tablas
        all_text_fields = []
        
        # Campos de adultos
        cursor.execute("PRAGMA table_info(adults)")
        adult_columns = [row[1] for row in cursor.fetchall()]
        text_adult_columns = [col for col in adult_columns if 'TEXT' in col or 'VARCHAR' in col]
        
        # Campos de children
        cursor.execute("PRAGMA table_info(children)")
        children_columns = [row[1] for row in cursor.fetchall()]
        text_children_columns = [col for col in children_columns if 'TEXT' in col or 'VARCHAR' in col]
        
        print(f"   Campos de texto en adults: {text_adult_columns}")
        print(f"   Campos de texto en children: {text_children_columns}")
        
        # Buscar en cada campo de texto
        for table, columns, table_name in [(adults, text_adult_columns, "adults"), (children, text_children_columns, "children")]:
            for column in columns:
                cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE {column} LIKE '%Joe%' OR {column} LIKE '%joe%' OR {column} LIKE '%Xilef%' OR {column} LIKE '%xilef%' OR {column} LIKE '%Abril%' OR {column} LIKE '%abril%' OR {column} LIKE '%Olivia%' OR {column} LIKE '%olivia%'")
                count = cursor.fetchone()[0]
                if count > 0:
                    all_text_fields.append(f"{table_name}.{column}: {count} menciones")
        
        if all_text_fields:
            print("   Menciones encontradas en campos de texto:")
            for field in all_text_fields:
                print(f"   • {field}")
        else:
            print("   ❌ No se encontraron menciones en campos de texto")
        
        print("\n4. ANÁLISIS DE ESTADO ACTUAL:")
        current_adult_name = None
        current_children_names = []
        
        if adults:
            # Buscar el adulto actual (el último modificado o el primero)
            current_adult = max(adults, key=lambda x: x.get('updated_at', ''))
            current_adult_name = current_adult['nombre']
        
        if children:
            current_children_names = [child['nombre'] for child in children]
        
        print(f"   Adulto actual en BD: {current_adult_name}")
        print(f"   Niños en BD: {current_children_names}")
        
        print("\n5. CONCLUSIONES:")
        total_found = len(found_adults) + len(found_children)
        
        if total_found == 0:
            print("   ❌ RESULTADO: Ninguna de las personas buscadas (Joe, Xilef, Abril, Olivia) existe en la base de datos actual")
            print("   ✅ Esto significa que:")
            print("      • Los datos fueron eliminados completamente")
            print("      • La base de datos fue reinicializada")
            print("      • Los nombres nunca existieron")
            print("      • Los nombres tienen formato diferente en la búsqueda")
            print("   📋 RECOMENDACIONES:")
            print("      • Verificar si hay backups de la base de datos (.backup, .bak)")
            print("      • Revisar archivos de exportación si existen")
            print("      • Comprobar si el sistema se reinició recientemente")
        else:
            print("   ⚠️  RESULTADO: Se encontraron algunas coincidencias")
            print("   📋 ANÁLISIS DE COINCIDENCIAS:")
            for found in found_adults + found_children:
                if found['tipo'] == 'exacta':
                    print(f"      • {found['coincidencia']}: Coincidencia EXACTA - '{found['nombre']}'")
                else:
                    print(f"      • {found['coincidencia']}: Coincidencia PARCIAL - '{found['nombre']}' contiene '{found['coincidencia']}'")
    
    except Exception as e:
        print(f"❌ Error en la búsqueda: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        conn.close()

if __name__ == "__main__":
    comprehensive_search()
