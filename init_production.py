#!/usr/bin/env python3
"""
Script de inicialización para producción en Railway
Usa DATABASE_URL pública para evitar problemas de DNS interno
"""

import os
import sys
from database import Database

def init_production_database():
    """Inicializa la base de datos en producción usando URL pública"""
    print("🔧 Inicializando base de datos de producción...")
    
    # Construir URL pública usando variables de entorno
    db_url = (
        f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
        f"@{os.getenv('RAILWAY_TCP_PROXY_DOMAIN')}:{os.getenv('RAILWAY_TCP_PROXY_PORT')}"
        f"/{os.getenv('POSTGRES_DB', 'railway')}"
    )
    
    print(f"📊 Usando URL: postgresql://***@{os.getenv('RAILWAY_TCP_PROXY_DOMAIN')}:{os.getenv('RAILWAY_TCP_PROXY_PORT')}")
    
    try:
        # Inicializar con URL pública
        db = Database(db_url)
        print("✅ Base de datos inicializada correctamente")
        
        # Añadir perfiles de ejemplo automáticamente
        add_sample_profiles(db)
        
        return db
    except Exception as e:
        print(f"❌ Error inicializando base de datos: {e}")
        return None

def add_sample_profiles(db):
    """Añade perfiles de ejemplo automáticamente"""
    print("👨‍👩‍👧‍👦 Añadiendo perfiles de ejemplo...")
    
    try:
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
            'edad': 42,
            'objetivo_alimentario': 'Mantener peso',
            'estilo_alimentacion': 'Omnívoro',
            'cocinas_favoritas': 'Asiática, Mexicana',
            'nivel_picante': 'Alto',
            'ingredientes_favoritos': 'Pollo, arroz, especias',
            'ingredientes_no_gustan': 'Repollo',
            'alergias': '',
            'intolerancias': '',
            'restricciones_religiosas': '',
            'flexibilidad_comer': 'Media',
            'preocupacion_principal': 'Proteína',
            'tiempo_max_cocinar': 60,
            'nivel_cocina': 'Avanzado',
            'tipo_desayuno': 'Huevos revueltos',
            'le_gustan_snacks': True,
            'plato_favorito': 'Curry',
            'plato_menos_favorito': 'Ensaladas',
            'comentarios': 'Le gusta experimentar'
        }
        
        # Niños de ejemplo
        nino1 = {
            'nombre': 'Sofía',
            'edad': 12,
            'nivel_exigencia': 'Medio',
            'acepta_comida_nueva': 'A veces',
            'alergias': '',
            'intolerancias': '',
            'ingredientes_favoritos': 'Pasta, pollo, queso',
            'ingredientes_rechaza': 'Pimientos, cebolla',
            'verduras_aceptadas': 'Zanahoria, guisantes, tomate',
            'verduras_rechazadas': 'Brócoli, espinaca',
            'texturas_no_gustan': 'Blandas, gelatinosas',
            'comentarios_padres': 'Le gusta la comida simple'
        }
        
        nino2 = {
            'nombre': 'Lucas',
            'edad': 8,
            'nivel_exigencia': 'Alto',
            'acepta_comida_nueva': 'No',
            'alergias': 'Frutos secos',
            'intolerancias': '',
            'ingredientes_favoritos': 'Nuggets, patatas fritas',
            'ingredientes_rechaza': 'Verduras verdes',
            'verduras_aceptadas': 'Zanahoria, guisantes',
            'verduras_rechazadas': 'Brócoli, espinaca, lechuga',
            'texturas_no_gustan': 'Crujientes, duras',
            'comentarios_padres': 'Muy selectivo, necesita paciencia'
        }
        
        nino3 = {
            'nombre': 'Emma',
            'edad': 5,
            'nivel_exigencia': 'Bajo',
            'acepta_comida_nueva': 'Sí',
            'alergias': '',
            'intolerancias': '',
            'ingredientes_favoritos': 'Fruta, yogur, galletas',
            'ingredientes_rechaza': 'Nada específico',
            'verduras_aceptadas': 'Todas',
            'verduras_rechazadas': '',
            'texturas_no_gustan': '',
            'comentarios_padres': 'Come de todo, muy fácil'
        }
        
        # Guardar en base de datos
        db.add_adult(adulto1)
        db.add_adult(adulto2)
        db.add_child(nino1)
        db.add_child(nino2)
        db.add_child(nino3)
        
        print("✅ Perfiles de ejemplo añadidos:")
        print("   👩 Adultos: María (38), Carlos (42)")
        print("   👧 Niños: Sofía (12), Lucas (8), Emma (5)")
        
    except Exception as e:
        print(f"❌ Error añadiendo perfiles: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("🍳 INICIALIZACIÓN DE PRODUCCIÓN - RAILWAY")
    print("=" * 60)
    
    db = init_production_database()
    
    if db:
        print("\n" + "=" * 60)
        print("✅ INICIALIZACIÓN COMPLETADA")
        print("🌐 Aplicación lista para usar en producción")
        print("📺 URL de TV: https://web-production-57291.up.railway.app/tv")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ ERROR EN INICIALIZACIÓN")
        print("🔧 Revisa la configuración de la base de datos")
        print("=" * 60)
