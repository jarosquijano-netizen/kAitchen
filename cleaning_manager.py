#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cleaning Manager Module for Family Command Center
Handles automatic rotation and assignment of cleaning tasks
"""

import json
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from database import Database


class CleaningManager:
    """Manages cleaning tasks and automatic rotation for family members"""
    
    def __init__(self, db: Database):
        self.db = db
        self.dias_semana = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
    
    def get_week_start(self, date_str: Optional[str] = None) -> str:
        """
        Get Monday of the week for a given date or current week
        Returns: YYYY-MM-DD string
        """
        if date_str:
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d')
            except ValueError:
                date = datetime.now()
        else:
            date = datetime.now()
        
        # Get Monday of the week
        days_since_monday = date.weekday()
        monday = date - timedelta(days=days_since_monday)
        return monday.strftime('%Y-%m-%d')
    
    def initialize_default_tasks(self) -> bool:
        """
        Initialize default cleaning tasks for a family home
        Returns: True if successful
        """
        default_tasks = [
            {
                'nombre': 'Limpiar cocina',
                'descripcion': 'Limpiar encimeras, fregadero y suelos de la cocina',
                'area': 'Cocina',
                'dificultad': 3,
                'frecuencia': 'diaria',
                'tiempo_estimado': 30,
                'dias_semana': ['martes', 'sábado']
            },
            {
                'nombre': 'Limpiar baño principal',
                'descripcion': 'Limpiar inodoro, lavabo, ducha y suelo del baño principal',
                'area': 'Baño',
                'dificultad': 4,
                'frecuencia': 'semanal',
                'tiempo_estimado': 45,
                'dias_semana': ['sábado']
            },
            {
                'nombre': 'Limpiar baño de arriba',
                'descripcion': 'Limpiar inodoro, lavabo y suelo del baño de arriba',
                'area': 'Baño',
                'dificultad': 3,
                'frecuencia': 'semanal',
                'tiempo_estimado': 30,
                'dias_semana': ['martes']
            },
            {
                'nombre': 'Aspirar y trapear suelo',
                'descripcion': 'Aspirar y trapear los suelos de toda la casa',
                'area': 'General',
                'dificultad': 4,
                'frecuencia': 'semanal',
                'tiempo_estimado': 60,
                'dias_semana': ['sábado']
            },
            {
                'nombre': 'Quitar polvo superficies',
                'descripcion': 'Quitar polvo de muebles, estanterías y superficies',
                'area': 'General',
                'dificultad': 2,
                'frecuencia': 'semanal',
                'tiempo_estimado': 30,
                'dias_semana': ['martes']
            },
            {
                'nombre': 'Limpiar salón',
                'descripcion': 'Ordenar y limpiar el salón/comedor',
                'area': 'Salón',
                'dificultad': 2,
                'frecuencia': 'diaria',
                'tiempo_estimado': 20,
                'dias_semana': ['martes', 'sábado']
            },
            {
                'nombre': 'Recoger habitaciones',
                'descripcion': 'Recoger y ordenar las habitaciones',
                'area': 'Habitaciones',
                'dificultad': 2,
                'frecuencia': 'diaria',
                'tiempo_estimado': 15,
                'dias_semana': ['martes', 'sábado']
            },
            {
                'nombre': 'Limpiar ventanas',
                'descripcion': 'Limpiar ventanas interiores y exteriores',
                'area': 'General',
                'dificultad': 3,
                'frecuencia': 'quincenal',
                'tiempo_estimado': 90,
                'dias_semana': ['sábado']
            },
            {
                'nombre': 'Cambiar sábanas',
                'descripcion': 'Cambiar sábanas de todas las camas',
                'area': 'Habitaciones',
                'dificultad': 2,
                'frecuencia': 'semanal',
                'tiempo_estimado': 30,
                'dias_semana': ['sábado']
            },
            {
                'nombre': 'Organizar armarios',
                'descripcion': 'Organizar y limpiar armarios de la cocina y habitaciones',
                'area': 'Organización',
                'dificultad': 3,
                'frecuencia': 'mensual',
                'tiempo_estimado': 120,
                'dias_semana': ['sábado']
            }
        ]
        
        try:
            for task in default_tasks:
                # Check if task already exists
                existing_tasks = self.db.get_all_cleaning_tasks()
                if not any(t['nombre'] == task['nombre'] for t in existing_tasks):
                    self.db.add_cleaning_task(task)
                    print(f"[CleaningManager] Added default task: {task['nombre']}")
            return True
        except Exception as e:
            print(f"[CleaningManager] Error initializing default tasks: {e}")
            return False
    
    def get_family_members(self) -> List[Dict]:
        """
        Get all family members (adults and children) for task assignment
        Returns: List of family members with id, nombre, tipo
        """
        members = []
        
        # Get adults
        adults = self.db.get_all_adults()
        for adult in adults:
            members.append({
                'id': adult['id'],
                'nombre': adult['nombre'],
                'tipo': 'adulto',
                'edad': adult.get('edad', 0)
            })
        
        # Get children (only assign to children 12+ years old)
        children = self.db.get_all_children()
        for child in children:
            if child.get('edad', 0) >= 12:  # Only children 12+ can do cleaning tasks
                members.append({
                    'id': child['id'],
                    'nombre': child['nombre'],
                    'tipo': 'niño',
                    'edad': child.get('edad', 0)
                })
        
        return members
    
    def calculate_task_load(self, assignments: List[Dict]) -> Dict:
        """
        Calculate current task load for each family member
        Returns: Dict with member_id as key and total_dificultad, total_tiempo as values
        """
        load = {}
        
        for assignment in assignments:
            member_id = assignment['member_id']
            if member_id not in load:
                load[member_id] = {
                    'total_dificultad': 0,
                    'total_tiempo': 0,
                    'num_tasks': 0
                }
            
            load[member_id]['total_dificultad'] += assignment.get('dificultad', 1)
            load[member_id]['total_tiempo'] += assignment.get('tiempo_estimado', 30)
            load[member_id]['num_tasks'] += 1
        
        return load
    
    def assign_tasks_for_week(self, week_start: Optional[str] = None) -> Dict:
        """
        Automatically assign cleaning tasks for a week using rotation algorithm
        Returns: Dict with success status and assignments
        """
        try:
            week_start = week_start or self.get_week_start()
            preferences = self.db.get_cleaning_preferences()
            
            if not preferences.get('asignacion_automatica', True):
                return {
                    'success': False,
                    'error': 'Asignación automática desactivada en preferencias'
                }
            
            # Get tasks and family members
            tasks = self.db.get_all_cleaning_tasks()
            members = self.get_family_members()
            
            if not tasks:
                return {
                    'success': False,
                    'error': 'No hay tareas de limpieza configuradas'
                }
            
            if not members:
                return {
                    'success': False,
                    'error': 'No hay miembros de la familia disponibles para asignar tareas'
                }
            
            # Get cleaning days from preferences
            cleaning_days = preferences.get('dias_trabajo', ['martes', 'sábado'])
            
            # Clear existing assignments for this week
            self._clear_week_assignments(week_start)
            
            # Assign tasks day by day
            all_assignments = []
            member_rotation = {}  # Track which member was last assigned for each area
            
            for day in cleaning_days:
                if day not in self.dias_semana:
                    continue
                
                # Filter tasks for this day
                day_tasks = [task for task in tasks 
                            if not task.get('dias_semana') or day in task.get('dias_semana', [])]
                
                # Sort tasks by difficulty (hardest first) for fair distribution
                day_tasks.sort(key=lambda x: x.get('dificultad', 1), reverse=True)
                
                for task in day_tasks:
                    # Find best member for this task
                    best_member = self._find_best_member_for_task(
                        task, members, all_assignments, member_rotation, preferences
                    )
                    
                    if best_member:
                        assignment = {
                            'task_id': task['id'],
                            'member_id': best_member['id'],
                            'member_type': best_member['tipo'],
                            'week_start': week_start,
                            'dia_semana': day,
                            'completado': False,
                            'notas': f'Asignado automáticamente a {best_member["nombre"]}'
                        }
                        
                        # Save assignment
                        assignment_id = self.db.save_cleaning_assignment(assignment)
                        assignment['id'] = assignment_id
                        assignment['task_nombre'] = task['nombre']
                        assignment['area'] = task['area']
                        assignment['dificultad'] = task['dificultad']
                        assignment['tiempo_estimado'] = task['tiempo_estimado']
                        assignment['member_name'] = best_member['nombre']
                        
                        all_assignments.append(assignment)
                        
                        # Update rotation tracking
                        area = task['area']
                        member_rotation[area] = best_member['id']
                        
                        print(f"[CleaningManager] Assigned '{task['nombre']}' to {best_member['nombre']} on {day}")
            
            return {
                'success': True,
                'week_start': week_start,
                'assignments': all_assignments,
                'total_assignments': len(all_assignments),
                'preferences': preferences
            }
            
        except Exception as e:
            print(f"[CleaningManager] Error assigning tasks: {e}")
            return {
                'success': False,
                'error': f'Error al asignar tareas: {str(e)}'
            }
    
    def _find_best_member_for_task(self, task: Dict, members: List[Dict], 
                                 existing_assignments: List[Dict], 
                                 member_rotation: Dict, 
                                 preferences: Dict) -> Optional[Dict]:
        """
        Find the best member for a specific task using rotation algorithm
        Returns: Best member dict or None
        """
        if preferences.get('balancear_cargas', True):
            return self._find_best_member_by_load(task, members, existing_assignments, member_rotation)
        else:
            return self._find_best_member_by_rotation(task, members, member_rotation)
    
    def _find_best_member_by_rotation(self, task: Dict, members: List[Dict], 
                                    member_rotation: Dict) -> Optional[Dict]:
        """
        Find best member using simple rotation (avoid same person getting same area)
        """
        area = task['area']
        last_assigned_id = member_rotation.get(area)
        
        # Filter out the member who was last assigned to this area
        available_members = [m for m in members if m['id'] != last_assigned_id]
        
        if not available_members:
            # If all members were assigned to this area, use all members
            available_members = members
        
        # Return the first available member (simple rotation)
        return available_members[0] if available_members else members[0]
    
    def _find_best_member_by_load(self, task: Dict, members: List[Dict], 
                                existing_assignments: List[Dict], 
                                member_rotation: Dict) -> Optional[Dict]:
        """
        Find best member by balancing current load and rotation
        """
        # Calculate current load
        current_load = self.calculate_task_load(existing_assignments)
        
        # Sort members by current load (lightest first)
        members_by_load = sorted(members, 
                               key=lambda m: current_load.get(m['id'], {}).get('total_dificultad', 0))
        
        # Try to assign to member with lightest load, but consider rotation
        area = task['area']
        last_assigned_id = member_rotation.get(area)
        
        for member in members_by_load:
            # Prefer not to assign same area to same person consecutively
            if member['id'] != last_assigned_id:
                return member
        
        # If rotation constraint makes it impossible, use lightest load anyway
        return members_by_load[0] if members_by_load else None
    
    def _clear_week_assignments(self, week_start: str):
        """Clear all assignments for a specific week"""
        # This would require a new method in database.py to delete assignments by week
        # For now, we'll rely on the ON CONFLICT clause to replace existing assignments
        pass
    
    def get_weekly_schedule(self, week_start: Optional[str] = None) -> Dict:
        """
        Get the complete cleaning schedule for a week
        Returns: Dict with assignments organized by day and member
        """
        try:
            week_start = week_start or self.get_week_start()
            assignments = self.db.get_weekly_cleaning_assignments(week_start)
            
            # Organize by day
            schedule = {day: [] for day in self.dias_semana}
            member_stats = {}
            
            for assignment in assignments:
                day = assignment['dia_semana']
                if day in schedule:
                    schedule[day].append(assignment)
                
                # Calculate member stats
                member_id = assignment['member_id']
                member_name = assignment.get('member_name', f'Miembro {member_id}')
                
                if member_id not in member_stats:
                    member_stats[member_id] = {
                        'nombre': member_name,
                        'tipo': assignment['member_type'],
                        'total_dificultad': 0,
                        'total_tiempo': 0,
                        'num_tasks': 0,
                        'completed_tasks': 0
                    }
                
                member_stats[member_id]['total_dificultad'] += assignment.get('dificultad', 1)
                member_stats[member_id]['total_tiempo'] += assignment.get('tiempo_estimado', 30)
                member_stats[member_id]['num_tasks'] += 1
                
                if assignment.get('completado', False):
                    member_stats[member_id]['completed_tasks'] += 1
            
            return {
                'success': True,
                'week_start': week_start,
                'schedule': schedule,
                'member_stats': member_stats,
                'total_assignments': len(assignments),
                'completion_rate': sum(m['completed_tasks'] for m in member_stats.values()) / max(len(assignments), 1) * 100
            }
            
        except Exception as e:
            print(f"[CleaningManager] Error getting weekly schedule: {e}")
            return {
                'success': False,
                'error': f'Error al obtener horario semanal: {str(e)}'
            }
    
    def update_task_completion(self, assignment_id: int, completado: bool, notas: str = None) -> Dict:
        """
        Update task completion status
        Returns: Dict with success status
        """
        try:
            success = self.db.update_assignment_completion(assignment_id, completado, notas)
            
            return {
                'success': success,
                'message': 'Tarea actualizada correctamente' if success else 'No se pudo actualizar la tarea'
            }
            
        except Exception as e:
            print(f"[CleaningManager] Error updating task completion: {e}")
            return {
                'success': False,
                'error': f'Error al actualizar tarea: {str(e)}'
            }
    
    def get_cleaning_statistics(self, weeks: int = 4) -> Dict:
        """
        Get cleaning statistics for the last N weeks
        Returns: Dict with various statistics
        """
        try:
            # Get assignments for the last N weeks
            all_assignments = []
            current_week = datetime.now()
            
            for i in range(weeks):
                week_start = self.get_week_start((current_week - timedelta(weeks=i)).strftime('%Y-%m-%d'))
                week_assignments = self.db.get_weekly_cleaning_assignments(week_start)
                all_assignments.extend(week_assignments)
            
            if not all_assignments:
                return {
                    'success': True,
                    'stats': {
                        'total_tasks': 0,
                        'completed_tasks': 0,
                        'completion_rate': 0,
                        'member_performance': {},
                        'area_performance': {}
                    }
                }
            
            # Calculate statistics
            total_tasks = len(all_assignments)
            completed_tasks = sum(1 for a in all_assignments if a.get('completado', False))
            completion_rate = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
            
            # Member performance
            member_performance = {}
            for assignment in all_assignments:
                member_id = assignment['member_id']
                member_name = assignment.get('member_name', f'Miembro {member_id}')
                
                if member_id not in member_performance:
                    member_performance[member_id] = {
                        'nombre': member_name,
                        'total_tasks': 0,
                        'completed_tasks': 0,
                        'completion_rate': 0
                    }
                
                member_performance[member_id]['total_tasks'] += 1
                if assignment.get('completado', False):
                    member_performance[member_id]['completed_tasks'] += 1
                
                member_performance[member_id]['completion_rate'] = (
                    member_performance[member_id]['completed_tasks'] / 
                    member_performance[member_id]['total_tasks'] * 100
                )
            
            # Area performance
            area_performance = {}
            for assignment in all_assignments:
                area = assignment.get('area', 'Unknown')
                
                if area not in area_performance:
                    area_performance[area] = {
                        'total_tasks': 0,
                        'completed_tasks': 0,
                        'completion_rate': 0
                    }
                
                area_performance[area]['total_tasks'] += 1
                if assignment.get('completado', False):
                    area_performance[area]['completed_tasks'] += 1
                
                area_performance[area]['completion_rate'] = (
                    area_performance[area]['completed_tasks'] / 
                    area_performance[area]['total_tasks'] * 100
                )
            
            return {
                'success': True,
                'stats': {
                    'total_tasks': total_tasks,
                    'completed_tasks': completed_tasks,
                    'completion_rate': completion_rate,
                    'member_performance': member_performance,
                    'area_performance': area_performance,
                    'weeks_analyzed': weeks
                }
            }
            
        except Exception as e:
            print(f"[CleaningManager] Error getting statistics: {e}")
            return {
                'success': False,
                'error': f'Error al obtener estadísticas: {str(e)}'
            }
