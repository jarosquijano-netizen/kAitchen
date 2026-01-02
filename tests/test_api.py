#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for Flask API endpoints
"""
import pytest
import json
import tempfile
import os
from app import app
from database import Database


@pytest.fixture
def client():
    """Create a test client"""
    # Create temporary database
    fd, path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    
    # Override database URL for testing
    app.config['TESTING'] = True
    app.config['DATABASE_URL'] = f'sqlite:///{path}'
    
    # Reinitialize database with test DB
    from app import db
    db.db_url = f'sqlite:///{path}'
    db.init_database()
    
    with app.test_client() as client:
        yield client
    
    # Cleanup
    if os.path.exists(path):
        os.unlink(path)


@pytest.fixture
def sample_adult():
    """Sample adult data for testing"""
    return {
        'nombre': 'Test Adult',
        'edad': 30,
        'objetivo_alimentario': 'Test objetivo',
        'estilo_alimentacion': 'Omnívoro',
        'cocinas_favoritas': 'Italiana',
        'nivel_picante': 'Medio',
        'ingredientes_favoritos': 'Pasta',
        'ingredientes_no_gustan': '',
        'alergias': '',
        'intolerancias': '',
        'restricciones_religiosas': '',
        'flexibilidad_comer': 'Alta',
        'preocupacion_principal': 'Salud',
        'tiempo_max_cocinar': 30,
        'nivel_cocina': 'Intermedio',
        'tipo_desayuno': 'Café',
        'le_gustan_snacks': True,
        'plato_favorito': 'Pasta',
        'plato_menos_favorito': '',
        'comentarios': ''
    }


@pytest.fixture
def sample_child():
    """Sample child data for testing"""
    return {
        'nombre': 'Test Child',
        'edad': 8,
        'come_solo': 'Solo',
        'nivel_exigencia': 'Medio',
        'cocinas_gustan': 'Italiana',
        'ingredientes_favoritos': 'Pasta',
        'ingredientes_rechaza': '',
        'texturas_no_gustan': '',
        'alergias': '',
        'intolerancias': '',
        'verduras_aceptadas': '',
        'verduras_rechazadas': '',
        'nivel_picante': 'Nada',
        'desayuno_preferido': 'Cereales',
        'snacks_favoritos': 'Fruta',
        'acepta_comida_nueva': 'A veces',
        'plato_favorito': 'Pasta',
        'plato_nunca_comeria': '',
        'comentarios_padres': ''
    }


class TestAdultsAPI:
    """Test adults API endpoints"""
    
    def test_get_adults_empty(self, client):
        """Test getting adults when none exist"""
        response = client.get('/api/adults')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert data['count'] == 0
        assert len(data['data']) == 0
    
    def test_add_adult(self, client, sample_adult):
        """Test adding an adult"""
        response = client.post('/api/adults',
                              data=json.dumps(sample_adult),
                              content_type='application/json')
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['success'] == True
        assert 'id' in data
    
    def test_get_adults_with_data(self, client, sample_adult):
        """Test getting adults after adding one"""
        # Add adult
        client.post('/api/adults',
                   data=json.dumps(sample_adult),
                   content_type='application/json')
        
        # Get adults
        response = client.get('/api/adults')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert data['count'] == 1
        assert len(data['data']) == 1
        assert data['data'][0]['nombre'] == 'Test Adult'
    
    def test_delete_adult(self, client, sample_adult):
        """Test deleting an adult"""
        # Add adult
        add_response = client.post('/api/adults',
                                  data=json.dumps(sample_adult),
                                  content_type='application/json')
        adult_id = json.loads(add_response.data)['id']
        
        # Delete adult
        response = client.delete(f'/api/adults/{adult_id}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        
        # Verify deleted
        get_response = client.get('/api/adults')
        assert json.loads(get_response.data)['count'] == 0


class TestChildrenAPI:
    """Test children API endpoints"""
    
    def test_get_children_empty(self, client):
        """Test getting children when none exist"""
        response = client.get('/api/children')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert data['count'] == 0
    
    def test_add_child(self, client, sample_child):
        """Test adding a child"""
        response = client.post('/api/children',
                              data=json.dumps(sample_child),
                              content_type='application/json')
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['success'] == True
        assert 'id' in data


class TestSettingsAPI:
    """Test settings API endpoints"""
    
    def test_get_settings(self, client):
        """Test getting settings"""
        response = client.get('/api/settings')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert 'data' in data
        assert 'has_api_key' in data['data']
        assert 'menu_preferences' in data['data']
    
    def test_get_family_summary(self, client, sample_adult, sample_child):
        """Test getting family summary"""
        # Add some profiles
        client.post('/api/adults',
                   data=json.dumps(sample_adult),
                   content_type='application/json')
        client.post('/api/children',
                   data=json.dumps(sample_child),
                   content_type='application/json')
        
        response = client.get('/api/family/summary')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert data['data']['total_members'] == 2
        assert len(data['data']['adults']) == 1
        assert len(data['data']['children']) == 1


class TestHealthCheck:
    """Test health check endpoint"""
    
    def test_health_endpoint(self, client):
        """Test health check"""
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'ok'
        assert 'timestamp' in data


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
