#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test del endpoint de Railway para ver qué está devolviendo
"""
import sys
import requests
import json

# Fix encoding for Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

url = "https://web-production-57291.up.railway.app/api/menu/current-week"

print(f"🔍 Probando endpoint: {url}\n")

try:
    response = requests.get(url, timeout=10)
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}\n")
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Respuesta exitosa:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
    elif response.status_code == 404:
        data = response.json()
        print("❌ 404 - No encontrado:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print(f"❌ Error {response.status_code}:")
        print(response.text)
except Exception as e:
    print(f"❌ Error al conectar: {e}")
