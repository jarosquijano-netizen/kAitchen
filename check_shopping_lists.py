import requests

# Get current week menu
response = requests.get('http://localhost:7000/api/menu/current-week')
if response.status_code == 200:
    data = response.json()
    if data.get('success') and 'data' in data:
        menu_data = data['data']['menu_data']
        
        print("=== CURRENT WEEK MENU ===")
        print(f"Menu keys: {list(menu_data.keys())}")
        
        # Check shopping lists
        if 'menu_adultos' in menu_data:
            adults_menu = menu_data['menu_adultos']
            if 'lista_compras' in adults_menu:
                shopping_list = adults_menu['lista_compras']
                print(f"\n=== SHOPPING LIST STRUCTURE ===")
                print(f"Keys: {list(shopping_list.keys())}")
                
                if 'por_categoria' in shopping_list:
                    categories = shopping_list['por_categoria']
                    print(f"Categories: {list(categories.keys())}")
                    
                    for cat_name, items in categories.items():
                        print(f"  {cat_name}: {len(items)} items")
                        if items:
                            print(f"    First item: {items[0]}")
                else:
                    print("No 'por_categoria' found")
            else:
                print("No 'lista_compras' found in menu_adultos")
        else:
            print("No 'menu_adultos' found")
    else:
        print("Invalid response structure")
else:
    print(f"Error getting menu: {response.status_code}")
