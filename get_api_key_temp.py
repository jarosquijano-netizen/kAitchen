#!/usr/bin/env python3
"""
Script temporal para obtener la API key completa del servidor Flask
y guardarla en el archivo .env
"""
import os
import sys
from dotenv import load_dotenv

# Cargar variables de entorno actuales
load_dotenv()

# Intentar obtener la key del entorno
api_key = os.getenv('ANTHROPIC_API_KEY', '')

if not api_key:
    print("⚠️  No se encontró ANTHROPIC_API_KEY en las variables de entorno")
    print("💡 El servidor Flask puede tenerla cargada en memoria desde antes")
    print("\nOpciones:")
    print("1. Proporciona la API key completa manualmente")
    print("2. El servidor Flask la tiene en memoria pero no está en .env")
    print("\nPara guardarla en .env, necesitas:")
    print("- La key completa (empieza con 'sk-ant-api03-...')")
    print("- O reiniciar el servidor después de guardarla en .env")
    sys.exit(1)

# Leer el archivo .env actual
env_path = '.env'
env_content = ''

if os.path.exists(env_path):
    with open(env_path, 'r', encoding='utf-8') as f:
        env_content = f.read()
else:
    # Crear estructura básica
    env_content = """# k[AI]tchen - Environment Variables
ANTHROPIC_API_KEY=
SECRET_KEY=
DATABASE_URL=
FLASK_ENV=development
PORT=7000
CORS_ORIGINS=*
"""

# Actualizar o añadir ANTHROPIC_API_KEY
lines = env_content.split('\n')
updated_lines = []
api_key_found = False

for line in lines:
    if line.strip().startswith('ANTHROPIC_API_KEY='):
        updated_lines.append(f'ANTHROPIC_API_KEY={api_key}')
        api_key_found = True
    else:
        updated_lines.append(line)

if not api_key_found:
    # Añadir al principio si no se encontró
    updated_lines.insert(0, f'ANTHROPIC_API_KEY={api_key}')

# Escribir de vuelta al .env
with open(env_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(updated_lines))

print(f"✅ API Key guardada en .env")
print(f"   Preview: {api_key[:20]}...")
print(f"   Longitud: {len(api_key)} caracteres")
