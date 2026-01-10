#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar qué menús hay en Railway y generar uno para la semana actual si falta
"""
import os
import sys
from datetime import datetime, timedelta

# Fix encoding for Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

from database import Database

# Calcular semana actual
today = datetime.now()
days_since_monday = today.weekday()  # 0 = Monday, 6 = Sunday
current_week_start = (today - timedelta(days=days_since_monday)).strftime('%Y-%m-%d')

print(f"📅 Hoy es: {today.strftime('%Y-%m-%d %A')}")
print(f"📅 Lunes de esta semana: {current_week_start}\n")

# Conectar a Railway
railway_db_url = os.getenv('RAILWAY_DATABASE_URL')
if not railway_db_url:
    print("❌ Error: RAILWAY_DATABASE_URL no está configurada")
    sys.exit(1)

print(f"📦 Conectando a Railway PostgreSQL...")
railway_db = Database(db_url=railway_db_url)

# Obtener todos los menús
all_menus = railway_db.get_all_menus()
print(f"\n📊 Menús encontrados en Railway: {len(all_menus)}")

if all_menus:
    print("\n📋 Lista de menús:")
    for menu in all_menus[:10]:  # Mostrar primeros 10
        week_start = menu.get('week_start_date', 'unknown')
        menu_id = menu.get('id', 'unknown')
        created = menu.get('created_at', 'unknown')
        print(f"   - Semana {week_start} (ID: {menu_id}, Creado: {created})")

# Verificar si hay menú para la semana actual
current_menu = railway_db.get_menu_by_week_start(current_week_start)

if current_menu:
    print(f"\n✅ ¡Hay menú para la semana actual ({current_week_start})!")
    print(f"   ID: {current_menu.get('id')}")
else:
    print(f"\n❌ No hay menú para la semana actual ({current_week_start})")
    print(f"\n💡 Solución:")
    print(f"   1. Ve a: https://web-production-57291.up.railway.app")
    print(f"   2. Ve a la pestaña 'Menu'")
    print(f"   3. Click en 'Generar Menú con IA'")
    print(f"   4. Esto creará un menú para la semana del {current_week_start}")
