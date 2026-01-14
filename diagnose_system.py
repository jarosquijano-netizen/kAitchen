import requests
import json

def test_endpoint(name, url, method='GET', data=None):
    try:
        if method == 'GET':
            response = requests.get(url)
        else:
            response = requests.post(url, json=data)
        
        print(f"\n=== {name} ===")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                print(f"Success: {result.get('success', False)}")
                
                if 'data' in result:
                    data = result['data']
                    print(f"Data type: {type(data)}")
                    if isinstance(data, dict):
                        print(f"Data keys: {list(data.keys())}")
                    elif isinstance(data, list):
                        print(f"Data length: {len(data)}")
                elif 'schedule' in result:
                    schedule = result['schedule']
                    print(f"Schedule type: {type(schedule)}")
                    if isinstance(schedule, dict):
                        print(f"Schedule keys: {list(schedule.keys())}")
                else:
                    print(f"Response keys: {list(result.keys())}")
                    
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}")
                print(f"Raw response: {response.text[:500]}...")
        else:
            print(f"Error response: {response.text}")
            
    except Exception as e:
        print(f"Request error: {e}")

# Test all problematic endpoints
print("DIAGNOSTICANDO SISTEMA...")

# Menu endpoints
test_endpoint("Current Week Menu", "http://localhost:7000/api/menu/current-week")
test_endpoint("Week Menu", "http://localhost:7000/api/menu/week/2026-01-12")

# Cleaning endpoints  
test_endpoint("Cleaning Tasks", "http://localhost:7000/api/cleaning/tasks")
test_endpoint("Cleaning Schedule", "http://localhost:7000/api/cleaning/schedule/2026-01-12")
test_endpoint("Cleaning Preferences", "http://localhost:7000/api/cleaning/preferences")

print("\nDIAGNOSTICO COMPLETADO")
