#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Probar la generación de menús
"""
import requests
import json

# URL base
base_url = "http://localhost:7000"

def test_endpoints():
    print("🧪 TEST DE ENDPOINTS DE MENÚ")
    print("=" * 40)
    
    # 1. Verificar perfiles
    print("\n1. 👪 Verificando perfiles...")
    try:
        response = requests.get(f"{base_url}/api/adults")
        if response.status_code == 200:
            adults = response.json()
            print(f"   ✅ Adultos: {adults['count']} encontrados")
        else:
            print(f"   ❌ Error adultos: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error conexión adultos: {e}")
    
    try:
        response = requests.get(f"{base_url}/api/children")
        if response.status_code == 200:
            children = response.json()
            print(f"   ✅ Niños: {children['count']} encontrados")
        else:
            print(f"   ❌ Error niños: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error conexión niños: {e}")
    
    # 2. Probar generación de menú
    print("\n2. 🍽️  Probando generación de menú...")
    try:
        payload = {
            "week_start_date": "2026-01-12",
            "preferences": {}
        }
        response = requests.post(
            f"{base_url}/api/menu/generate",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Menú generado: {result.get('success', False)}")
        else:
            print(f"   ❌ Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Error conexión: {e}")
    
    # 3. Verificar menú actual
    print("\n3. 📅 Verificando menú actual...")
    try:
        response = requests.get(f"{base_url}/api/menu/current-week")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Menú encontrado: {result.get('success', False)}")
        else:
            print(f"   ❌ Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Error conexión: {e}")

if __name__ == "__main__":
    test_endpoints()
