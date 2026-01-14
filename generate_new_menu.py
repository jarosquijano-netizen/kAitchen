import requests

# Generate new menu with current recipes
test_data = {
    "week_start_date": "2026-01-12",
    "preferences": {
        "include_weekend": True,
        "include_breakfast": True,
        "include_lunch": True,
        "include_dinner": True
    }
}

print("=== GENERATING NEW MENU ===")
response = requests.post('http://localhost:7000/api/menu/generate', json=test_data)

if response.status_code == 200:
    result = response.json()
    print(f"Success: {result.get('success')}")
    
    if result.get('success'):
        print("New menu generated successfully!")
        
        # Check shopping lists
        if 'menu' in result:
            menu = result['menu']
            if 'menu_adultos' in menu and 'lista_compras' in menu['menu_adultos']:
                shopping = menu['menu_adultos']['lista_compras']
                if 'por_categoria' in shopping:
                    categories = shopping['por_categoria']
                    print(f"\n=== NEW SHOPPING LIST ===")
                    total_items = sum(len(items) for items in categories.values())
                    print(f"Total items: {total_items}")
                    
                    for cat, items in categories.items():
                        if items:
                            print(f"{cat}: {len(items)} items")
                            for item in items[:2]:  # Show first 2 items
                                print(f"  - {item['nombre']}: {item['cantidad']}")
    else:
        print(f"Error generating menu: {result.get('error', 'Unknown error')}")
else:
    print(f"HTTP Error: {response.status_code} - {response.text}")
