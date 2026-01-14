import requests

def test_shopping_simple():
    print("=== TESTING SHOPPING LIST ===\n")
    
    try:
        # Test shopping list endpoint
        response = requests.get('http://localhost:7000/api/shopping/list/2026-01-12')
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                shopping_data = data.get('data', {})
                categories = shopping_data.get('categories', {})
                total_items = shopping_data.get('total_items', 0)
                print(f"OK: Shopping list working - {total_items} items in {len(categories)} categories")
                
                # Show categories
                for category, items in categories.items():
                    print(f"   {category}: {len(items)} items")
            else:
                print(f"ERROR: {data.get('error')}")
        else:
            print(f"ERROR: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    test_shopping_simple()
