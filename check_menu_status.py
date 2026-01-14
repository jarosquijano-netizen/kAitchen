import sqlite3

def check_menu_status():
    print("=== VERIFICACIÓN DE ESTADO DE MENÚS ===\n")
    
    # Conectar a la base de datos
    conn = sqlite3.connect("family_kitchen.db")
    cursor = conn.cursor()
    
    try:
        # 1. Verificar tabla weekly_menus
        print("1. VERIFICANDO TABLA weekly_menus:")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='weekly_menus'")
        table_exists = cursor.fetchone()
        
        if table_exists:
            print("   ✅ Tabla weekly_menus encontrada")
            
            # 2. Contar menús totales
            cursor.execute("SELECT COUNT(*) FROM weekly_menus")
            total_menus = cursor.fetchone()[0]
            print(f"   Total de menús: {total_menus}")
            
            # 3. Verificar menús por semana
            cursor.execute("SELECT week_start_date, created_at, COUNT(*) as count FROM weekly_menus GROUP BY week_start_date ORDER BY week_start_date")
            menus_by_week = cursor.fetchall()
            
            print("   Menús por semana:")
            for menu in menus_by_week:
                print(f"   • Semana {menu[0]}: {menu[2]} menús (creado: {menu[1]})")
            
            # 4. Verificar menú de la semana actual
            current_week = "2026-01-12"
            print(f"\n2. BUSCANDO MENÚ PARA SEMANA ACTUAL: {current_week}")
            
            cursor.execute("SELECT id, week_start_date, created_at, metadata, rating FROM weekly_menus WHERE week_start_date = ?", (current_week,))
            current_menu = cursor.fetchone()
            
            if current_menu:
                print("   ✅ Menú encontrado:")
                print(f"   • ID: {current_menu[0]}")
                print(f"   • Semana: {current_menu[1]}")
                print(f"   • Creado: {current_menu[2]}")
                print(f"   • Rating: {current_menu[3]}")
                
                # Verificar si tiene datos
                if current_menu[4]:  # metadata
                    try:
                        import json
                        metadata = json.loads(current_menu[4])
                        print(f"   • Metadata: {len(metadata)} campos")
                    except:
                        print(f"   • Metadata: Error al parsear JSON")
            else:
                print("   ❌ Menú no encontrado para la semana actual")
            
            # 5. Verificar otras semanas disponibles
            print("\n3. OTRAS SEMANAS DISPONIBLES:")
            cursor.execute("SELECT week_start_date, created_at FROM weekly_menus WHERE week_start_date != ? ORDER BY week_start_date DESC LIMIT 5", (current_week,))
            other_weeks = cursor.fetchall()
            
            if other_weeks:
                print(f"   Encontradas {len(other_weeks)} otras semanas:")
                for week in other_weeks:
                    print(f"   • {week[0]} (creado: {week[1]})")
            else:
                print("   ❌ No hay otras semanas disponibles")
                
        else:
            print("   ❌ Tabla weekly_menus no encontrada")
        
        # 6. Verificar si hay datos de prueba
        print("\n4. VERIFICANDO DATOS DE PRUEBA:")
        
        # Buscar en todas las tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        all_tables = [row[0] for row in cursor.fetchall()]
        
        print(f"   Tablas encontradas: {len(all_tables)}")
        for table in all_tables:
            if table != 'sqlite_sequence':
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                if count > 0:
                    print(f"   • {table}: {count} registros")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        conn.close()

if __name__ == "__main__":
    check_menu_status()
