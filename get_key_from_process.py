#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para obtener la API key del proceso Flask en ejecucion
"""
import sys
import os

# Intentar importar psutil
try:
    import psutil
except ImportError:
    print("Instalando psutil...")
    os.system(f"{sys.executable} -m pip install psutil")
    import psutil

def get_flask_process():
    """Encuentra el proceso Flask que esta corriendo"""
    for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'environ']):
        try:
            cmdline = proc.info.get('cmdline', [])
            if cmdline and any('app.py' in str(arg) for arg in cmdline):
                return proc
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return None

def get_api_key_from_process(proc):
    """Intenta obtener la API key del proceso"""
    try:
        # Obtener variables de entorno del proceso
        env = proc.environ()
        api_key = env.get('ANTHROPIC_API_KEY', '')
        if api_key:
            return api_key
    except (psutil.NoSuchProcess, psutil.AccessDenied, AttributeError):
        pass
    
    # Intentar leer de memoria (mas complejo, requiere permisos)
    try:
        # Esto es mas complejo y puede no funcionar en Windows
        # Por ahora, solo intentamos las variables de entorno
        pass
    except:
        pass
    
    return None

if __name__ == '__main__':
    print("Buscando proceso Flask...")
    proc = get_flask_process()
    
    if not proc:
        print("No se encontro proceso Flask corriendo")
        sys.exit(1)
    
    print(f"Proceso Flask encontrado: PID {proc.pid}")
    print("Intentando obtener API key...")
    
    api_key = get_api_key_from_process(proc)
    
    if api_key:
        print(f"\nAPI Key encontrada: {api_key[:20]}...")
        print(f"Longitud: {len(api_key)} caracteres")
        
        # Guardar en .env
        env_path = '.env'
        env_content = ''
        
        if os.path.exists(env_path):
            with open(env_path, 'r', encoding='utf-8') as f:
                env_content = f.read()
        else:
            env_content = """# k[AI]tchen - Environment Variables
ANTHROPIC_API_KEY=
SECRET_KEY=dda99c73a04fca83e4a492b2310fea5c90a957423faf37118270dd3b8b922e62
DATABASE_URL=
FLASK_ENV=development
PORT=7000
CORS_ORIGINS=*
"""
        
        # Actualizar
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
            updated_lines.insert(0, f'ANTHROPIC_API_KEY={api_key}')
        
        with open(env_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(updated_lines))
        
        print("\nOK: API Key guardada en .env")
    else:
        print("\nERROR: No se pudo obtener la API key del proceso")
        print("   El proceso puede no tener permisos para leer variables de entorno")
        print("   O la key no esta en las variables de entorno del proceso")
