import sqlite3
import json

conn = sqlite3.connect('family_kitchen.db')
cursor = conn.cursor()

# Check weekly_menus table
cursor.execute("SELECT week_start_date, menu_data FROM weekly_menus ORDER BY created_at DESC LIMIT 1")
row = cursor.fetchone()

if row:
    week_start, menu_data = row
    print(f"=== MENU FROM DATABASE ===")
    print(f"Week: {week_start}")
    print(f"Menu data type: {type(menu_data)}")
    
    if menu_data:
        try:
            menu_dict = json.loads(menu_data)
            print(f"Menu keys: {list(menu_dict.keys())}")
            
            if 'menu_adultos' in menu_dict:
                adults = menu_dict['menu_adultos']
                if 'dias' in adults:
                    days = adults['dias']
                    print(f"Days in menu: {list(days.keys())}")
                    
                    # Check first day's meals
                    if days:
                        first_day = list(days.keys())[0]
                        meals = days[first_day]
                        print(f"Meals for {first_day}: {list(meals.keys())}")
                        
                        # Check ingredients from first meal
                        for meal_name, meal_data in meals.items():
                            if 'ingredientes' in meal_data:
                                print(f"Ingredients for {meal_name}: {meal_data['ingredientes'][:5]}")
                                break
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
else:
    print("No menu found in database")

conn.close()
