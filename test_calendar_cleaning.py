#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for calendar cleaning system
"""

from database import Database
from cleaning_manager import CleaningManager
from datetime import datetime, timedelta

def test_calendar_system():
    """Test the calendar cleaning system"""
    
    print("🧪 Testing Calendar Cleaning System")
    print("=" * 50)
    
    try:
        # Initialize components
        db = Database()
        cleaning_manager = CleaningManager(db)
        
        # Test 1: Initialize default tasks
        print("\n1️⃣ Initializing default cleaning tasks...")
        success = cleaning_manager.initialize_default_tasks()
        print(f"   ✓ Tasks initialized: {success}")
        
        # Test 2: Get family members
        print("\n2️⃣ Getting family members...")
        members = cleaning_manager.get_family_members()
        print(f"   ✓ Found {len(members)} family members:")
        for member in members:
            print(f"     - {member['nombre']} ({member['tipo']})")
        
        # Test 3: Assign tasks to calendar dates
        print("\n3️⃣ Assigning tasks to calendar dates...")
        start_date = "2026-01-14"
        end_date = "2026-01-20"
        
        result = cleaning_manager.assign_tasks_to_calendar_dates(start_date, end_date)
        print(f"   ✓ Assignment success: {result['success']}")
        
        if result['success']:
            print(f"   ✓ Total assignments: {result['total_assignments']}")
            print(f"   ✓ Dates covered: {len(result['dates_covered'])}")
            
            # Show sample assignments
            print("\n   Sample assignments:")
            for assignment in result['assignments'][:5]:  # Show first 5
                print(f"     - {assignment['fecha']}: {assignment['task_nombre']} → {assignment['member_name']}")
        
        # Test 4: Get calendar schedule
        print("\n4️⃣ Getting calendar schedule...")
        schedule_result = cleaning_manager.get_calendar_schedule(start_date, end_date)
        print(f"   ✓ Schedule success: {schedule_result['success']}")
        
        if schedule_result['success']:
            print(f"   ✓ Total assignments in schedule: {schedule_result['total_assignments']}")
            print(f"   ✓ Completion rate: {schedule_result['completion_rate']:.1f}%")
            
            # Show daily breakdown
            print("\n   Daily breakdown:")
            for date, assignments in schedule_result['schedule'].items():
                if assignments:
                    print(f"     {date}: {len(assignments)} tasks")
                    for assignment in assignments:
                        status = "✅" if assignment.get('completado') else "⏳"
                        print(f"       {status} {assignment['task_nombre']} → {assignment.get('member_name', 'N/A')}")
        
        # Test 5: Test specific day query
        print("\n5️⃣ Testing specific day query...")
        test_date = "2026-01-15"
        day_assignments = db.get_calendar_cleaning_assignments(test_date)
        print(f"   ✓ Found {len(day_assignments)} assignments for {test_date}")
        
        for assignment in day_assignments:
            print(f"     - {assignment['task_nombre']} ({assignment.get('area', 'N/A')}) → {assignment.get('member_name', 'N/A')}")
        
        print("\n✅ All tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_calendar_system()
