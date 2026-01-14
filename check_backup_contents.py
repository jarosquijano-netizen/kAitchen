import sqlite3
import json

def check_backup_contents():
    print("=== VERIFICACIÓN DE CONTENIDO DEL BACKUP ===\n")
    
    backup_db = "family_kitchen_backup.db"
    
    if not sqlite3.connect(backup_db):
        print(f"❌ ERROR: No se puede conectar al backup {backup_db}")
        return
    
    conn = sqlite3.connect(backup_db)
    cursor = conn.cursor()
    
    try:
        # 1. Verificar tablas en el backup
        print("1. TABLAS EN BACKUP:")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        print(f"   Tablas encontradas: {len(tables)}")
        for table in tables:
            if table != 'sqlite_sequence':
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"   • {table}: {count} registros")
        
        # 2. Verificar menús en el backup
        print("\n2. MENÚS EN BACKUP:")
        cursor.execute("SELECT COUNT(*) FROM weekly_menus")
        menu_count = cursor.fetchone()[0]
        
        if menu_count > 0:
            print(f"   ✅ Se encontraron {menu_count} menús en el backup")
            
            # Obtener el menú más reciente
            cursor.execute("SELECT week_start_date, created_at, menu_data FROM weekly_menus ORDER BY created_at DESC LIMIT 1")
            latest_menu = cursor.fetchone()
            
            if latest_menu:
                print(f"   ✅ Menú más reciente:")
                print(f"   • Semana: {latest_menu[0]}")
                print(f"   • Creado: {latest_menu[1]}")
                
                # Verificar contenido del menú
                if latest_menu[2]:  # menu_data
                    try:
                        menu_data = json.loads(latest_menu[2])
                        print(f"   • Estructura: {type(menu_data)}")
                        
                        if isinstance(menu_data, dict):
                            print("   • Campos encontrados:")
                            for key, value in menu_data.items():
                                print(f"     - {key}: {type(value)}")
                                
                                if key == 'menu_adultos' and isinstance(value, dict):
                                    print(f"       • Subcampos: {list(value.keys())}")
                                elif key == 'menu_ninos' and isinstance(value, dict):
                                    print(f"       • Subcampos: {list(value.keys())}")
                        else:
                            print(f"   • Formato: {type(menu_data)} (no es dict)")
                    except Exception as e:
                        print(f"   • Error al parsear menu_data: {e}")
        else:
            print("   ❌ No se encontraron menús en el backup")
        
        # 3. Verificar recetas en el backup
        print("\n3. RECETAS EN BACKUP:")
        cursor.execute("SELECT COUNT(*) FROM recipes")
        recipe_count = cursor.fetchone()[0]
        
        if recipe_count > 0:
            print(f"   ✅ Se encontraron {recipe_count} recetas en el backup")
            
            # Obtener algunas recetas de ejemplo
            cursor.execute("SELECT title, created_at FROM recipes ORDER BY created_at DESC LIMIT 3")
            recipes = cursor.fetchall()
            
            print("   ✅ Últimas recetas:")
            for recipe in recipes:
                print(f"   • {recipe[0]} (creado: {recipe[1]})")
        else:
            print("   ❌ No se encontraron recetas en el backup")
        
        # 4. Verificar perfiles en el backup
        print("\n4. PERFILES EN BACKUP:")
        
        cursor.execute("SELECT COUNT(*) FROM adults")
        adults_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM children")
        children_count = cursor.fetchone()[0]
        
        print(f"   ✅ Adultos: {adults_count}")
        print(f"   ✅ Niños: {children_count}")
        
        if adults_count > 0:
            cursor.execute("SELECT nombre, edad FROM adults LIMIT 3")
            adults = cursor.fetchall()
            print("   Últimos adultos:")
            for adult in adults:
                print(f"   • {adult[0]} ({adult[1]} años)")
        
        if children_count > 0:
            cursor.execute("SELECT nombre, edad FROM children LIMIT 3")
            children = cursor.fetchall()
            print("   Últimos niños:")
            for child in children:
                print(f"   • {child[0]} ({child[1]} años)")
        
        print("\n5. CONCLUSIONES:")
        if menu_count > 0 and recipe_count > 0:
            print("   ✅ BACKUP CONTIENE DATOS ÚTILES")
            print("   🔄 SE PUEDE RESTAURAR ESTE BACKUP")
            print("   📋 ESTADO: Listo para generar menú desde backup")
        else:
            print("   ❌ BACKUP VACÍO O INCOMPLETO")
            print("   📋 ESTADO: Se necesita generar nuevos datos")
    
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        conn.close()

if __name__ == "__main__":
    check_backup_contents()
