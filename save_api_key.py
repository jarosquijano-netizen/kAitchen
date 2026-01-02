#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para guardar la API key de Anthropic en el archivo .env
"""
import os
import sys

def save_api_key_to_env(api_key):
    """Guarda la API key en el archivo .env"""
    if not api_key or not api_key.strip():
        print("Error: La API key no puede estar vacia")
        return False
    
    api_key = api_key.strip()
    
    if not api_key.startswith('sk-ant-'):
        print("Error: La API key debe comenzar con 'sk-ant-'")
        return False
    
    # Leer el archivo .env actual
    env_path = '.env'
    env_content = ''
    
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            env_content = f.read()
    else:
        # Crear estructura basica
        env_content = """# k[AI]tchen - Environment Variables
ANTHROPIC_API_KEY=
SECRET_KEY=dda99c73a04fca83e4a492b2310fea5c90a957423faf37118270dd3b8b922e62
DATABASE_URL=
FLASK_ENV=development
PORT=7000
CORS_ORIGINS=*
"""
    
    # Actualizar o anadir ANTHROPIC_API_KEY
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
        # Anadir al principio si no se encontro
        updated_lines.insert(0, f'ANTHROPIC_API_KEY={api_key}')
    
    # Escribir de vuelta al .env
    with open(env_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(updated_lines))
    
    print(f"OK: API Key guardada en .env")
    print(f"   Preview: {api_key[:20]}...")
    print(f"   Longitud: {len(api_key)} caracteres")
    return True

if __name__ == '__main__':
    if len(sys.argv) > 1:
        # API key proporcionada como argumento
        api_key = sys.argv[1]
        save_api_key_to_env(api_key)
    else:
        # Pedir la API key interactivamente
        print("=" * 60)
        print("Guardar API Key de Anthropic en .env")
        print("=" * 60)
        print("\nPega tu API key completa (empieza con 'sk-ant-api03-...'):")
        api_key = input("> ").strip()
        
        if save_api_key_to_env(api_key):
            print("\nLa API key ha sido guardada correctamente en .env")
            print("Reinicia el servidor Flask para que la cargue.")
        else:
            print("\nError al guardar la API key")
            sys.exit(1)
