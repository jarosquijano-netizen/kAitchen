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
        
        # Initialize database tables
        self.init_database()
    
    def get_connection(self):
        """Get database connection"""
        if self.is_postgres:
            # PostgreSQL connection pool
            if not hasattr(self, '_pool'):
                self._pool = SimpleConnectionPool(1, 10, self.db_url)
            return self._pool.getconn()
        else:
            # SQLite connection
            db_path = self.db_url.replace('sqlite:///', '')
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row
            return conn
    
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
        
        conn.commit()
        conn.close()
    
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
        conn.close()
        return adult_id
    
    def get_all_adults(self) -> List[Dict]:
        """Get all adult profiles"""
        conn = self.get_connection()
        
        if self.is_postgres:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute('SELECT * FROM adults ORDER BY nombre')
        else:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM adults ORDER BY nombre')
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
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
        conn.close()
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
        conn.close()
        return child_id
    
    def get_all_children(self) -> List[Dict]:
        """Get all children profiles"""
        conn = self.get_connection()
        
        if self.is_postgres:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute('SELECT * FROM children ORDER BY nombre')
        else:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM children ORDER BY nombre')
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
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
        conn.close()
        return success
    
    # ==================== RECIPES ====================
    
    def add_recipe(self, recipe: Dict) -> int:
        """Add recipe"""
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
        conn.close()
        return recipe_id
    
    def get_all_recipes(self) -> List[Dict]:
        """Get all recipes"""
        conn = self.get_connection()
        
        if self.is_postgres:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute('SELECT * FROM recipes ORDER BY title')
        else:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM recipes ORDER BY title')
        
        rows = cursor.fetchall()
        conn.close()
        
        recipes = []
        for row in rows:
            recipe = dict(row)
            recipe['ingredients'] = json.loads(recipe.get('ingredients', '[]'))
            recipe['extracted_data'] = json.loads(recipe.get('extracted_data', '{}'))
            recipes.append(recipe)
        
        return recipes
    
    def delete_recipe(self, recipe_id: int) -> bool:
        """Delete recipe"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if self.is_postgres:
            cursor.execute('DELETE FROM recipes WHERE id = %s', (recipe_id,))
        else:
            cursor.execute('DELETE FROM recipes WHERE id = ?', (recipe_id,))
        
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        return success
    
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
        conn.close()
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
        conn.close()
        
        if row:
            menu = dict(row)
            menu['menu_data'] = json.loads(menu.get('menu_data', '{}'))
            menu['metadata'] = json.loads(menu.get('metadata', '{}'))
            return menu
        return None
    
    def get_menu_by_week_start(self, week_start_date: str) -> Optional[Dict]:
        """Get menu for specific week start date"""
        conn = self.get_connection()
        
        if self.is_postgres:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute('SELECT * FROM weekly_menus WHERE week_start_date = %s', (week_start_date,))
        else:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM weekly_menus WHERE week_start_date = ?', (week_start_date,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            menu = dict(row)
            menu['menu_data'] = json.loads(menu.get('menu_data', '{}'))
            menu['metadata'] = json.loads(menu.get('metadata', '{}'))
            return menu
        return None
    
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
        conn.close()
        
        menus = []
        for row in rows:
            menu = dict(row)
            menu['menu_data'] = json.loads(menu.get('menu_data', '{}'))
            menu['metadata'] = json.loads(menu.get('metadata', '{}'))
            menus.append(menu)
        
        return menus
    
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
        conn.close()
        
        if row:
            prefs = dict(row)
            excluded_days = prefs.get('excluded_days', '[]')
            if isinstance(excluded_days, str):
                prefs['excluded_days'] = json.loads(excluded_days)
            return prefs
        
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
        conn.close()
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
        conn.close()
        
        if row:
            recipe = dict(row)
            recipe['ingredients'] = json.loads(recipe.get('ingredients', '[]'))
            recipe['extracted_data'] = json.loads(recipe.get('extracted_data', '{}'))
            return recipe
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
        conn.close()
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
        conn.close()
        
        menus = []
        for row in rows:
            menu = dict(row)
            menu['menu_data'] = json.loads(menu.get('menu_data', '{}'))
            menus.append(menu)
        
        return menus
