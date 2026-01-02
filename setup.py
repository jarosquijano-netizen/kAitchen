#!/usr/bin/env python3
"""
k[AI]tchen - Setup Script
Configures the project for development or production deployment
"""

import os
import sys
import secrets
from pathlib import Path

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")

def print_success(text):
    """Print success message"""
    print(f"✅ {text}")

def print_info(text):
    """Print info message"""
    print(f"ℹ️  {text}")

def print_warning(text):
    """Print warning message"""
    print(f"⚠️  {text}")

def print_error(text):
    """Print error message"""
    print(f"❌ {text}")

def generate_secret_key():
    """Generate secure secret key"""
    return secrets.token_hex(32)

def setup_env_file():
    """Create .env file from template"""
    print_header("Configuración de Variables de Entorno")
    
    env_path = Path('.env')
    env_example_path = Path('.env.example')
    
    if env_path.exists():
        print_warning(".env ya existe")
        response = input("¿Sobrescribir? (s/n): ").lower()
        if response != 's':
            print_info("Manteniendo .env existente")
            return False
    
    # Read template
    if not env_example_path.exists():
        print_error(".env.example no encontrado")
        return False
    
    with open(env_example_path, 'r') as f:
        template = f.read()
    
    # Get Anthropic API key
    print("\n📝 Configuración de API Keys")
    print_info("Obtén tu Anthropic API key en: https://console.anthropic.com/")
    anthropic_key = input("\nANTHROPIC_API_KEY (o Enter para dejar en blanco): ").strip()
    
    # Generate secret key
    secret_key = generate_secret_key()
    print_success(f"SECRET_KEY generado: {secret_key[:20]}...")
    
    # Replace in template
    content = template.replace('your-secret-key-here-generate-with-python-secrets', secret_key)
    
    if anthropic_key:
        content = content.replace('sk-ant-api03-your-key-here', anthropic_key)
    
    # Write .env
    with open('.env', 'w') as f:
        f.write(content)
    
    print_success(".env creado correctamente")
    return True

def check_dependencies():
    """Check if required packages are installed"""
    print_header("Verificación de Dependencias")
    
    required = [
        'flask',
        'anthropic',
        'beautifulsoup4',
        'pandas',
        'psycopg2',
    ]
    
    missing = []
    for package in required:
        try:
            __import__(package.replace('-', '_'))
            print_success(f"{package} instalado")
        except ImportError:
            print_warning(f"{package} NO instalado")
            missing.append(package)
    
    if missing:
        print("\n" + "="*70)
        print_warning("Faltan dependencias. Instala con:")
        print(f"pip install -r requirements.txt")
        print("="*70)
        return False
    
    print_success("Todas las dependencias instaladas")
    return True

def init_database():
    """Initialize database"""
    print_header("Inicialización de Base de Datos")
    
    try:
        from database import Database
        
        print_info("Creando base de datos...")
        db = Database()
        
        print_success("Base de datos inicializada")
        
        # Ask to add sample profiles
        response = input("\n¿Añadir perfiles de ejemplo? (s/n): ").lower()
        if response == 's':
            from init import add_sample_profiles
            add_sample_profiles(db)
        
        return True
        
    except Exception as e:
        print_error(f"Error al inicializar base de datos: {e}")
        return False

def check_cursor_config():
    """Check if Cursor configuration exists"""
    print_header("Configuración de Cursor")
    
    cursor_rules = Path('.cursorrules')
    if cursor_rules.exists():
        print_success(".cursorrules encontrado")
        print_info("Cursor AI está configurado para este proyecto")
        return True
    else:
        print_warning(".cursorrules no encontrado")
        return False

def setup_git():
    """Initialize git if not already done"""
    print_header("Configuración de Git")
    
    git_dir = Path('.git')
    if git_dir.exists():
        print_success("Git ya inicializado")
        return True
    
    response = input("¿Inicializar repositorio Git? (s/n): ").lower()
    if response == 's':
        os.system('git init')
        os.system('git add .')
        os.system('git commit -m "Initial commit - k[AI]tchen"')
        print_success("Git inicializado")
        print_info("Recuerda crear repositorio en Github y hacer push:")
        print("  git remote add origin https://github.com/TU_USUARIO/tu-repo.git")
        print("  git push -u origin main")
        return True
    
    return False

def print_next_steps(config):
    """Print next steps based on setup"""
    print_header("🎉 ¡Configuración Completada!")
    
    print("📋 PRÓXIMOS PASOS:\n")
    
    print("1️⃣  DESARROLLO LOCAL:")
    print("   python app.py")
    print("   Abre: http://localhost:5000\n")
    
    if not config.get('anthropic_key'):
        print("2️⃣  CONFIGURAR API KEY:")
        print("   - Edita .env")
        print("   - Añade tu ANTHROPIC_API_KEY")
        print("   - Consigue key en: https://console.anthropic.com/\n")
    else:
        print("2️⃣  API KEY: ✅ Configurado\n")
    
    print("3️⃣  DEPLOYMENT EN RAILWAY:")
    print("   - Lee: RAILWAY_DEPLOYMENT.md")
    print("   - O usa: railway init && railway up\n")
    
    print("4️⃣  USAR CURSOR:")
    print("   - Abre proyecto en Cursor")
    print("   - .cursorrules está configurado")
    print("   - Usa Cursor AI para ayuda contextual\n")
    
    print("5️⃣  DOCUMENTACIÓN:")
    print("   - README_GITHUB.md - Guía completa")
    print("   - GUIA_RAPIDA.md - Inicio rápido")
    print("   - RAILWAY_DEPLOYMENT.md - Deploy en Railway\n")
    
    print("="*70)
    print("💡 TIP: Si usas Cursor, pregúntale cualquier duda sobre el código")
    print("="*70)

def main():
    """Main setup function"""
    print("\n" + "🍳 "*20)
    print_header("k[AI]tchen - Setup")
    print("🍳 "*20)
    
    config = {}
    
    # 1. Check dependencies
    deps_ok = check_dependencies()
    
    if not deps_ok:
        print("\n❌ Instala dependencias primero y vuelve a ejecutar")
        sys.exit(1)
    
    # 2. Setup .env
    env_created = setup_env_file()
    if env_created:
        # Check if key was added
        with open('.env', 'r') as f:
            content = f.read()
            config['anthropic_key'] = 'sk-ant-api03-your-key-here' not in content
    
    # 3. Initialize database
    db_ok = init_database()
    
    # 4. Check Cursor
    check_cursor_config()
    
    # 5. Setup Git
    setup_git()
    
    # Print next steps
    print_next_steps(config)
    
    print("\n✨ Setup completado. ¡Feliz coding!\n")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup cancelado por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Error durante setup: {e}")
        sys.exit(1)
