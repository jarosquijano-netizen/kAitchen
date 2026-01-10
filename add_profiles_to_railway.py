#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Añadir perfiles desde localhost a Railway usando la API
"""
import sys
import requests
import json

# Fix encoding for Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

from database import Database

# Base de datos local
local_db = Database(db_url='sqlite:///family_kitchen.db')

# URL de Railway
railway_url = "https://web-production-57291.up.railway.app"

print("🚀 Añadiendo perfiles a Railway...\n")

# 1. Añadir Adultos
print("1️⃣  Añadiendo adultos...")
local_adults = local_db.get_all_adults()
print(f"   📊 Encontrados {len(local_adults)} adultos en local\n")

for adult in local_adults:
    try:
        # Limpiar datos para la API
        adult_data = {k: v for k, v in adult.items() if k != 'id' and k != 'created_at'}
        # Convertir valores vacíos a None
        for key, value in adult_data.items():
            if value == '' or value == 'None':
                adult_data[key] = None
            elif key in ['edad', 'tiempo_max_cocinar']:
                try:
                    adult_data[key] = int(value) if value else None
                except:
                    adult_data[key] = None
            elif key == 'le_gustan_snacks':
                adult_data[key] = bool(value) if value else None
        
        response = requests.post(
            f"{railway_url}/api/adults",
            json=adult_data,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print(f"   ✅ Añadido: {adult.get('nombre')}")
            else:
                print(f"   ⚠️  {adult.get('nombre')}: {result.get('error', 'Error desconocido')}")
        else:
            print(f"   ❌ Error añadiendo {adult.get('nombre')}: {response.status_code}")
            print(f"      {response.text}")
    except Exception as e:
        print(f"   ❌ Error añadiendo {adult.get('nombre')}: {e}")

# 2. Añadir Niños
print("\n2️⃣  Añadiendo niños...")
local_children = local_db.get_all_children()
print(f"   📊 Encontrados {len(local_children)} niños en local\n")

for child in local_children:
    try:
        # Limpiar datos para la API
        child_data = {k: v for k, v in child.items() if k != 'id' and k != 'created_at'}
        # Convertir valores vacíos a None
        for key, value in child_data.items():
            if value == '' or value == 'None':
                child_data[key] = None
            elif key == 'edad':
                try:
                    child_data[key] = int(value) if value else None
                except:
                    child_data[key] = None
        
        response = requests.post(
            f"{railway_url}/api/children",
            json=child_data,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print(f"   ✅ Añadido: {child.get('nombre')}")
            else:
                print(f"   ⚠️  {child.get('nombre')}: {result.get('error', 'Error desconocido')}")
        else:
            print(f"   ❌ Error añadiendo {child.get('nombre')}: {response.status_code}")
            print(f"      {response.text}")
    except Exception as e:
        print(f"   ❌ Error añadiendo {child.get('nombre')}: {e}")

print("\n✅ Proceso completado!")
print(f"\n🌐 Verifica en: {railway_url}")
print(f"📺 Vista TV: {railway_url}/tv")
