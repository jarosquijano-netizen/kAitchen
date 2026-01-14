import sqlite3
import json

conn = sqlite3.connect('family_kitchen.db')
cursor = conn.cursor()

# Check actual values in ingredients column
cursor.execute("SELECT id, title, ingredients FROM recipes LIMIT 3")
rows = cursor.fetchall()

print("=== RECIPE INGREDIENTS VALUES ===")
for row in rows:
    recipe_id, title, ingredients = row
    print(f"Recipe {recipe_id}: {title}")
    print(f"Ingredients type: {type(ingredients)}")
    print(f"Ingredients value: {repr(ingredients)}")
    
    if ingredients is not None:
        try:
            parsed = json.loads(ingredients)
            print(f"Parsed successfully: {type(parsed)} - {len(parsed)} items")
        except Exception as e:
            print(f"JSON parse error: {e}")
    else:
        print("Ingredients is None")
    print("---")

conn.close()
