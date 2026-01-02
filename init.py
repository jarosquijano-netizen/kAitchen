#!/usr/bin/env python3
"""
Script de inicialización para el sistema de gestión de menús familiares
Este script ayuda a configurar la base de datos y añadir perfiles de ejemplo
"""

import os
import sys
from database import Database

def init_database():
    """Inicializa la base de datos"""
    print("🔧 Inicializando base de datos...")
    db = Database()
    print("✅ Base de datos inicializada correctamente\n")
    return db

def add_sample_profiles(db):
    """Añade perfiles de ejemplo basados en la familia de 5 miembros en Barcelona"""
    print("👨‍👩‍👧‍👦 ¿Deseas añadir perfiles de ejemplo? (s/n): ", end="")
    response = input().strip().lower()
    
    if response != 's':
        return
    
    print("\n📝 Añadiendo perfiles de ejemplo...")
    
    # Adultos de ejemplo
    adulto1 = {
        'nombre': 'María',
        'edad': 38,
        'objetivo_alimentario': 'Salud general',
        'estilo_alimentacion': 'Omnívoro',
        'cocinas_favoritas': 'Mediterránea, Italiana',
        'nivel_picante': 'Medio',
        'ingredientes_favoritos': 'Verduras frescas, pescado, legumbres',
        'ingredientes_no_gustan': 'Vísceras',
        'alergias': '',
        'intolerancias': 'Lactosa (leve)',
        'restricciones_religiosas': '',
        'flexibilidad_comer': 'Alta',
        'preocupacion_principal': 'Balance nutricional',
        'tiempo_max_cocinar': 45,
        'nivel_cocina': 'Intermedio',
        'tipo_desayuno': 'Tostadas con aguacate',
        'le_gustan_snacks': True,
        'plato_favorito': 'Paella',
        'plato_menos_favorito': 'Casquería',
        'comentarios': 'Le gusta cocinar en familia'
    }
    
    adulto2 = {
        'nombre': 'Carlos',
        'edad': 40,
        'objetivo_alimentario': 'Mantener peso',
        'estilo_alimentacion': 'Omnívoro',
        'cocinas_favoritas': 'Española, Asiática',
        'nivel_picante': 'Alto',
        'ingredientes_favoritos': 'Carnes, arroces, especias',
        'ingredientes_no_gustan': 'Remolacha',
        'alergias': '',
        'intolerancias': '',
        'restricciones_religiosas': '',
        'flexibilidad_comer': 'Alta',
        'preocupacion_principal': 'Proteínas',
        'tiempo_max_cocinar': 30,
        'nivel_cocina': 'Básico',
        'tipo_desayuno': 'Café con tostadas',
        'le_gustan_snacks': True,
        'plato_favorito': 'Costillas a la brasa',
        'plato_menos_favorito': 'Ensaladas complejas',
        'comentarios': 'Prefiere platos contundentes'
    }
    
    adulto3 = {
        'nombre': 'Lucía',
        'edad': 65,
        'objetivo_alimentario': 'Salud cardiovascular',
        'estilo_alimentacion': 'Flexitariano',
        'cocinas_favoritas': 'Mediterránea, Casera',
        'nivel_picante': 'Bajo',
        'ingredientes_favoritos': 'Verduras, pescado, aceite de oliva',
        'ingredientes_no_gustan': 'Comida muy grasa',
        'alergias': '',
        'intolerancias': '',
        'restricciones_religiosas': '',
        'flexibilidad_comer': 'Media',
        'preocupacion_principal': 'Sal, grasas',
        'tiempo_max_cocinar': 60,
        'nivel_cocina': 'Avanzado',
        'tipo_desayuno': 'Fruta y yogur',
        'le_gustan_snacks': False,
        'plato_favorito': 'Lentejas guisadas',
        'plato_menos_favorito': 'Comida rápida',
        'comentarios': 'Prefiere cocina tradicional y saludable'
    }
    
    # Niñas de ejemplo
    nina1 = {
        'nombre': 'Emma',
        'edad': 12,
        'come_solo': 'Solo',
        'nivel_exigencia': 'Medio',
        'cocinas_gustan': 'Italiana, Japonesa',
        'ingredientes_favoritos': 'Pasta, pollo, arroz',
        'ingredientes_rechaza': 'Pescado azul',
        'texturas_no_gustan': 'Gelatinosas',
        'alergias': '',
        'intolerancias': '',
        'verduras_aceptadas': 'Zanahoria, tomate, lechuga',
        'verduras_rechazadas': 'Brócoli, coliflor',
        'nivel_picante': 'Nada',
        'desayuno_preferido': 'Cereales con leche',
        'snacks_favoritos': 'Fruta, galletas',
        'acepta_comida_nueva': 'A veces',
        'plato_favorito': 'Pizza',
        'plato_nunca_comeria': 'Sushi con pescado crudo',
        'comentarios_padres': 'Le gusta ayudar en la cocina, selectiva con las verduras'
    }
    
    nina2 = {
        'nombre': 'Sofía',
        'edad': 4,
        'come_solo': 'Con ayuda',
        'nivel_exigencia': 'Alto',
        'cocinas_gustan': 'Casera simple',
        'ingredientes_favoritos': 'Pollo, patatas, pasta',
        'ingredientes_rechaza': 'Pescado, verduras',
        'texturas_no_gustan': 'Fibrosas, pegajosas',
        'alergias': '',
        'intolerancias': '',
        'verduras_aceptadas': 'Patatas, guisantes',
        'verduras_rechazadas': 'Casi todas las demás',
        'nivel_picante': 'Nada',
        'desayuno_preferido': 'Pan con mantequilla',
        'snacks_favoritos': 'Galletas, yogur',
        'acepta_comida_nueva': 'No',
        'plato_favorito': 'Macarrones con tomate',
        'plato_nunca_comeria': 'Ensalada',
        'comentarios_padres': 'Muy selectiva, necesita presentación atractiva. Le gusta que la comida sea "bonita"'
    }
    
    # Añadir a la base de datos
    try:
        db.add_adult(adulto1)
        db.add_adult(adulto2)
        db.add_adult(adulto3)
        print("✅ Añadidos 3 perfiles de adultos")
        
        db.add_child(nina1)
        db.add_child(nina2)
        print("✅ Añadidos 2 perfiles de niños")
        
        print("\n✨ Perfiles de ejemplo añadidos correctamente\n")
    except Exception as e:
        print(f"❌ Error al añadir perfiles: {e}\n")

def check_api_key():
    """Verifica que la API key esté configurada"""
    print("🔑 Verificando configuración de API key...")
    
    api_key = os.getenv('ANTHROPIC_API_KEY')
    
    if not api_key or api_key == 'tu_api_key_aqui':
        print("\n⚠️  ATENCIÓN: No se ha configurado la API key de Anthropic")
        print("\nPara generar menús con IA, necesitas:")
        print("1. Obtener una API key en: https://console.anthropic.com/")
        print("2. Copiar .env.example a .env")
        print("3. Añadir tu API key en el archivo .env")
        print("\n💡 Puedes usar el sistema sin API key, pero no podrás generar menús automáticos\n")
        return False
    else:
        print("✅ API key configurada correctamente\n")
        return True

def main():
    """Función principal"""
    print("=" * 60)
    print("🍳 SISTEMA DE GESTIÓN DE MENÚS FAMILIARES")
    print("   Inicialización")
    print("=" * 60)
    print()
    
    # Inicializar base de datos
    db = init_database()
    
    # Añadir perfiles de ejemplo
    add_sample_profiles(db)
    
    # Verificar API key
    check_api_key()
    
    print("=" * 60)
    print("✅ Inicialización completada")
    print("=" * 60)
    print("\n📱 Para iniciar la aplicación, ejecuta:")
    print("   python app.py")
    print("\n🌐 Luego accede a: http://localhost:5000")
    print("📺 Vista TV: http://localhost:5000/tv")
    print()

if __name__ == '__main__':
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    main()
