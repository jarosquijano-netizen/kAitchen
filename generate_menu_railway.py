#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generar menú para la semana actual en Railway usando la API
"""
import sys
import requests
import json

# Fix encoding for Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

from datetime import datetime, timedelta

# Calcular semana actual
today = datetime.now()
days_since_monday = today.weekday()  # 0 = Monday, 6 = Sunday
current_week_start = (today - timedelta(days=days_since_monday)).strftime('%Y-%m-%d')

print(f"📅 Semana actual: {current_week_start}")
print(f"🌐 Generando menú en Railway...\n")

url = "https://web-production-57291.up.railway.app/api/menu/generate"

data = {
    "week_start_date": current_week_start
}

try:
    print("⏳ Enviando solicitud...")
    response = requests.post(url, json=data, timeout=600)  # 10 minutos timeout
    
    print(f"Status Code: {response.status_code}\n")
    
    if response.status_code == 200:
        result = response.json()
        if result.get('success'):
            print("✅ Menú generado exitosamente!")
            print(f"   Menu ID: {result.get('menu_id')}")
            print(f"   Week Start: {result.get('week_start', current_week_start)}")
            print("\n🎉 Ahora puedes ver el menú en:")
            print("   https://web-production-57291.up.railway.app/tv")
        else:
            print("❌ Error al generar menú:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"❌ Error {response.status_code}:")
        print(response.text)
        
except Exception as e:
    print(f"❌ Error al conectar: {e}")
    import traceback
    traceback.print_exc()
