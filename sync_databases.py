#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para sincronizar datos de SQLite local a PostgreSQL en Railway
"""
import os
import sys
import json

# Fix encoding for Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

from database import Database

def sync_databases():
    """Sincroniza datos de SQLite local a PostgreSQL en Railway"""
    
    # Base de datos local (SQLite)
    local_db = Database(db_url='sqlite:///family_kitchen.db')
    
    # Base de datos de Railway (PostgreSQL)
    railway_db_url = os.getenv('RAILWAY_DATABASE_URL')
    if not railway_db_url:
        print("❌ Error: RAILWAY_DATABASE_URL no está configurada")
        print("   Obtén la URL de Railway → Tu servicio PostgreSQL → Variables → DATABASE_URL")
        print("   Luego ejecuta: set RAILWAY_DATABASE_URL=postgresql://...")
        return False
    
    print(f"📦 Conectando a Railway PostgreSQL...")
    # Crear nueva instancia para evitar problemas de pool
    railway_db = Database(db_url=railway_db_url)
    
    # Limpiar pool si existe para evitar problemas
    if hasattr(railway_db, '_pool'):
        try:
            railway_db._pool.closeall()
        except:
            pass
        delattr(railway_db, '_pool')
    
    print("\n🔄 Iniciando sincronización...\n")
    
    # 1. Sincronizar Adults
    print("1️⃣  Sincronizando adultos...")
    local_adults = local_db.get_all_adults()
    print(f"   📊 Encontrados {len(local_adults)} adultos en local")
    
    for adult in local_adults:
        try:
            # Limpiar valores vacíos que causan errores de tipo
            cleaned_adult = {}
            for key, value in adult.items():
                if value == '' or value == 'None':
                    cleaned_adult[key] = None
                elif key == 'edad' or key == 'tiempo_max_cocinar':
                    try:
                        cleaned_adult[key] = int(value) if value else None
                    except:
                        cleaned_adult[key] = None
                elif key == 'le_gustan_snacks':
                    cleaned_adult[key] = bool(value) if value else None
                else:
                    cleaned_adult[key] = value
            
            # Verificar si ya existe
            existing = railway_db.get_all_adults()
            exists = any(a.get('nombre') == cleaned_adult.get('nombre') and 
                        a.get('email') == cleaned_adult.get('email') for a in existing)
            
            if not exists:
                adult_id = railway_db.add_adult(cleaned_adult)
                print(f"   ✅ Añadido: {cleaned_adult.get('nombre')} (ID: {adult_id})")
            else:
                print(f"   ⏭️  Ya existe: {cleaned_adult.get('nombre')}")
        except Exception as e:
            print(f"   ❌ Error añadiendo {adult.get('nombre')}: {e}")
            import traceback
            traceback.print_exc()
    
    # 2. Sincronizar Children
    print("\n2️⃣  Sincronizando niños...")
    local_children = local_db.get_all_children()
    print(f"   📊 Encontrados {len(local_children)} niños en local")
    
    for child in local_children:
        try:
            # Limpiar valores vacíos
            cleaned_child = {}
            for key, value in child.items():
                if value == '' or value == 'None':
                    cleaned_child[key] = None
                elif key == 'edad':
                    try:
                        cleaned_child[key] = int(value) if value else None
                    except:
                        cleaned_child[key] = None
                else:
                    cleaned_child[key] = value
            
            # Verificar si ya existe
            existing = railway_db.get_all_children()
            exists = any(c.get('nombre') == cleaned_child.get('nombre') for c in existing)
            
            if not exists:
                child_id = railway_db.add_child(cleaned_child)
                print(f"   ✅ Añadido: {cleaned_child.get('nombre')} (ID: {child_id})")
            else:
                print(f"   ⏭️  Ya existe: {cleaned_child.get('nombre')}")
        except Exception as e:
            print(f"   ❌ Error añadiendo {child.get('nombre')}: {e}")
            import traceback
            traceback.print_exc()
    
    # 3. Sincronizar Recipes
    print("\n3️⃣  Sincronizando recetas...")
    local_recipes = local_db.get_all_recipes()
    print(f"   📊 Encontradas {len(local_recipes)} recetas en local")
    
    # Obtener recetas existentes una sola vez
    existing_recipes = railway_db.get_all_recipes()
    
    for recipe in local_recipes:
        try:
            # Verificar si ya existe por título
            exists = any(r.get('title', '').lower() == recipe.get('title', '').lower() 
                        for r in existing_recipes)
            
            if not exists:
                recipe_id = railway_db.add_recipe(recipe)
                print(f"   ✅ Añadida: {recipe.get('title')} (ID: {recipe_id})")
            else:
                print(f"   ⏭️  Ya existe: {recipe.get('title')}")
        except Exception as e:
            print(f"   ❌ Error añadiendo {recipe.get('title')}: {e}")
            import traceback
            traceback.print_exc()
    
    # 4. Sincronizar Weekly Menus
    print("\n4️⃣  Sincronizando menús semanales...")
    local_menus = local_db.get_all_menus()
    print(f"   📊 Encontrados {len(local_menus)} menús en local")
    
    # Procesar en lotes pequeños para evitar agotar el pool
    batch_size = 3
    for i in range(0, len(local_menus), batch_size):
        batch = local_menus[i:i+batch_size]
        print(f"   📦 Procesando lote {i//batch_size + 1} de {(len(local_menus)-1)//batch_size + 1}...")
        
        for menu in batch:
            try:
                menu_data = menu.get('menu_data')
                if isinstance(menu_data, str):
                    menu_data = json.loads(menu_data)
                
                week_start = menu.get('week_start_date') or menu.get('week_start')
                
                if not week_start:
                    print(f"   ⚠️  Menú sin week_start, saltando...")
                    continue
                
                # Obtener metadata si existe
                metadata = menu.get('metadata', {})
                if isinstance(metadata, str):
                    try:
                        metadata = json.loads(metadata)
                    except:
                        metadata = {}
                
                # Crear nueva instancia para cada menú para evitar problemas de pool
                temp_db = Database(db_url=railway_db_url)
                menu_id = temp_db.save_weekly_menu(week_start, menu_data, metadata)
                
                # Cerrar conexiones
                if hasattr(temp_db, '_pool'):
                    try:
                        temp_db._pool.closeall()
                    except:
                        pass
                
                print(f"   ✅ Sincronizado menú para semana {week_start} (ID: {menu_id})")
            except Exception as e:
                print(f"   ❌ Error sincronizando menú {menu.get('week_start_date', 'unknown')}: {e}")
                import traceback
                traceback.print_exc()
    
    # 5. Sincronizar Menu Preferences
    print("\n5️⃣  Sincronizando preferencias de menú...")
    try:
        local_prefs = local_db.get_menu_preferences()
        if local_prefs:
            railway_db.save_menu_preferences(local_prefs)
            print(f"   ✅ Preferencias sincronizadas")
        else:
            print(f"   ⏭️  No hay preferencias para sincronizar")
    except Exception as e:
        print(f"   ❌ Error sincronizando preferencias: {e}")
    
    print("\n✅ Sincronización completada!")
    print("\n📊 Resumen:")
    print(f"   - Adultos: {len(local_adults)}")
    print(f"   - Niños: {len(local_children)}")
    print(f"   - Recetas: {len(local_recipes)}")
    print(f"   - Menús: {len(local_menus)}")
    
    return True

if __name__ == '__main__':
    print("🚀 Sincronizador de Base de Datos: Local → Railway\n")
    
    # Verificar que existe la base de datos local
    if not os.path.exists('family_kitchen.db'):
        print("❌ Error: No se encuentra family_kitchen.db")
        print("   Asegúrate de ejecutar este script desde el directorio del proyecto")
        sys.exit(1)
    
    success = sync_databases()
    
    if success:
        print("\n🎉 ¡Datos sincronizados exitosamente!")
        print("   Ahora puedes ver tus datos en Railway")
    else:
        print("\n❌ Error durante la sincronización")
        sys.exit(1)
