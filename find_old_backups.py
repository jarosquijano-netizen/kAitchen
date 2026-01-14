import os
import sqlite3
import glob
from datetime import datetime

def find_old_backups():
    print("=== BÚSQUEDA DE BACKUPS ANTIGUOS ===\n")
    
    # 1. Buscar todos los archivos .db
    print("1. BUSCANDO TODOS LOS ARCHIVOS .DB:")
    all_db_files = glob.glob('*.db')
    
    # Excluir archivos actuales
    exclude_files = ['family_kitchen.db', 'family_kitchen_backup.db']
    exclude_files.extend(glob.glob('family_kitchen_safety_*.db'))
    
    potential_backups = []
    for db_file in all_db_files:
        if db_file not in exclude_files:
            potential_backups.append(db_file)
    
    print(f"   Encontrados {len(potential_backups)} archivos potenciales:")
    for i, backup_file in enumerate(potential_backups, 1):
        size = os.path.getsize(backup_file)
        mod_time = os.path.getmtime(backup_file)
        mod_date = datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d %H:%M:%S')
        
        print(f"   {i}. {backup_file}")
        print(f"      Tamaño: {size:,} bytes ({size/1024:.1f} KB)")
        print(f"      Modificado: {mod_date}")
    
    # 2. Verificar cuáles tienen datos
    print("\n2. VERIFICANDO CONTENIDO DE BACKUPS:")
    
    valid_backups = []
    
    for backup_file in potential_backups:
        try:
            conn = sqlite3.connect(backup_file)
            cursor = conn.cursor()
            
            # Verificar tablas principales
            cursor.execute("SELECT COUNT(*) FROM adults")
            adults_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM children")
            children_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM recipes")
            recipes_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM weekly_menus")
            menus_count = cursor.fetchone()[0]
            
            total_records = adults_count + children_count + recipes_count + menus_count
            
            conn.close()
            
            if total_records > 0:
                valid_backups.append({
                    'file': backup_file,
                    'adults': adults_count,
                    'children': children_count,
                    'recipes': recipes_count,
                    'menus': menus_count,
                    'total': total_records
                })
                print(f"   ✅ {backup_file}: {total_records} registros totales")
                print(f"      Adultos: {adults_count}, Niños: {children_count}")
                print(f"      Recetas: {recipes_count}, Menús: {menus_count}")
            else:
                print(f"   ❌ {backup_file}: Vacío")
                
        except Exception as e:
            print(f"   ❌ {backup_file}: Error al verificar - {e}")
    
    # 3. Ordenar por cantidad de datos
    print("\n3. BACKUPS ORDENADOS POR CANTIDAD DE DATOS:")
    valid_backups.sort(key=lambda x: x['total'], reverse=True)
    
    for i, backup in enumerate(valid_backups, 1):
        print(f"   {i}. {backup['file']}")
        print(f"      Total registros: {backup['total']}")
        print(f"      Adultos: {backup['adults']}, Niños: {backup['children']}")
        print(f"      Recetas: {backup['recipes']}, Menús: {backup['menus']}")
    
    # 4. Recomendación
    print("\n4. RECOMENDACIÓN:")
    
    if valid_backups:
        best_backup = valid_backups[0]
        print(f"   ✅ MEJOR OPCIÓN: {best_backup['file']}")
        print(f"      Contiene {best_backup['total']} registros")
        print(f"      Adultos: {best_backup['adults']}, Niños: {best_backup['children']}")
        print(f"      Recetas: {best_backup['recipes']}, Menús: {best_backup['menus']}")
        print(f"\n   🔄 ¿DESEA RESTAURAR DESDE {best_backup['file']}?")
        
        # Opción para restaurar
        confirm = input("   ¿Restaurar desde este backup? (s/n): ").lower().strip()
        
        if confirm == 's':
            print(f"   🔄 Restaurando desde {best_backup['file']}...")
            
            # Hacer backup de seguridad de la base actual
            import shutil
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            safety_backup = f"family_kitchen_before_restore_{timestamp}.db"
            
            try:
                shutil.copy2("family_kitchen.db", safety_backup)
                print(f"   ✅ Copia de seguridad: {safety_backup}")
                
                # Restaurar desde el backup seleccionado
                shutil.copy2(best_backup['file'], "family_kitchen.db")
                print(f"   ✅ Restauración completada desde {best_backup['file']}")
                
                print("\n   🎉 RESTAURACIÓN COMPLETADA")
                print("   📊 El sistema ahora tiene los datos del backup")
                print("   🔄 Reinicie el servidor para aplicar cambios")
                
            except Exception as e:
                print(f"   ❌ Error durante restauración: {e}")
        else:
            print("   ❌ Restauración cancelada")
    else:
        print("   ❌ NO SE ENCONTRARON BACKUPS CON DATOS")
        print("   📋 RECOMENDACIONES:")
        print("      • Generar nuevos perfiles familiares")
        print("      • Crear menús de prueba")
        print("      • Agregar recetas manualmente")

if __name__ == "__main__":
    find_old_backups()
