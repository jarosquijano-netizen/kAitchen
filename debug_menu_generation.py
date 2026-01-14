import requests
import json

# Test menu generation with debug
test_data = {
    "week_start_date": "2026-01-12",
    "preferences": {
        "include_weekend": True,
        "include_breakfast": True,
        "include_lunch": True,
        "include_dinner": True
    }
}

print("=== ENVIANDO PETICIÓN DE GENERACIÓN ===")
response = requests.post('http://localhost:7000/api/menu/generate', json=test_data)

print(f"Status: {response.status_code}")
if response.status_code == 200:
    result = response.json()
    print(f"Success: {result.get('success')}")
    
    if 'menu' in result:
        menu = result['menu']
        print(f"Menu type: {type(menu)}")
        print(f"Menu keys: {list(menu.keys()) if isinstance(menu, dict) else 'Not a dict'}")
        
        # Check if it has expected structure
        if isinstance(menu, dict):
            if 'menu_adultos' in menu or 'menu_ninos' in menu or 'dias' in menu:
                print("Menu has expected structure")
            else:
                print("Menu missing expected structure keys")
                print("Available keys:", list(menu.keys()))
                
                # Check if it's a single recipe
                if 'nombre' in menu and 'ingredientes' in menu:
                    print("Menu appears to be a single recipe instead of weekly menu")
                    print("This suggests Claude is not following the prompt instructions")
    else:
        print(f"Raw menu: {str(menu)[:500]}...")
        
    if 'raw_response' in result:
        raw = result['raw_response']
        print(f"\n=== RAW RESPONSE (first 1000 chars) ===")
        print(raw[:1000])
        
        # Check if response contains expected structure indicators
        if 'menu_adultos' in raw or 'menu_ninos' in raw or '"lunes"' in raw:
            print("Raw response contains expected structure")
        else:
            print("Raw response missing expected structure")
else:
    print(f"Error: {response.text}")
