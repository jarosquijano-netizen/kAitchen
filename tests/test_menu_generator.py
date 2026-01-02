#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for menu generator (requires API key)
"""
import pytest
import os
from menu_generator import MenuGenerator


@pytest.fixture
def api_key():
    """Get API key from environment"""
    key = os.getenv('ANTHROPIC_API_KEY', '')
    if not key or key.startswith('sk-ant-api03-your-key'):
        pytest.skip("ANTHROPIC_API_KEY not configured")
    return key


@pytest.fixture
def menu_gen(api_key):
    """Create menu generator instance"""
    return MenuGenerator(api_key)


@pytest.fixture
def sample_family():
    """Sample family data for testing"""
    return {
        'adults': [
            {
                'nombre': 'Test Adult',
                'edad': 30,
                'objetivo_alimentario': 'Salud general',
                'estilo_alimentacion': 'Omnívoro',
                'cocinas_favoritas': 'Italiana',
                'alergias': '',
                'intolerancias': ''
            }
        ],
        'children': [
            {
                'nombre': 'Test Child',
                'edad': 8,
                'nivel_exigencia': 'Medio',
                'ingredientes_favoritos': 'Pasta',
                'alergias': ''
            }
        ],
        'recipes': []
    }


class TestMenuGenerator:
    """Test menu generator functionality"""
    
    def test_menu_generator_initialization(self, api_key):
        """Test menu generator can be initialized"""
        gen = MenuGenerator(api_key)
        assert gen is not None
        assert gen.api_key == api_key
    
    def test_generate_weekly_menu_structure(self, menu_gen, sample_family):
        """Test that menu generation returns correct structure"""
        result = menu_gen.generate_weekly_menu(
            adults=sample_family['adults'],
            children=sample_family['children'],
            recipes=sample_family['recipes']
        )
        
        assert 'success' in result
        if result['success']:
            assert 'menu' in result
            assert 'generated_at' in result
            # Menu structure can vary, just check it's a dict with content
            menu = result['menu']
            assert isinstance(menu, dict)
            assert len(menu) > 0, "Menu should not be empty"
        else:
            # If generation failed, check error message exists
            assert 'error' in result


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
