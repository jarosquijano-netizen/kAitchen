#!/usr/bin/env python3
"""
Script para probar el generador de menú con datos de prueba
"""

import os
import sys
import requests
import json

# Agregar el directorio del proyecto al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_menu_generation():
    """Probar el generador de menú con datos mínimos"""
    print("=== Probando Generador de Menú ===\n")
    
    # URL de producción
    url = "https://web-production-57291.up.railway.app/api/menu/generate"
    
    # Datos mínimos para probar
    test_data = {
        "week_start_date": "2026-01-19",
        "preferences": {}
    }
    
    try:
        print(f"🌐 Enviando POST request a: {url}")
        print(f"📋 Datos enviados:")
        print(json.dumps(test_data, indent=2))
        
        response = requests.post(url, json=test_data, timeout=30)
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📋 Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Response JSON:")
            print(json.dumps(data, indent=2))
        else:
            print(f"❌ Error Response: {response.text}")
            
    except requests.exceptions.Timeout:
        print("❌ Timeout: La petición tardó demasiado tiempo")
    except requests.exceptions.RequestException as e:
        print(f"❌ Request Error: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
    
    print("\n=== Prueba completada ===")

if __name__ == "__main__":
    test_menu_generation()
