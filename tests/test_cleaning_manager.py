#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for Cleaning Manager Module
"""

import unittest
import json
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cleaning_manager import CleaningManager


class TestCleaningManager(unittest.TestCase):
    """Test cases for CleaningManager class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_db = Mock()
        self.cleaning_manager = CleaningManager(self.mock_db)
    
    def test_get_week_start_current_date(self):
        """Test getting week start for current date"""
        # Test with a known date (Wednesday, 2024-01-10)
        with patch('cleaning_manager.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 10)  # Wednesday
            mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)
            
            result = self.cleaning_manager.get_week_start()
            expected = "2024-01-08"  # Monday of that week
            
            self.assertEqual(result, expected)
    
    def test_get_week_start_specific_date(self):
        """Test getting week start for a specific date"""
        result = self.cleaning_manager.get_week_start("2024-01-15")  # Monday
        expected = "2024-01-15"
        
        self.assertEqual(result, expected)
    
    def test_get_week_start_weekend_date(self):
        """Test getting week start for a weekend date"""
        result = self.cleaning_manager.get_week_start("2024-01-14")  # Sunday
        expected = "2024-01-08"  # Monday of that week
        
        self.assertEqual(result, expected)
    
    def test_get_family_members_adults_only(self):
        """Test getting family members with only adults"""
        mock_adults = [
            {'id': 1, 'nombre': 'Juan', 'edad': 35},
            {'id': 2, 'nombre': 'María', 'edad': 32}
        ]
        mock_children = [
            {'id': 3, 'nombre': 'Ana', 'edad': 8},  # Too young for cleaning
            {'id': 4, 'nombre': 'Carlos', 'edad': 10}  # Too young for cleaning
        ]
        
        self.mock_db.get_all_adults.return_value = mock_adults
        self.mock_db.get_all_children.return_value = mock_children
        
        result = self.cleaning_manager.get_family_members()
        
        expected = [
            {'id': 1, 'nombre': 'Juan', 'tipo': 'adulto', 'edad': 35},
            {'id': 2, 'nombre': 'María', 'tipo': 'adulto', 'edad': 32}
        ]
        
        self.assertEqual(result, expected)
        self.mock_db.get_all_adults.assert_called_once()
        self.mock_db.get_all_children.assert_called_once()
    
    def test_get_family_members_with_teens(self):
        """Test getting family members including teens (12+)"""
        mock_adults = [
            {'id': 1, 'nombre': 'Juan', 'edad': 35}
        ]
        mock_children = [
            {'id': 3, 'nombre': 'Ana', 'edad': 8},   # Too young
            {'id': 4, 'nombre': 'Carlos', 'edad': 12}, # Can clean
            {'id': 5, 'nombre': 'Laura', 'edad': 15}   # Can clean
        ]
        
        self.mock_db.get_all_adults.return_value = mock_adults
        self.mock_db.get_all_children.return_value = mock_children
        
        result = self.cleaning_manager.get_family_members()
        
        expected = [
            {'id': 1, 'nombre': 'Juan', 'tipo': 'adulto', 'edad': 35},
            {'id': 4, 'nombre': 'Carlos', 'tipo': 'niño', 'edad': 12},
            {'id': 5, 'nombre': 'Laura', 'tipo': 'niño', 'edad': 15}
        ]
        
        self.assertEqual(result, expected)
    
    def test_calculate_task_load(self):
        """Test calculating task load for family members"""
        assignments = [
            {
                'persona_id': 1,
                'dificultad': 3,
                'tiempo_estimado': 30
            },
            {
                'persona_id': 1,
                'dificultad': 2,
                'tiempo_estimado': 20
            },
            {
                'persona_id': 2,
                'dificultad': 4,
                'tiempo_estimado': 45
            }
        ]
        
        result = self.cleaning_manager.calculate_task_load(assignments)
        
        expected = {
            1: {
                'total_dificultad': 5,
                'total_tiempo': 50,
                'num_tasks': 2
            },
            2: {
                'total_dificultad': 4,
                'total_tiempo': 45,
                'num_tasks': 1
            }
        }
        
        self.assertEqual(result, expected)
    
    def test_initialize_default_tasks(self):
        """Test initializing default cleaning tasks"""
        # Mock empty existing tasks
        self.mock_db.get_all_cleaning_tasks.return_value = []
        self.mock_db.add_cleaning_task.return_value = 1
        
        result = self.cleaning_manager.initialize_default_tasks()
        
        self.assertTrue(result)
        # Should add all default tasks (10 in our implementation)
        self.assertEqual(self.mock_db.add_cleaning_task.call_count, 10)
    
    def test_initialize_default_tasks_existing(self):
        """Test initializing when tasks already exist"""
        # Mock existing tasks
        existing_tasks = [
            {'id': 1, 'nombre': 'Limpiar cocina'},
            {'id': 2, 'nombre': 'Limpiar baño'}
        ]
        self.mock_db.get_all_cleaning_tasks.return_value = existing_tasks
        
        result = self.cleaning_manager.initialize_default_tasks()
        
        self.assertTrue(result)
        # Should not add any new tasks
        self.mock_db.add_cleaning_task.assert_not_called()
    
    def test_assign_tasks_for_week_no_tasks(self):
        """Test assigning tasks when no tasks exist"""
        self.mock_db.get_all_cleaning_tasks.return_value = []
        
        result = self.cleaning_manager.assign_tasks_for_week("2024-01-08")
        
        self.assertFalse(result['success'])
        self.assertIn('No hay tareas de limpieza configuradas', result['error'])
    
    def test_assign_tasks_for_week_no_members(self):
        """Test assigning tasks when no family members available"""
        mock_tasks = [
            {'id': 1, 'nombre': 'Limpiar cocina', 'area': 'Cocina', 'dificultad': 3}
        ]
        
        self.mock_db.get_all_cleaning_tasks.return_value = mock_tasks
        self.mock_db.get_all_adults.return_value = []
        self.mock_db.get_all_children.return_value = []
        
        result = self.cleaning_manager.assign_tasks_for_week("2024-01-08")
        
        self.assertFalse(result['success'])
        self.assertIn('No hay miembros de la familia', result['error'])
    
    def test_assign_tasks_for_week_success(self):
        """Test successful task assignment"""
        mock_tasks = [
            {
                'id': 1,
                'nombre': 'Limpiar cocina',
                'area': 'Cocina',
                'dificultad': 3,
                'tiempo_estimado': 30,
                'dias_semana': ['martes', 'sábado']
            }
        ]
        
        mock_members = [
            {'id': 1, 'nombre': 'Juan', 'tipo': 'adulto', 'edad': 35},
            {'id': 2, 'nombre': 'María', 'tipo': 'adulto', 'edad': 32}
        ]
        
        mock_preferences = {
            'asignacion_automatica': True,
            'dias_limpieza': ['martes', 'sábado'],
            'balancear_cargas': True
        }
        
        self.mock_db.get_all_cleaning_tasks.return_value = mock_tasks
        self.mock_db.get_all_adults.return_value = mock_members[:1]
        self.mock_db.get_all_children.return_value = []
        self.mock_db.get_cleaning_preferences.return_value = mock_preferences
        self.mock_db.save_cleaning_assignment.return_value = 1
        
        result = self.cleaning_manager.assign_tasks_for_week("2024-01-08")
        
        self.assertTrue(result['success'])
        self.assertEqual(result['week_start'], "2024-01-08")
        self.assertGreater(result['total_assignments'], 0)
    
    def test_update_task_completion_success(self):
        """Test successful task completion update"""
        self.mock_db.update_assignment_completion.return_value = True
        
        result = self.cleaning_manager.update_task_completion(1, True, "Completado sin problemas")
        
        self.assertTrue(result['success'])
        self.assertIn('Tarea actualizada correctamente', result['message'])
        self.mock_db.update_assignment_completion.assert_called_once_with(1, True, "Completado sin problemas")
    
    def test_update_task_completion_failure(self):
        """Test failed task completion update"""
        self.mock_db.update_assignment_completion.return_value = False
        
        result = self.cleaning_manager.update_task_completion(1, True)
        
        self.assertFalse(result['success'])
        self.assertIn('No se pudo actualizar la tarea', result['message'])
    
    def test_get_weekly_schedule_success(self):
        """Test getting weekly schedule successfully"""
        mock_assignments = [
            {
                'id': 1,
                'dia_semana': 'martes',
                'persona_id': 1,
                'persona_nombre': 'Juan',
                'tipo_persona': 'adulto',
                'task_nombre': 'Limpiar cocina',
                'area': 'Cocina',
                'dificultad': 3,
                'tiempo_estimado': 30,
                'completado': False
            }
        ]
        
        self.mock_db.get_weekly_cleaning_assignments.return_value = mock_assignments
        
        result = self.cleaning_manager.get_weekly_schedule("2024-01-08")
        
        self.assertTrue(result['success'])
        self.assertEqual(result['week_start'], "2024-01-08")
        self.assertEqual(result['total_assignments'], 1)
        self.assertIn('martes', result['schedule'])
        self.assertEqual(len(result['schedule']['martes']), 1)
        self.assertIn('member_stats', result)
    
    def test_get_cleaning_statistics_no_data(self):
        """Test getting statistics with no data"""
        self.mock_db.get_weekly_cleaning_assignments.return_value = []
        
        result = self.cleaning_manager.get_cleaning_statistics(4)
        
        self.assertTrue(result['success'])
        stats = result['stats']
        self.assertEqual(stats['total_tasks'], 0)
        self.assertEqual(stats['completed_tasks'], 0)
        self.assertEqual(stats['completion_rate'], 0)
        self.assertEqual(stats['member_performance'], {})
        self.assertEqual(stats['area_performance'], {})
    
    def test_get_cleaning_statistics_with_data(self):
        """Test getting statistics with actual data"""
        mock_assignments = [
            {
                'persona_id': 1,
                'persona_nombre': 'Juan',
                'area': 'Cocina',
                'completado': True
            },
            {
                'persona_id': 1,
                'persona_nombre': 'Juan',
                'area': 'Baño',
                'completado': False
            },
            {
                'persona_id': 2,
                'persona_nombre': 'María',
                'area': 'Cocina',
                'completado': True
            }
        ]
        
        self.mock_db.get_weekly_cleaning_assignments.return_value = mock_assignments
        
        result = self.cleaning_manager.get_cleaning_statistics(1)
        
        self.assertTrue(result['success'])
        stats = result['stats']
        self.assertEqual(stats['total_tasks'], 3)
        self.assertEqual(stats['completed_tasks'], 2)
        self.assertEqual(stats['completion_rate'], 66.66666666666666)
        self.assertIn('member_performance', stats)
        self.assertIn('area_performance', stats)
    
    def test_find_best_member_by_rotation(self):
        """Test finding best member using rotation algorithm"""
        members = [
            {'id': 1, 'nombre': 'Juan'},
            {'id': 2, 'nombre': 'María'}
        ]
        
        task = {'area': 'Cocina'}
        member_rotation = {'Cocina': 1}  # Juan was last assigned to kitchen
        
        result = self.cleaning_manager._find_best_member_by_rotation(task, members, member_rotation)
        
        # Should return María (not the one who was last assigned to kitchen)
        self.assertEqual(result['id'], 2)
        self.assertEqual(result['nombre'], 'María')
    
    def test_find_best_member_by_load(self):
        """Test finding best member using load balancing"""
        existing_assignments = [
            {'persona_id': 1, 'dificultad': 5, 'tiempo_estimado': 60},  # Heavy load
            {'persona_id': 2, 'dificultad': 1, 'tiempo_estimado': 15}   # Light load
        ]
        
        members = [
            {'id': 1, 'nombre': 'Juan'},
            {'id': 2, 'nombre': 'María'}
        ]
        
        task = {'area': 'Cocina', 'dificultad': 3}
        member_rotation = {}
        
        result = self.cleaning_manager._find_best_member_by_load(
            task, members, existing_assignments, member_rotation
        )
        
        # Should return María (lighter current load)
        self.assertEqual(result['id'], 2)
        self.assertEqual(result['nombre'], 'María')


class TestCleaningManagerIntegration(unittest.TestCase):
    """Integration tests for CleaningManager"""
    
    def setUp(self):
        """Set up integration test fixtures"""
        # These tests would require a real database connection
        # For now, we'll use comprehensive mocks
        pass
    
    def test_full_workflow_initialization_to_assignment(self):
        """Test complete workflow from initialization to assignment"""
        # This would be a comprehensive integration test
        # that tests the entire flow with mocked database calls
        pass


if __name__ == '__main__':
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_suite.addTest(unittest.makeSuite(TestCleaningManager))
    test_suite.addTest(unittest.makeSuite(TestCleaningManagerIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print(f"\n{'='*50}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    print(f"{'='*50}")
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)
