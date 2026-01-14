import requests
import json

# Get the current week menu and examine its structure
response = requests.get('http://localhost:7000/api/menu/current-week')
if response.status_code == 200:
    data = response.json()
    menu_data = data['data']['menu_data']
    
    print("=== MENU DATA STRUCTURE ===")
    print(f"Type: {type(menu_data)}")
    
    if isinstance(menu_data, dict):
        print(f"Keys: {list(menu_data.keys())}")
        
        # Check if it has the expected structure
        expected_keys = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
        has_days = any(key in menu_data for key in expected_keys)
        print(f"Has day keys: {has_days}")
        
        # Look for nested structures
        for key, value in menu_data.items():
            print(f"  {key}: {type(value)} - {str(value)[:100]}...")
            
            if isinstance(value, dict):
                print(f"    Sub-keys: {list(value.keys())}")
                
    else:
        print(f"Content preview: {str(menu_data)[:500]}...")
else:
    print(f"Error: {response.status_code} - {response.text}")
