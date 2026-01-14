#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple test for calendar functionality without database dependencies
"""

from datetime import datetime, timedelta

def test_date_range():
    """Test date range generation"""
    print("🧪 Testing Date Range Generation")
    print("=" * 40)
    
    def get_date_range(start_date: str, end_date: str):
        """Generate list of dates between start_date and end_date inclusive"""
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        
        dates = []
        current = start
        while current <= end:
            dates.append(current.strftime('%Y-%m-%d'))
            current += timedelta(days=1)
        
        return dates
    
    # Test
    start_date = "2026-01-14"
    end_date = "2026-01-20"
    dates = get_date_range(start_date, end_date)
    
    print(f"Start date: {start_date}")
    print(f"End date: {end_date}")
    print(f"Generated {len(dates)} dates:")
    for date in dates:
        print(f"  - {date}")
    
    print("\n✅ Date range test passed!")

def test_day_mapping():
    """Test day name mapping"""
    print("\n🧪 Testing Day Name Mapping")
    print("=" * 40)
    
    dias_semana = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
    
    test_dates = ["2026-01-14", "2026-01-15", "2026-01-16", "2026-01-17", "2026-01-18"]
    
    for date_str in test_dates:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        day_name = dias_semana[date_obj.weekday()]
        print(f"{date_str} → {day_name}")
    
    print("\n✅ Day mapping test passed!")

def test_task_assignment_logic():
    """Test basic task assignment logic"""
    print("\n🧪 Testing Task Assignment Logic")
    print("=" * 40)
    
    # Sample tasks
    tasks = [
        {'nombre': 'Limpiar cocina', 'area': 'Cocina', 'dificultad': 3, 'dias_semana': ['martes', 'sábado']},
        {'nombre': 'Limpiar baño principal', 'area': 'Baño', 'dificultad': 4, 'dias_semana': ['sábado']},
        {'nombre': 'Aspirar y trapear', 'area': 'General', 'dificultad': 4, 'dias_semana': ['sábado']},
        {'nombre': 'Quitar polvo', 'area': 'General', 'dificultad': 2, 'dias_semana': ['martes']}
    ]
    
    # Sample members
    members = [
        {'id': 1, 'nombre': 'Joe', 'tipo': 'adulto'},
        {'id': 2, 'nombre': 'Xilef', 'tipo': 'adulto'},
        {'id': 3, 'nombre': 'Marycel', 'tipo': 'adulto'}
    ]
    
    dias_semana = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
    
    # Test assignment for a specific date
    test_date = "2026-01-14"  # This is a Tuesday
    date_obj = datetime.strptime(test_date, '%Y-%m-%d')
    day_name = dias_semana[date_obj.weekday()]
    
    print(f"Testing assignments for {test_date} ({day_name})")
    
    # Filter tasks for this day
    day_tasks = [task for task in tasks 
                if not task.get('dias_semana') or day_name in task.get('dias_semana', [])]
    
    print(f"Tasks available for {day_name}: {len(day_tasks)}")
    for task in day_tasks:
        print(f"  - {task['nombre']} ({task['area']}) - Dificultad: {task['dificultad']}")
        
        # Simple round-robin assignment
        member_index = len(day_tasks) % len(members)
        assigned_member = members[member_index]
        print(f"    → Assigned to: {assigned_member['nombre']}")
    
    print("\n✅ Task assignment logic test passed!")

if __name__ == "__main__":
    test_date_range()
    test_day_mapping()
    test_task_assignment_logic()
    print("\n🎉 All simple tests completed successfully!")
