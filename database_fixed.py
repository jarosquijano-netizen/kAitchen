#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database management module for Family Kitchen Menu System
Supports both SQLite (local) and PostgreSQL (production)
"""
import os
import sqlite3
import json
from typing import Dict, List, Optional
from datetime import datetime

try:
    from psycopg2.pool import SimpleConnectionPool
    from psycopg2.extras import RealDictCursor
    POSTGRES_AVAILABLE = True
except ImportError:
    POSTGRES_AVAILABLE = False


class Database:
    """Database abstraction layer supporting SQLite and PostgreSQL"""
    
    def __init__(self, db_url: Optional[str] = None):
        """
        Initialize database connection
        Args:
            db_url: Database URL (sqlite:///path/to/db or postgresql://...)
                    If None, uses DATABASE_URL from environment or defaults to SQLite
        """
        # Try individual PostgreSQL variables first (Railway compatibility)
        if os.getenv('POSTGRES_USER') and os.getenv('POSTGRES_PASSWORD'):
            self.db_url = (
                f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
                f"@{os.getenv('PGHOST', 'postgres.railway.internal')}:{os.getenv('PGPORT', '5432')}"
                f"/{os.getenv('POSTGRES_DB', 'railway')}"
            )
        else:
            self.db_url = (db_url or os.getenv('DATABASE_URL', 'sqlite:///family_kitchen.db')).strip()
        
        # Debug: Print database URL (first 50 chars only for security)
        db_url_preview = self.db_url[:50] + '...' if len(self.db_url) > 50 else self.db_url
        print(f"[Database] Initializing with DB URL: {db_url_preview}")
        
        # Check for PostgreSQL - support both postgresql:// and postgres://
        self.is_postgres = (
            self.db_url.startswith('postgresql://') or 
            self.db_url.startswith('postgres://')
        )
        
        print(f"[Database] Is PostgreSQL: {self.is_postgres}")
        
        if self.is_postgres and not POSTGRES_AVAILABLE:
            raise ImportError("psycopg2 is required for PostgreSQL support")
        
        # Initialize database tables with error handling
        try:
            print("[Database] Initializing database tables...")
            self.init_database()
            print("[Database] Database tables initialized successfully")
        except Exception as e:
            print(f"[Database] Error initializing database: {e}")
            # Don't raise here - allow app to start and show error in web interface
    
    def get_connection(self):
        """Get database connection"""
        if self.is_postgres:
            # PostgreSQL connection pool with timeout
            if not hasattr(self, '_pool'):
                try:
                    self._pool = SimpleConnectionPool(
                        1, 10, self.db_url,
                        connect_timeout=10,
                        options="-c statement_timeout=30000"
                    )
                    print("[Database] PostgreSQL connection pool created successfully")
                except Exception as e:
                    print(f"[Database] Error creating PostgreSQL pool: {e}")
                    raise
            return self._pool.getconn()
        else:
            # SQLite connection
            db_path = self.db_url.replace('sqlite:///', '')
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row
            return conn
    
    def _close_connection(self, conn):
        """Close or return connection to pool"""
        if conn:
            if self.is_postgres:
                self._pool.putconn(conn)
            else:
                conn.close()
    
    def init_database(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if self.is_postgres:
            # PostgreSQL table creation
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS adults (
                    id SERIAL PRIMARY KEY,
                    nombre TEXT NOT NULL,
                    edad INTEGER,
                    objetivo_alimentario TEXT,
                    estilo_alimentacion TEXT,
                    cocinas_favoritas TEXT,
                    nivel_picante TEXT,
                    ingredientes_favoritos TEXT,
                    ingredientes_no_gustan TEXT,
                    alergias TEXT,
                    intolerancias TEXT,
                    restricciones_religiosas TEXT,
                    flexibilidad_comer TEXT,
                    preocupacion_principal TEXT,
                    tiempo_max_cocinar INTEGER,
                    nivel_cocina TEXT,
                    tipo_desayuno TEXT,
                    le_gustan_snacks BOOLEAN,
                    plato_favorito TEXT,
                    plato_menos_favorito TEXT,
                    comentarios TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS children (
                    id SERIAL PRIMARY KEY,
                    nombre TEXT NOT NULL,
                    edad INTEGER,
                    come_solo TEXT,
                    nivel_exigencia TEXT,
                    cocinas_gustan TEXT,
                    ingredientes_favoritos TEXT,
                    ingredientes_rechaza TEXT,
                    texturas_no_gustan TEXT,
                    alergias TEXT,
                    intolerancias TEXT,
                    verduras_aceptadas TEXT,
                    verduras_rechazadas TEXT,
                    nivel_picante TEXT,
                    desayuno_preferido TEXT,
                    snacks_favoritos TEXT,
                    acepta_comida_nueva TEXT,
                    plato_favorito TEXT,
                    plato_nunca_comeria TEXT,
                    comentarios TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS recipes (
                    id SERIAL PRIMARY KEY,
                    nombre TEXT NOT NULL,
                    descripcion TEXT,
                    ingredientes TEXT,
                    instrucciones TEXT,
                    tiempo_preparacion INTEGER,
                    dificultad INTEGER,
                    tipo_plato TEXT,
                    origen_receta TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS weekly_menus (
                    id SERIAL PRIMARY KEY,
                    menu_id TEXT NOT NULL,
                    day_name TEXT NOT NULL,
                    menu_type TEXT NOT NULL,
                    menu_data TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(menu_id, day_name, menu_type)
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS menu_preferences (
                    id SERIAL PRIMARY KEY,
                    include_weekend BOOLEAN DEFAULT TRUE,
                    include_breakfast BOOLEAN DEFAULT TRUE,
                    include_lunch BOOLEAN DEFAULT TRUE,
                    include_dinner BOOLEAN DEFAULT TRUE,
                    excluded_days TEXT DEFAULT '[]',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS menu_day_ratings (
                    id SERIAL PRIMARY KEY,
                    menu_id TEXT NOT NULL,
                    day_name TEXT NOT NULL,
                    menu_type TEXT NOT NULL,
                    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
                    comentarios TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(menu_id, day_name, menu_type)
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS house_config (
                    id SERIAL PRIMARY KEY,
                    config_key TEXT NOT NULL UNIQUE,
                    config_value TEXT,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS cleaning_capacity (
                    id SERIAL PRIMARY KEY,
                    member_id INTEGER NOT NULL,
                    capacity_level INTEGER DEFAULT 3,
                    max_tasks_per_day INTEGER DEFAULT 2,
                    areas_preferidas TEXT DEFAULT '[]',
                    areas_evitar TEXT DEFAULT '[]',
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
        else:
            # SQLite table creation
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS adults (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    edad INTEGER,
                    objetivo_alimentario TEXT,
                    estilo_alimentacion TEXT,
                    cocinas_favoritas TEXT,
                    nivel_picante TEXT,
                    ingredientes_favoritos TEXT,
                    ingredientes_no_gustan TEXT,
                    alergias TEXT,
                    intolerancias TEXT,
                    restricciones_religiosas TEXT,
                    flexibilidad_comer TEXT,
                    preocupacion_principal TEXT,
                    tiempo_max_cocinar INTEGER,
                    nivel_cocina TEXT,
                    tipo_desayuno TEXT,
                    le_gustan_snacks BOOLEAN,
                    plato_favorito TEXT,
                    plato_menos_favorito TEXT,
                    comentarios TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS children (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    edad INTEGER,
                    come_solo TEXT,
                    nivel_exigencia TEXT,
                    cocinas_gustan TEXT,
                    ingredientes_favoritos TEXT,
                    ingredientes_rechaza TEXT,
                    texturas_no_gustan TEXT,
                    alergias TEXT,
                    intolerancias TEXT,
                    verduras_aceptadas TEXT,
                    verduras_rechazadas TEXT,
                    nivel_picante TEXT,
                    desayuno_preferido TEXT,
                    snacks_favoritos TEXT,
                    acepta_comida_nueva TEXT,
                    plato_favorito TEXT,
                    plato_nunca_comeria TEXT,
                    comentarios TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS recipes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    descripcion TEXT,
                    ingredientes TEXT,
                    instrucciones TEXT,
                    tiempo_preparacion INTEGER,
                    dificultad INTEGER,
                    tipo_plato TEXT,
                    origen_receta TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS weekly_menus (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    menu_id TEXT NOT NULL,
                    day_name TEXT NOT NULL,
                    menu_type TEXT NOT NULL,
                    menu_data TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(menu_id, day_name, menu_type)
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS menu_preferences (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    include_weekend BOOLEAN DEFAULT TRUE,
                    include_breakfast BOOLEAN DEFAULT TRUE,
                    include_lunch BOOLEAN DEFAULT TRUE,
                    include_dinner BOOLEAN DEFAULT TRUE,
                    excluded_days TEXT DEFAULT '[]',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS menu_day_ratings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    menu_id TEXT NOT NULL,
                    day_name TEXT NOT NULL,
                    menu_type TEXT NOT NULL,
                    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
                    comentarios TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(menu_id, day_name, menu_type)
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS house_config (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    config_key TEXT NOT NULL UNIQUE,
                    config_value TEXT,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS cleaning_capacity (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    member_id INTEGER NOT NULL,
                    capacity_level INTEGER DEFAULT 3,
                    max_tasks_per_day INTEGER DEFAULT 2,
                    areas_preferidas TEXT DEFAULT '[]',
                    areas_evitar TEXT DEFAULT '[]',
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
        
        # Initialize default preferences if table is empty
        cursor.execute('SELECT COUNT(*) FROM menu_preferences')
        count = cursor.fetchone()[0] if self.is_postgres else cursor.fetchone()[0]
        if count == 0:
            if self.is_postgres:
                cursor.execute('''
                    INSERT INTO menu_preferences 
                    (include_weekend, include_breakfast, include_lunch, include_dinner, excluded_days)
                    VALUES (TRUE, TRUE, TRUE, TRUE, '[]')
                ''')
            else:
                cursor.execute('''
                    INSERT INTO menu_preferences 
                    (include_weekend, include_breakfast, include_lunch, include_dinner, excluded_days)
                    VALUES (1, 1, 1, 1, '[]')
                ''')
        
        # Cleaning tables - PostgreSQL
        if self.is_postgres:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS cleaning_tasks (
                    id SERIAL PRIMARY KEY,
                    nombre TEXT NOT NULL,
                    descripcion TEXT,
                    area TEXT NOT NULL,
                    dificultad INTEGER DEFAULT 1 CHECK (dificultad >= 1 AND dificultad <= 5),
                    frecuencia TEXT NOT NULL,
                    tiempo_estimado INTEGER,
                    herramientas TEXT,
                    dias_semana TEXT DEFAULT '[]',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS cleaning_assignments (
                    id SERIAL PRIMARY KEY,
                    task_id INTEGER NOT NULL REFERENCES cleaning_tasks(id),
                    member_id INTEGER NOT NULL,
                    member_type TEXT NOT NULL,
                    dia_semana TEXT NOT NULL,
                    week_start DATE NOT NULL,
                    fecha_especifica DATE,
                    tipo_asignacion TEXT DEFAULT 'semanal',
                    semana_referencia DATE,
                    completado BOOLEAN DEFAULT FALSE,
                    notas TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(task_id, member_id, week_start)
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS cleaning_preferences (
                    id SERIAL PRIMARY KEY,
                    asignacion_automatica BOOLEAN DEFAULT TRUE,
                    dias_trabajo TEXT DEFAULT '[]',
                    areas_preferidas TEXT DEFAULT '[]',
                    areas_evitar TEXT DEFAULT '[]',
                    dificultad_maxima INTEGER DEFAULT 3,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
        else:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS cleaning_tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    descripcion TEXT,
                    area TEXT NOT NULL,
                    dificultad INTEGER DEFAULT 1 CHECK (dificultad >= 1 AND dificultad <= 5),
                    frecuencia TEXT NOT NULL,
                    tiempo_estimado INTEGER,
                    herramientas TEXT,
                    dias_semana TEXT DEFAULT '[]',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS cleaning_assignments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_id INTEGER NOT NULL,
                    member_id INTEGER NOT NULL,
                    member_type TEXT NOT NULL,
                    dia_semana TEXT NOT NULL,
                    week_start DATE NOT NULL,
                    fecha_especifica DATE,
                    tipo_asignacion TEXT DEFAULT 'semanal',
                    semana_referencia DATE,
                    completado BOOLEAN DEFAULT FALSE,
                    notas TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(task_id, member_id, week_start)
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS cleaning_preferences (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    asignacion_automatica BOOLEAN DEFAULT TRUE,
                    dias_trabajo TEXT DEFAULT '[]',
                    areas_preferidas TEXT DEFAULT '[]',
                    areas_evitar TEXT DEFAULT '[]',
                    dificultad_maxima INTEGER DEFAULT 3,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
        
        conn.commit()
        self._close_connection(conn)
        print("[Database] Database initialization completed")
