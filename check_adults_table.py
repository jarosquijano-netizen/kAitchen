import sqlite3
import json

def check_adults_table():
    print("=== ANÁLISIS DETALLADO DE TABLA ADULTS ===\n")
    
    # Conectar a la base de datos
    db_path = "family_kitchen.db"
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        # 1. Verificar estructura de la tabla
        print("1. ESTRUCTURA DE LA TABLA:")
        cursor.execute("PRAGMA table_info(adults)")
        columns = cursor.fetchall()
        
        print("   Columnas encontradas:")
        for col in columns:
            print(f"   • {col[1]} ({col[2]}) - {'NOT NULL' if col[3] == 1 else 'NULL'}")
        
        # 2. Verificar todos los registros
        print("\n2. REGISTROS EN LA TABLA:")
        cursor.execute("SELECT * FROM adults")
        adults = cursor.fetchall()
        
        print(f"   Total de adultos: {len(adults)}")
        
        for i, adult in enumerate(adults, 1):
            print(f"\n   --- Adulto {i} ---")
            print(f"   ID: {adult['id']}")
            print(f"   Nombre: {adult['nombre']}")
            print(f"   Edad: {adult['edad']}")
            print(f"   Estilo alimentación: {adult['estilo_alimentacion'] if adult['estilo_alimentacion'] else 'No especificado'}")
            print(f"   Objetivo alimentario: {adult['objetivo_alimentario'] if adult['objetivo_alimentario'] else 'No especificado'}")
            print(f"   Alergias: {adult['alergias'] if adult['alergias'] else 'No especificadas'}")
            print(f"   Intolerancias: {adult['intolerancias'] if adult['intolerancias'] else 'No especificadas'}")
            print(f"   Ingredientes favoritos: {adult['ingredientes_favoritos'] if adult['ingredientes_favoritos'] else 'No especificados'}")
            print(f"   Ingredientes rechaza: {adult['ingredientes_no_gustan'] if adult['ingredientes_no_gustan'] else 'No especificados'}")
            print(f"   Creado: {adult['created_at'] if adult['created_at'] else 'No especificado'}")
            print(f"   Actualizado: {adult['updated_at'] if adult['updated_at'] else 'No especificado'}")
            
            # Mostrar todos los campos disponibles
            print(f"   Campos disponibles: {list(adult.keys())}")
        
        # 3. Verificar si hay datos JSON complejos
        print("\n3. ANÁLISIS DE CAMPOS JSON:")
        for adult in adults:
            for field in ['ingredientes_favoritos', 'ingredientes_no_gustan']:
                value = adult.get(field)
                if value and value != 'No especificados':
                    try:
                        parsed = json.loads(value) if isinstance(value, str) else value
                        print(f"   {field} (ID {adult['id']}): {type(parsed)} - {len(parsed) if isinstance(parsed, list) else 'N/A'} items")
                    except:
                        print(f"   {field} (ID {adult['id']}): Error al parsear JSON")
        
        # 4. Estadísticas
        print("\n4. ESTADÍSTICAS:")
        with_edad = sum(1 for adult in adults if adult.get('edad'))
        avg_edad = sum(adult.get('edad', 0) for adult in adults) / len(adults) if adults else 0
        
        print(f"   Con edad especificada: {with_edad}/{len(adults)}")
        if adults:
            print(f"   Edad promedio: {avg_edad:.1f} años")
        
        # 5. Campos nulos
        print("\n5. CAMPOS NULOS/VACÍOS:")
        null_counts = {}
        for col in columns:
            col_name = col[1]
            cursor.execute(f"SELECT COUNT(*) FROM adults WHERE {col_name} IS NULL OR {col_name} = ''")
            null_count = cursor.fetchone()[0]
            if null_count > 0:
                null_counts[col_name] = null_count
        
        if null_counts:
            print("   Campos con valores nulos:")
            for col_name, count in null_counts.items():
                print(f"   • {col_name}: {count} registros")
        else:
            print("   ✅ No hay campos nulos")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        conn.close()

if __name__ == "__main__":
    check_adults_table()
