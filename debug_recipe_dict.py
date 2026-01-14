import sqlite3

conn = sqlite3.connect('family_kitchen.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

cursor.execute("SELECT * FROM recipes LIMIT 1")
row = cursor.fetchone()

print("=== DEBUG RECIPE DICT ===")
print(f"Row type: {type(row)}")
print(f"Row: {row}")

if row:
    recipe = dict(row)
    print(f"Recipe dict: {recipe}")
    print(f"Recipe keys: {list(recipe.keys())}")
    
    if 'ingredients' in recipe:
        print(f"ingredients exists: True")
        print(f"ingredients value: {recipe['ingredients']}")
        print(f"ingredients type: {type(recipe['ingredients'])}")
    else:
        print("ingredients exists: False")

conn.close()
