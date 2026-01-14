#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Probar la integración completa del sistema de limpieza inteligente
"""
import requests
import json

def test_smart_cleaning_integration():
    base_url = "http://localhost:7000"
    
    print("🧪 Probando integración completa de limpieza inteligente...")
    
    # 1. Test family members
    print("\n1. 📋 Verificando miembros de la familia...")
    try:
        response = requests.get(f"{base_url}/api/family/summary")
        if response.status_code == 200:
            family_data = response.json()
            print(f"✅ Familia cargada: {family_data}")
        else:
            print(f"❌ Error cargando familia: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return
    
    # 2. Test cleaning capacity
    print("\n2. 🧹 Verificando capacidades de limpieza...")
    try:
        response = requests.get(f"{base_url}/api/cleaning/capacity")
        if response.status_code == 200:
            capacity_data = response.json()
            print(f"✅ Capacidades cargadas: {json.dumps(capacity_data['data'], indent=2, ensure_ascii=False)}")
        else:
            print(f"❌ Error cargando capacidades: {response.status_code}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
    
    # 3. Test house config
    print("\n3. 🏠 Verificando configuración de la casa...")
    try:
        response = requests.get(f"{base_url}/api/house/config")
        if response.status_code == 200:
            house_data = response.json()
            print(f"✅ Configuración de casa: {json.dumps(house_data['data'], indent=2, ensure_ascii=False)}")
        else:
            print(f"❌ Error cargando configuración: {response.status_code}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
    
    # 4. Test smart cleaning plan generation
    print("\n4. ⚡ Generando plan de limpieza inteligente...")
    try:
        response = requests.post(f"{base_url}/api/cleaning/generate-smart-plan", 
                              json={}, 
                              headers={'Content-Type': 'application/json'})
        if response.status_code == 200:
            plan_data = response.json()
            print(f"✅ Plan generado exitosamente!")
            
            # Show distribution
            if plan_data.get('success') and plan_data.get('plan'):
                plan = plan_data['plan']
                print(f"\n📊 Resumen del Plan:")
                print(f"  - Total tareas: {plan.get('total_tasks', 0)}")
                print(f"  - Tareas asignadas: {plan.get('assigned_tasks', 0)}")
                print(f"  - Tareas sin asignar: {plan.get('unassigned_tasks', 0)}")
                print(f"  - Horas semanales estimadas: {plan.get('estimated_weekly_hours', 0):.1f}h")
                
                # Show member distribution
                distribution = plan.get('distribution', {})
                if distribution:
                    print(f"\n👥 Distribución por miembro:")
                    for member_name, member_data in distribution.items():
                        print(f"  - {member_name} ({member_data.get('edad', '?')} años, {member_data.get('tipo', '?')}):")
                        print(f"    * Tareas: {len(member_data.get('tasks', []))}")
                        print(f"    * Horas: {member_data.get('total_hours', 0)}h")
                        print(f"    * Porcentaje: {member_data.get('percentage', 0)}%")
                        print(f"    * Tareas específicas: {', '.join(member_data.get('tasks', [])[:3])}{'...' if len(member_data.get('tasks', [])) > 3 else ''}")
                
                # Show sample assigned tasks
                tasks = plan.get('tasks', [])
                assigned_tasks = [t for t in tasks if t.get('asignado_a') != 'Sin asignar']
                if assigned_tasks:
                    print(f"\n📋 Ejemplo de tareas asignadas:")
                    for i, task in enumerate(assigned_tasks[:5], 1):
                        print(f"  {i}. {task['nombre']} → {task['asignado_a']} ({task.get('dificultad', 0)}/5 dificultad)")
                    if len(assigned_tasks) > 5:
                        print(f"  ... y {len(assigned_tasks) - 5} más tareas")
                
        else:
            print(f"❌ Error generando plan: {response.status_code}")
            print(f"Respuesta: {response.text}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
    
    print("\n🎉 Prueba completada!")

if __name__ == "__main__":
    test_smart_cleaning_integration()
