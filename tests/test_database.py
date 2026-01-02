#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for database operations
"""
import pytest
import sqlite3
import os
import tempfile
from database import Database


@pytest.fixture
def temp_db():
    """Create a temporary database for testing"""
    fd, path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    db_url = f'sqlite:///{path}'
    db = Database(db_url=db_url)
    yield db, path
    # Cleanup
    if os.path.exists(path):
        os.unlink(path)


class TestDatabase:
    """Test database initialization and operations"""
    
    def test_database_initialization(self, temp_db):
        """Test that database initializes correctly"""
        db, path = temp_db
        assert db is not None
        assert os.path.exists(path)
        assert db.db_url == f'sqlite:///{path}'
        assert db.is_postgres == False
    
    def test_tables_created(self, temp_db):
        """Test that all required tables are created"""
        db, path = temp_db
        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        required_tables = ['adults', 'children', 'recipes', 'weekly_menus', 'menu_preferences']
        for table in required_tables:
            assert table in tables, f"Table {table} not found"
        
        conn.close()
    
    def test_add_adult(self, temp_db):
        """Test adding an adult profile"""
        db, path = temp_db
        adult_data = {
            'nombre': 'Test Adult',
            'edad': 30,
            'objetivo_alimentario': 'Test objetivo',
            'estilo_alimentacion': 'Omnívoro',
            'cocinas_favoritas': 'Italiana',
            'nivel_picante': 'Medio',
            'ingredientes_favoritos': 'Pasta, tomate',
            'ingredientes_no_gustan': 'Nada',
            'alergias': '',
            'intolerancias': '',
            'restricciones_religiosas': '',
            'flexibilidad_comer': 'Alta',
            'preocupacion_principal': 'Salud',
            'tiempo_max_cocinar': 30,
            'nivel_cocina': 'Intermedio',
            'tipo_desayuno': 'Café y tostadas',
            'le_gustan_snacks': True,
            'plato_favorito': 'Pasta',
            'plato_menos_favorito': 'Nada',
            'comentarios': 'Test comment'
        }
        
        adult_id = db.add_adult(adult_data)
        assert adult_id is not None
        assert adult_id > 0
        
        adults = db.get_all_adults()
        assert len(adults) == 1
        assert adults[0]['nombre'] == 'Test Adult'
        assert adults[0]['edad'] == 30
    
    def test_add_child(self, temp_db):
        """Test adding a child profile"""
        db, path = temp_db
        child_data = {
            'nombre': 'Test Child',
            'edad': 8,
            'come_solo': 'Solo',
            'nivel_exigencia': 'Medio',
            'cocinas_gustan': 'Italiana',
            'ingredientes_favoritos': 'Pasta',
            'ingredientes_rechaza': 'Verduras',
            'texturas_no_gustan': 'Fibrosas',
            'alergias': '',
            'intolerancias': '',
            'verduras_aceptadas': 'Zanahoria',
            'verduras_rechazadas': 'Brócoli',
            'nivel_picante': 'Nada',
            'desayuno_preferido': 'Cereales',
            'snacks_favoritos': 'Fruta',
            'acepta_comida_nueva': 'A veces',
            'plato_favorito': 'Pasta',
            'plato_nunca_comeria': 'Brócoli',
            'comentarios_padres': 'Test comment'
        }
        
        child_id = db.add_child(child_data)
        assert child_id is not None
        assert child_id > 0
        
        children = db.get_all_children()
        assert len(children) == 1
        assert children[0]['nombre'] == 'Test Child'
        assert children[0]['edad'] == 8
    
    def test_delete_adult(self, temp_db):
        """Test deleting an adult profile"""
        db, path = temp_db
        adult_data = {
            'nombre': 'Test Adult',
            'edad': 30,
            'objetivo_alimentario': 'Test',
            'estilo_alimentacion': 'Omnívoro'
        }
        
        adult_id = db.add_adult(adult_data)
        assert len(db.get_all_adults()) == 1
        
        success = db.delete_adult(adult_id)
        assert success == True
        assert len(db.get_all_adults()) == 0
    
    def test_get_menu_preferences(self, temp_db):
        """Test getting menu preferences"""
        db, path = temp_db
        prefs = db.get_menu_preferences()
        
        assert 'include_weekend' in prefs
        assert 'include_breakfast' in prefs
        assert 'include_lunch' in prefs
        assert 'include_dinner' in prefs
        assert 'excluded_days' in prefs
        assert isinstance(prefs['excluded_days'], list)
    
    def test_save_menu_preferences(self, temp_db):
        """Test saving menu preferences"""
        db, path = temp_db
        prefs = {
            'include_weekend': False,
            'include_breakfast': True,
            'include_lunch': True,
            'include_dinner': False,
            'excluded_days': ['Monday', 'Tuesday']
        }
        
        success = db.save_menu_preferences(prefs)
        assert success == True
        
        saved_prefs = db.get_menu_preferences()
        assert saved_prefs['include_weekend'] == False
        assert saved_prefs['include_dinner'] == False
        assert 'Monday' in saved_prefs['excluded_days']


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
