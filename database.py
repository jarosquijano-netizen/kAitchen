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
                    comentarios_padres TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS recipes (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    url TEXT,
                    ingredients TEXT,
                    instructions TEXT,
                    prep_time INTEGER,
                    cook_time INTEGER,
                    servings INTEGER,
                    cuisine_type TEXT,
                    meal_type TEXT,
                    difficulty TEXT,
                    image_url TEXT,
                    extracted_data TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS weekly_menus (
                    id SERIAL PRIMARY KEY,
                    week_start_date DATE NOT NULL,
                    menu_data TEXT,
                    metadata TEXT,
                    rating INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS menu_preferences (
                    id SERIAL PRIMARY KEY,
                    include_weekend BOOLEAN DEFAULT TRUE,
                    include_breakfast BOOLEAN DEFAULT TRUE,
                    include_lunch BOOLEAN DEFAULT TRUE,
                    include_dinner BOOLEAN DEFAULT TRUE,
                    excluded_days TEXT,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS menu_day_ratings (
                    id SERIAL PRIMARY KEY,
                    menu_id INTEGER NOT NULL,
                    week_start_date DATE NOT NULL,
                    day_name TEXT NOT NULL,
                    menu_type TEXT NOT NULL,
                    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(menu_id, day_name, menu_type)
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
                    comentarios_padres TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS recipes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    url TEXT,
                    ingredients TEXT,
                    instructions TEXT,
                    prep_time INTEGER,
                    cook_time INTEGER,
                    servings INTEGER,
                    cuisine_type TEXT,
                    meal_type TEXT,
                    difficulty TEXT,
                    image_url TEXT,
                    extracted_data TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS weekly_menus (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    week_start_date DATE NOT NULL,
                    menu_data TEXT,
                    metadata TEXT,
                    rating INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS menu_preferences (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    include_weekend BOOLEAN DEFAULT 1,
                    include_breakfast BOOLEAN DEFAULT 1,
                    include_lunch BOOLEAN DEFAULT 1,
                    include_dinner BOOLEAN DEFAULT 1,
                    excluded_days TEXT,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS menu_day_ratings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    menu_id INTEGER NOT NULL,
                    week_start_date DATE NOT NULL,
                    day_name TEXT NOT NULL,
                    menu_type TEXT NOT NULL,
                    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(menu_id, day_name, menu_type)
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
            
            # Cleaning tables
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
    
    # ==================== ADULT PROFILES ====================
    
    def add_adult(self, profile: Dict) -> int:
        """Add adult profile"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if self.is_postgres:
            cursor.execute('''
                INSERT INTO adults (nombre, edad, objetivo_alimentario, estilo_alimentacion,
                    cocinas_favoritas, nivel_picante, ingredientes_favoritos, ingredientes_no_gustan,
                    alergias, intolerancias, restricciones_religiosas, flexibilidad_comer,
                    preocupacion_principal, tiempo_max_cocinar, nivel_cocina, tipo_desayuno,
                    le_gustan_snacks, plato_favorito, plato_menos_favorito, comentarios)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            ''', (
                profile.get('nombre'), profile.get('edad'), profile.get('objetivo_alimentario'),
                profile.get('estilo_alimentacion'), profile.get('cocinas_favoritas'),
                profile.get('nivel_picante'), profile.get('ingredientes_favoritos'),
                profile.get('ingredientes_no_gustan'), profile.get('alergias'),
                profile.get('intolerancias'), profile.get('restricciones_religiosas'),
                profile.get('flexibilidad_comer'), profile.get('preocupacion_principal'),
                profile.get('tiempo_max_cocinar'), profile.get('nivel_cocina'),
                profile.get('tipo_desayuno'), profile.get('le_gustan_snacks'),
                profile.get('plato_favorito'), profile.get('plato_menos_favorito'),
                profile.get('comentarios')
            ))
            adult_id = cursor.fetchone()[0]
        else:
            cursor.execute('''
                INSERT INTO adults (nombre, edad, objetivo_alimentario, estilo_alimentacion,
                    cocinas_favoritas, nivel_picante, ingredientes_favoritos, ingredientes_no_gustan,
                    alergias, intolerancias, restricciones_religiosas, flexibilidad_comer,
                    preocupacion_principal, tiempo_max_cocinar, nivel_cocina, tipo_desayuno,
                    le_gustan_snacks, plato_favorito, plato_menos_favorito, comentarios)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                profile.get('nombre'), profile.get('edad'), profile.get('objetivo_alimentario'),
                profile.get('estilo_alimentacion'), profile.get('cocinas_favoritas'),
                profile.get('nivel_picante'), profile.get('ingredientes_favoritos'),
                profile.get('ingredientes_no_gustan'), profile.get('alergias'),
                profile.get('intolerancias'), profile.get('restricciones_religiosas'),
                profile.get('flexibilidad_comer'), profile.get('preocupacion_principal'),
                profile.get('tiempo_max_cocinar'), profile.get('nivel_cocina'),
                profile.get('tipo_desayuno'), profile.get('le_gustan_snacks'),
                profile.get('plato_favorito'), profile.get('plato_menos_favorito'),
                profile.get('comentarios')
            ))
            adult_id = cursor.lastrowid
        
        conn.commit()
        self._close_connection(conn)
        return adult_id
    
    def get_all_adults(self) -> List[Dict]:
        """Get all adult profiles"""
        conn = self.get_connection()
        try:
            if self.is_postgres:
                cursor = conn.cursor(cursor_factory=RealDictCursor)
                cursor.execute('SELECT * FROM adults ORDER BY nombre')
            else:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM adults ORDER BY nombre')
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            self._close_connection(conn)
    
    def update_adult(self, adult_id: int, profile: Dict) -> bool:
        """Update adult profile"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Build dynamic update query
            set_clause = []
            values = []
            
            for key, value in profile.items():
                if key != 'id':  # Don't update the ID
                    set_clause.append(f"{key} = ?")
                    values.append(value)
            
            if not set_clause:
                return False  # Nothing to update
            
            values.append(adult_id)
            
            if self.is_postgres:
                query = f"UPDATE adults SET {', '.join(set_clause)} WHERE id = %s"
                cursor.execute(query, values)
            else:
                query = f"UPDATE adults SET {', '.join(set_clause)} WHERE id = ?"
                cursor.execute(query, values)
            
            conn.commit()
            success = cursor.rowcount > 0
            return success
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            self._close_connection(conn)
    
    def delete_adult(self, adult_id: int) -> bool:
        """Delete adult profile"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if self.is_postgres:
            cursor.execute('DELETE FROM adults WHERE id = %s', (adult_id,))
        else:
            cursor.execute('DELETE FROM adults WHERE id = ?', (adult_id,))
        
        conn.commit()
        success = cursor.rowcount > 0
        self._close_connection(conn)
        return success
    
    # ==================== CHILDREN PROFILES ====================
    
    def add_child(self, profile: Dict) -> int:
        """Add child profile"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if self.is_postgres:
            cursor.execute('''
                INSERT INTO children (nombre, edad, come_solo, nivel_exigencia, cocinas_gustan,
                    ingredientes_favoritos, ingredientes_rechaza, texturas_no_gustan, alergias,
                    intolerancias, verduras_aceptadas, verduras_rechazadas, nivel_picante,
                    desayuno_preferido, snacks_favoritos, acepta_comida_nueva, plato_favorito,
                    plato_nunca_comeria, comentarios_padres)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            ''', (
                profile.get('nombre'), profile.get('edad'), profile.get('come_solo'),
                profile.get('nivel_exigencia'), profile.get('cocinas_gustan'),
                profile.get('ingredientes_favoritos'), profile.get('ingredientes_rechaza'),
                profile.get('texturas_no_gustan'), profile.get('alergias'),
                profile.get('intolerancias'), profile.get('verduras_aceptadas'),
                profile.get('verduras_rechazadas'), profile.get('nivel_picante'),
                profile.get('desayuno_preferido'), profile.get('snacks_favoritos'),
                profile.get('acepta_comida_nueva'), profile.get('plato_favorito'),
                profile.get('plato_nunca_comeria'), profile.get('comentarios_padres')
            ))
            child_id = cursor.fetchone()[0]
        else:
            cursor.execute('''
                INSERT INTO children (nombre, edad, come_solo, nivel_exigencia, cocinas_gustan,
                    ingredientes_favoritos, ingredientes_rechaza, texturas_no_gustan, alergias,
                    intolerancias, verduras_aceptadas, verduras_rechazadas, nivel_picante,
                    desayuno_preferido, snacks_favoritos, acepta_comida_nueva, plato_favorito,
                    plato_nunca_comeria, comentarios_padres)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                profile.get('nombre'), profile.get('edad'), profile.get('come_solo'),
                profile.get('nivel_exigencia'), profile.get('cocinas_gustan'),
                profile.get('ingredientes_favoritos'), profile.get('ingredientes_rechaza'),
                profile.get('texturas_no_gustan'), profile.get('alergias'),
                profile.get('intolerancias'), profile.get('verduras_aceptadas'),
                profile.get('verduras_rechazadas'), profile.get('nivel_picante'),
                profile.get('desayuno_preferido'), profile.get('snacks_favoritos'),
                profile.get('acepta_comida_nueva'), profile.get('plato_favorito'),
                profile.get('plato_nunca_comeria'), profile.get('comentarios_padres')
            ))
            child_id = cursor.lastrowid
        
        conn.commit()
        self._close_connection(conn)
        return child_id
    
    def get_all_children(self) -> List[Dict]:
        """Get all children profiles"""
        conn = self.get_connection()
        try:
            if self.is_postgres:
                cursor = conn.cursor(cursor_factory=RealDictCursor)
                cursor.execute('SELECT * FROM children ORDER BY nombre')
            else:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM children ORDER BY nombre')
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            self._close_connection(conn)
    
    def update_child(self, child_id: int, profile: Dict) -> bool:
        """Update child profile"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Build dynamic update query
            set_clause = []
            values = []
            
            for key, value in profile.items():
                if key != 'id':  # Don't update the ID
                    set_clause.append(f"{key} = ?")
                    values.append(value)
            
            if not set_clause:
                return False  # Nothing to update
            
            values.append(child_id)
            
            if self.is_postgres:
                query = f"UPDATE children SET {', '.join(set_clause)} WHERE id = %s"
                cursor.execute(query, values)
            else:
                query = f"UPDATE children SET {', '.join(set_clause)} WHERE id = ?"
                cursor.execute(query, values)
            
            conn.commit()
            success = cursor.rowcount > 0
            return success
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            self._close_connection(conn)
    
    def delete_child(self, child_id: int) -> bool:
        """Delete child profile"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if self.is_postgres:
            cursor.execute('DELETE FROM children WHERE id = %s', (child_id,))
        else:
            cursor.execute('DELETE FROM children WHERE id = ?', (child_id,))
        
        conn.commit()
        success = cursor.rowcount > 0
        self._close_connection(conn)
        return success
    
    # ==================== RECIPES ====================
    
    def add_recipe(self, recipe: Dict) -> int:
        """Add recipe"""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            ingredients_json = json.dumps(recipe.get('ingredients', []))
            extracted_data_json = json.dumps(recipe.get('extracted_data', {}))
            
            if self.is_postgres:
                cursor.execute('''
                    INSERT INTO recipes (title, url, ingredients, instructions, prep_time,
                        cook_time, servings, cuisine_type, meal_type, difficulty, image_url, extracted_data)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                ''', (
                    recipe.get('title'), recipe.get('url'), ingredients_json,
                    recipe.get('instructions'), recipe.get('prep_time'),
                    recipe.get('cook_time'), recipe.get('servings'),
                    recipe.get('cuisine_type'), recipe.get('meal_type'),
                    recipe.get('difficulty'), recipe.get('image_url'), extracted_data_json
                ))
                recipe_id = cursor.fetchone()[0]
            else:
                cursor.execute('''
                    INSERT INTO recipes (title, url, ingredients, instructions, prep_time,
                        cook_time, servings, cuisine_type, meal_type, difficulty, image_url, extracted_data)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    recipe.get('title'), recipe.get('url'), ingredients_json,
                    recipe.get('instructions'), recipe.get('prep_time'),
                    recipe.get('cook_time'), recipe.get('servings'),
                    recipe.get('cuisine_type'), recipe.get('meal_type'),
                    recipe.get('difficulty'), recipe.get('image_url'), extracted_data_json
                ))
                recipe_id = cursor.lastrowid
            
            conn.commit()
            print(f"[Database] Recipe saved: '{recipe.get('title')}' (ID: {recipe_id})")
            return recipe_id
        except Exception as e:
            print(f"[Database] Error saving recipe '{recipe.get('title')}': {str(e)}")
            if conn:
                conn.rollback()
            raise
        finally:
            self._close_connection(conn)
    
    def get_all_recipes(self) -> List[Dict]:
        """Get all recipes"""
        conn = self.get_connection()
        try:
            if self.is_postgres:
                cursor = conn.cursor(cursor_factory=RealDictCursor)
                cursor.execute('SELECT * FROM recipes ORDER BY title')
            else:
                # SQLite connection - row_factory already set in get_connection()
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM recipes ORDER BY title')
            
            rows = cursor.fetchall()
            
            recipes = []
            for row in rows:
                recipe = dict(row)
                
                # Parse JSON fields safely - only if they exist and are strings
                if 'ingredients' in recipe and recipe['ingredients']:
                    try:
                        recipe['ingredients'] = json.loads(recipe['ingredients'])
                    except (json.JSONDecodeError, TypeError):
                        pass  # Keep original value if parsing fails
                
                if 'extracted_data' in recipe and recipe['extracted_data']:
                    try:
                        recipe['extracted_data'] = json.loads(recipe['extracted_data'])
                    except (json.JSONDecodeError, TypeError):
                        recipe['extracted_data'] = {}  # Default to empty dict
                else:
                    recipe['extracted_data'] = {}
                
                recipes.append(recipe)
            
            return recipes
        finally:
            self._close_connection(conn)
    
    def delete_recipe(self, recipe_id: int) -> bool:
        """Delete recipe"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            
            if self.is_postgres:
                cursor.execute('DELETE FROM recipes WHERE id = %s', (recipe_id,))
            else:
                cursor.execute('DELETE FROM recipes WHERE id = ?', (recipe_id,))
            
            conn.commit()
            success = cursor.rowcount > 0
            return success
        finally:
            self._close_connection(conn)
    
    # ==================== WEEKLY MENUS ====================
    
    def save_weekly_menu(self, week_start_date: str, menu_data: Dict, metadata: Optional[Dict] = None) -> int:
        """
        Save weekly menu. If a menu already exists for this week_start_date, update it.
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        menu_json = json.dumps(menu_data)
        metadata_json = json.dumps(metadata or {})
        
        # Check if menu already exists for this week
        if self.is_postgres:
            cursor.execute('SELECT id FROM weekly_menus WHERE week_start_date = %s', (week_start_date,))
        else:
            cursor.execute('SELECT id FROM weekly_menus WHERE week_start_date = ?', (week_start_date,))
        
        existing = cursor.fetchone()
        
        if existing:
            # Update existing menu
            menu_id = existing[0] if self.is_postgres else existing['id']
            if self.is_postgres:
                cursor.execute('''
                    UPDATE weekly_menus 
                    SET menu_data = %s, metadata = %s, created_at = CURRENT_TIMESTAMP
                    WHERE id = %s
                ''', (menu_json, metadata_json, menu_id))
            else:
                cursor.execute('''
                    UPDATE weekly_menus 
                    SET menu_data = ?, metadata = ?, created_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (menu_json, metadata_json, menu_id))
        else:
            # Insert new menu
            if self.is_postgres:
                cursor.execute('''
                    INSERT INTO weekly_menus (week_start_date, menu_data, metadata)
                    VALUES (%s, %s, %s)
                    RETURNING id
                ''', (week_start_date, menu_json, metadata_json))
                menu_id = cursor.fetchone()[0]
            else:
                cursor.execute('''
                    INSERT INTO weekly_menus (week_start_date, menu_data, metadata)
                    VALUES (?, ?, ?)
                ''', (week_start_date, menu_json, metadata_json))
                menu_id = cursor.lastrowid
        
        conn.commit()
        self._close_connection(conn)
        return menu_id
    
    def get_latest_menu(self) -> Optional[Dict]:
        """Get most recent menu"""
        conn = self.get_connection()
        
        if self.is_postgres:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute('''
                SELECT * FROM weekly_menus 
                ORDER BY created_at DESC 
                LIMIT 1
            ''')
        else:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM weekly_menus 
                ORDER BY created_at DESC 
                LIMIT 1
            ''')
        
        row = cursor.fetchone()
        
        if row:
            menu = dict(row)
            menu['menu_data'] = json.loads(menu.get('menu_data', '{}'))
            menu['metadata'] = json.loads(menu.get('metadata', '{}'))
            self._close_connection(conn)
            return menu
        self._close_connection(conn)
        return None
    
    def get_menu_by_week_start(self, week_start_date: str) -> Optional[Dict]:
        """Get menu for specific week start date"""
        conn = self.get_connection()
        try:
            if self.is_postgres:
                cursor = conn.cursor(cursor_factory=RealDictCursor)
                cursor.execute('SELECT * FROM weekly_menus WHERE week_start_date = %s', (week_start_date,))
            else:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM weekly_menus WHERE week_start_date = ?', (week_start_date,))
            
            row = cursor.fetchone()
            
            if row:
                menu = dict(row)
                menu['menu_data'] = json.loads(menu.get('menu_data', '{}'))
                menu['metadata'] = json.loads(menu.get('metadata', '{}'))
                return menu
            return None
        finally:
            self._close_connection(conn)
    
    def get_all_menus(self) -> List[Dict]:
        """Get all weekly menus"""
        conn = self.get_connection()
        
        if self.is_postgres:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute('SELECT * FROM weekly_menus ORDER BY week_start_date DESC')
        else:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM weekly_menus ORDER BY week_start_date DESC')
        
        rows = cursor.fetchall()
        
        menus = []
        for row in rows:
            menu = dict(row)
            menu['menu_data'] = json.loads(menu.get('menu_data', '{}'))
            menu['metadata'] = json.loads(menu.get('metadata', '{}'))
            menus.append(menu)
        
        self._close_connection(conn)
        return menus
    
    # ==================== MENU DAY RATINGS ====================
    
    def rate_menu_day(self, menu_id: int, week_start_date: str, day_name: str, menu_type: str, rating: int) -> bool:
        """
        Rate a specific day menu (adults or children).
        
        Args:
            menu_id: ID of the weekly menu
            week_start_date: Week start date (YYYY-MM-DD)
            day_name: Day name (lunes, martes, etc.)
            menu_type: 'adultos' or 'ninos'
            rating: Rating from 1 to 5
        
        Returns:
            True if successful, False otherwise
        """
        if rating < 1 or rating > 5:
            return False
        
        if menu_type not in ['adultos', 'ninos']:
            return False
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            if self.is_postgres:
                cursor.execute('''
                    INSERT INTO menu_day_ratings (menu_id, week_start_date, day_name, menu_type, rating)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (menu_id, day_name, menu_type) 
                    DO UPDATE SET rating = %s, created_at = CURRENT_TIMESTAMP
                ''', (menu_id, week_start_date, day_name, menu_type, rating, rating))
            else:
                cursor.execute('''
                    INSERT OR REPLACE INTO menu_day_ratings (menu_id, week_start_date, day_name, menu_type, rating, created_at)
                    VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                ''', (menu_id, week_start_date, day_name, menu_type, rating))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"[Database] Error rating menu day: {e}")
            conn.rollback()
            return False
        finally:
            self._close_connection(conn)
    
    def get_menu_day_rating(self, menu_id: int, day_name: str, menu_type: str) -> Optional[int]:
        """
        Get rating for a specific day menu.
        
        Returns:
            Rating (1-5) or None if not rated
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            if self.is_postgres:
                cursor.execute('''
                    SELECT rating FROM menu_day_ratings
                    WHERE menu_id = %s AND day_name = %s AND menu_type = %s
                ''', (menu_id, day_name, menu_type))
            else:
                cursor.execute('''
                    SELECT rating FROM menu_day_ratings
                    WHERE menu_id = ? AND day_name = ? AND menu_type = ?
                ''', (menu_id, day_name, menu_type))
            
            row = cursor.fetchone()
            if row:
                return row[0] if self.is_postgres else row['rating']
            return None
        finally:
            self._close_connection(conn)
    
    def get_all_menu_ratings(self, limit: int = 50) -> List[Dict]:
        """
        Get all menu day ratings for AI learning.
        
        Returns:
            List of rating records with menu data
        """
        conn = self.get_connection()
        
        try:
            if self.is_postgres:
                cursor = conn.cursor(cursor_factory=RealDictCursor)
                cursor.execute('''
                    SELECT mdr.*, wm.menu_data
                    FROM menu_day_ratings mdr
                    JOIN weekly_menus wm ON mdr.menu_id = wm.id
                    ORDER BY mdr.created_at DESC
                    LIMIT %s
                ''', (limit,))
            else:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT mdr.*, wm.menu_data
                    FROM menu_day_ratings mdr
                    JOIN weekly_menus wm ON mdr.menu_id = wm.id
                    ORDER BY mdr.created_at DESC
                    LIMIT ?
                ''', (limit,))
            
            rows = cursor.fetchall()
            ratings = []
            for row in rows:
                rating = dict(row)
                if rating.get('menu_data'):
                    try:
                        rating['menu_data'] = json.loads(rating['menu_data'])
                    except:
                        pass
                ratings.append(rating)
            
            return ratings
        finally:
            self._close_connection(conn)
    
    # ==================== MENU PREFERENCES ====================
    
    def get_menu_preferences(self) -> Dict:
        """Get menu preferences"""
        conn = self.get_connection()
        
        if self.is_postgres:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute('SELECT * FROM menu_preferences ORDER BY id DESC LIMIT 1')
        else:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM menu_preferences ORDER BY id DESC LIMIT 1')
        
        row = cursor.fetchone()
        
        if row:
            prefs = dict(row)
            excluded_days = prefs.get('excluded_days', '[]')
            if isinstance(excluded_days, str):
                prefs['excluded_days'] = json.loads(excluded_days)
            self._close_connection(conn)
            return prefs
        
        self._close_connection(conn)
        
        # Return defaults if no preferences found
        return {
            'include_weekend': True,
            'include_breakfast': True,
            'include_lunch': True,
            'include_dinner': True,
            'excluded_days': []
        }
    
    def save_menu_preferences(self, preferences: Dict):
        """Save menu preferences"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        excluded_days_json = json.dumps(preferences.get('excluded_days', []))
        
        if self.is_postgres:
            cursor.execute('''
                INSERT INTO menu_preferences 
                (include_weekend, include_breakfast, include_lunch, include_dinner, excluded_days)
                VALUES (%s, %s, %s, %s, %s)
            ''', (
                preferences.get('include_weekend', True),
                preferences.get('include_breakfast', True),
                preferences.get('include_lunch', True),
                preferences.get('include_dinner', True),
                excluded_days_json
            ))
        else:
            cursor.execute('''
                INSERT INTO menu_preferences 
                (include_weekend, include_breakfast, include_lunch, include_dinner, excluded_days)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                preferences.get('include_weekend', True),
                preferences.get('include_breakfast', True),
                preferences.get('include_lunch', True),
                preferences.get('include_dinner', True),
                excluded_days_json
            ))
        
        conn.commit()
        self._close_connection(conn)
        return True
    
    # ==================== RECIPE EXTRACTION FROM MENU ====================
    
    def extract_and_save_recipes_from_menu(self, menu_data: Dict) -> List[int]:
        """
        Extract recipes from menu data and save them to the recipes table.
        Returns list of recipe IDs that were created/updated.
        """
        recipe_ids = []
        
        if not menu_data:
            return recipe_ids
        
        # Extract recipes from menu_adultos and menu_ninos
        for menu_type in ['menu_adultos', 'menu_ninos']:
            if menu_type not in menu_data:
                continue
            
            menu = menu_data[menu_type]
            if 'dias' not in menu:
                continue
            
            # Iterate through all days
            for day_name, day_data in menu['dias'].items():
                if not isinstance(day_data, dict):
                    continue
                
                # Check all meal types
                for meal_type in ['desayuno', 'comida', 'merienda', 'cena']:
                    if meal_type not in day_data:
                        continue
                    
                    meal = day_data[meal_type]
                    if not isinstance(meal, dict):
                        continue
                    
                    # Check if this meal has a recipe_base that's not "Original"
                    recipe_base = meal.get('receta_base', '')
                    if recipe_base and recipe_base.lower() != 'original':
                        # Check if recipe already exists
                        existing_recipe = self._find_recipe_by_title(recipe_base)
                        
                        if existing_recipe:
                            recipe_ids.append(existing_recipe['id'])
                        else:
                            # Create new recipe from menu meal
                            recipe_data = {
                                'title': recipe_base,
                                'ingredients': meal.get('ingredientes', []),
                                'instructions': meal.get('instrucciones', ''),
                                'prep_time': meal.get('tiempo_prep'),
                                'meal_type': meal_type,
                                'cuisine_type': '',  # Could be extracted from menu context
                                'servings': 4,  # Default
                                'extracted_data': {
                                    'source': 'menu_generated',
                                    'from_menu': True,
                                    'meal_type': meal_type,
                                    'day': day_name,
                                    'calorias': meal.get('calorias'),
                                    'nutrientes': meal.get('nutrientes', {}),
                                    'notas': meal.get('notas', ''),
                                    'porque_seleccionada': meal.get('porque_seleccionada', '')
                                }
                            }
                            recipe_id = self.add_recipe(recipe_data)
                            recipe_ids.append(recipe_id)
                            print(f"[Database] Saved recipe '{recipe_base}' from menu (ID: {recipe_id})")
        
        return recipe_ids
    
    def _find_recipe_by_title(self, title: str) -> Optional[Dict]:
        """Find a recipe by title (case-insensitive)"""
        conn = self.get_connection()
        
        if self.is_postgres:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute('SELECT * FROM recipes WHERE LOWER(title) = LOWER(%s) LIMIT 1', (title,))
        else:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM recipes WHERE LOWER(title) = LOWER(?) LIMIT 1', (title,))
        
        row = cursor.fetchone()
        
        if row:
            recipe = dict(row)
            recipe['ingredients'] = json.loads(recipe.get('ingredients', '[]'))
            recipe['extracted_data'] = json.loads(recipe.get('extracted_data', '{}'))
            self._close_connection(conn)
            return recipe
        self._close_connection(conn)
        return None
    
    def rate_menu(self, menu_id: int, rating: int) -> bool:
        """
        Rate a menu (1-5 stars).
        Returns True if successful, False otherwise.
        """
        if rating < 1 or rating > 5:
            return False
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if self.is_postgres:
            cursor.execute('''
                UPDATE weekly_menus 
                SET rating = %s 
                WHERE id = %s
            ''', (rating, menu_id))
        else:
            cursor.execute('''
                UPDATE weekly_menus 
                SET rating = ? 
                WHERE id = ?
            ''', (rating, menu_id))
        
        conn.commit()
        self._close_connection(conn)
        return True
    
    def get_highly_rated_menus(self, min_rating: int = 4, limit: int = 10) -> List[Dict]:
        """
        Get menus with high ratings to use as examples for AI learning.
        Returns list of menu data with ratings >= min_rating.
        """
        conn = self.get_connection()
        
        if self.is_postgres:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute('''
                SELECT week_start_date, menu_data, rating, created_at
                FROM weekly_menus 
                WHERE rating >= %s 
                ORDER BY rating DESC, created_at DESC 
                LIMIT %s
            ''', (min_rating, limit))
        else:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('''
                SELECT week_start_date, menu_data, rating, created_at
                FROM weekly_menus 
                WHERE rating >= ? 
                ORDER BY rating DESC, created_at DESC 
                LIMIT ?
            ''', (min_rating, limit))
        
        rows = cursor.fetchall()
        
        menus = []
        for row in rows:
            menu = dict(row)
            menu['menu_data'] = json.loads(menu.get('menu_data', '{}'))
            menus.append(menu)
        
        self._close_connection(conn)
        return menus
    
    # ==================== CLEANING METHODS ====================
    
    def get_all_cleaning_tasks(self) -> List[Dict]:
        """Get all cleaning tasks"""
        conn = self.get_connection()
        
        if self.is_postgres:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute('SELECT * FROM cleaning_tasks ORDER BY area, nombre')
        else:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM cleaning_tasks ORDER BY area, nombre')
        
        rows = cursor.fetchall()
        self._close_connection(conn)
        return [dict(row) for row in rows]
    
    def add_cleaning_task(self, task: Dict) -> int:
        """Add a new cleaning task"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if self.is_postgres:
            cursor.execute('''
                INSERT INTO cleaning_tasks (nombre, descripcion, area, dificultad, frecuencia, 
                    tiempo_estimado, herramientas)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            ''', (
                task.get('nombre'), task.get('descripcion'), task.get('area'),
                task.get('dificultad', 1), task.get('frecuencia'),
                task.get('tiempo_estimado'), task.get('herramientas')
            ))
            task_id = cursor.fetchone()[0]
        else:
            cursor.execute('''
                INSERT INTO cleaning_tasks (nombre, descripcion, area, dificultad, frecuencia, 
                    tiempo_estimado, herramientas)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                task.get('nombre'), task.get('descripcion'), task.get('area'),
                task.get('dificultad', 1), task.get('frecuencia'),
                task.get('tiempo_estimado'), task.get('herramientas')
            ))
            task_id = cursor.lastrowid
        
        conn.commit()
        self._close_connection(conn)
        return task_id
    
    def save_cleaning_assignment(self, assignment: Dict) -> int:
        """Save a cleaning assignment"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if self.is_postgres:
            cursor.execute('''
                INSERT INTO cleaning_assignments (task_id, member_id, member_type, 
                    dia_semana, week_start, completado, notas)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (task_id, member_id, week_start) 
                DO UPDATE SET dia_semana = EXCLUDED.dia_semana, 
                              member_type = EXCLUDED.member_type,
                              completado = EXCLUDED.completado,
                              notas = EXCLUDED.notas
                RETURNING id
            ''', (
                assignment.get('task_id'), assignment.get('member_id'),
                assignment.get('member_type'), assignment.get('dia_semana'),
                assignment.get('week_start'), assignment.get('completado', False),
                assignment.get('notas')
            ))
            assignment_id = cursor.fetchone()[0]
        else:
            cursor.execute('''
                INSERT OR REPLACE INTO cleaning_assignments (task_id, member_id, member_type, 
                    dia_semana, week_start, completado, notas)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                assignment.get('task_id'), assignment.get('member_id'),
                assignment.get('member_type'), assignment.get('dia_semana'),
                assignment.get('week_start'), assignment.get('completado', False),
                assignment.get('notas')
            ))
            assignment_id = cursor.lastrowid
        
        conn.commit()
        self._close_connection(conn)
        return assignment_id
    
    def get_weekly_cleaning_assignments(self, week_start: str) -> List[Dict]:
        """Get all cleaning assignments for a specific week"""
        conn = self.get_connection()
        
        if self.is_postgres:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute('''
                SELECT ca.*, ct.nombre as task_nombre, ct.area, ct.descripcion
                FROM cleaning_assignments ca
                JOIN cleaning_tasks ct ON ca.task_id = ct.id
                WHERE ca.week_start = %s
                ORDER BY ca.dia_semana, ct.area
            ''', (week_start,))
        else:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('''
                SELECT ca.*, ct.nombre as task_nombre, ct.area, ct.descripcion
                FROM cleaning_assignments ca
                JOIN cleaning_tasks ct ON ca.task_id = ct.id
                WHERE ca.week_start = ?
                ORDER BY ca.dia_semana, ct.area
            ''', (week_start,))
        
        rows = cursor.fetchall()
        self._close_connection(conn)
        return [dict(row) for row in rows]
    
    def update_assignment_completion(self, assignment_id: int, completado: bool, notas: str = None) -> bool:
        """Update assignment completion status"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if self.is_postgres:
            cursor.execute('''
                UPDATE cleaning_assignments 
                SET completado = %s, notas = %s
                WHERE id = %s
            ''', (completado, notas, assignment_id))
        else:
            cursor.execute('''
                UPDATE cleaning_assignments 
                SET completado = ?, notas = ?
                WHERE id = ?
            ''', (completado, notas, assignment_id))
        
        conn.commit()
        success = cursor.rowcount > 0
        self._close_connection(conn)
        return success
    
    def get_cleaning_preferences(self) -> Dict:
        """Get cleaning preferences"""
        conn = self.get_connection()
        
        if self.is_postgres:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute('SELECT * FROM cleaning_preferences ORDER BY id DESC LIMIT 1')
        else:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM cleaning_preferences ORDER BY id DESC LIMIT 1')
        
        row = cursor.fetchone()
        self._close_connection(conn)
        
        if row:
            prefs = dict(row)
            prefs['dias_trabajo'] = json.loads(prefs.get('dias_trabajo', '[]'))
            prefs['areas_preferidas'] = json.loads(prefs.get('areas_preferidas', '[]'))
            prefs['areas_evitar'] = json.loads(prefs.get('areas_evitar', '[]'))
            return prefs
        
        # Return default preferences if none exist
        return {
            'asignacion_automatica': True,
            'dias_trabajo': [],
            'areas_preferidas': [],
            'areas_evitar': [],
            'dificultad_maxima': 3
        }
    
    def save_cleaning_preferences(self, preferences: Dict) -> bool:
        """Save cleaning preferences"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if self.is_postgres:
            cursor.execute('''
                UPDATE cleaning_preferences 
                SET asignacion_automatica = %s, dias_trabajo = %s, 
                    areas_preferidas = %s, areas_evitar = %s, 
                    dificultad_maxima = %s, updated_at = CURRENT_TIMESTAMP
                WHERE id = (SELECT id FROM cleaning_preferences ORDER BY id DESC LIMIT 1)
            ''', (
                preferences.get('asignacion_automatica', True),
                json.dumps(preferences.get('dias_trabajo', [])),
                json.dumps(preferences.get('areas_preferidas', [])),
                json.dumps(preferences.get('areas_evitar', [])),
                preferences.get('dificultad_maxima', 3)
            ))
            
            if cursor.rowcount == 0:
                cursor.execute('''
                    INSERT INTO cleaning_preferences 
                    (asignacion_automatica, dias_trabajo, areas_preferidas, areas_evitar, dificultad_maxima)
                    VALUES (%s, %s, %s, %s, %s)
                ''', (
                    preferences.get('asignacion_automatica', True),
                    json.dumps(preferences.get('dias_trabajo', [])),
                    json.dumps(preferences.get('areas_preferidas', [])),
                    json.dumps(preferences.get('areas_evitar', [])),
                    preferences.get('dificultad_maxima', 3)
                ))
        else:
            cursor.execute('''
                UPDATE cleaning_preferences 
                SET asignacion_automatica = ?, dias_trabajo = ?, 
                    areas_preferidas = ?, areas_evitar = ?, 
                    dificultad_maxima = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = (SELECT id FROM cleaning_preferences ORDER BY id DESC LIMIT 1)
            ''', (
                preferences.get('asignacion_automatica', True),
                json.dumps(preferences.get('dias_trabajo', [])),
                json.dumps(preferences.get('areas_preferidas', [])),
                json.dumps(preferences.get('areas_evitar', [])),
                preferences.get('dificultad_maxima', 3)
            ))
            
            if cursor.rowcount == 0:
                cursor.execute('''
                    INSERT INTO cleaning_preferences 
                    (asignacion_automatica, dias_trabajo, areas_preferidas, areas_evitar, dificultad_maxima)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    preferences.get('asignacion_automatica', True),
                    json.dumps(preferences.get('dias_trabajo', [])),
                    json.dumps(preferences.get('areas_preferidas', [])),
                    json.dumps(preferences.get('areas_evitar', [])),
                    preferences.get('dificultad_maxima', 3)
                ))
        
        conn.commit()
        self._close_connection(conn)
        return True
