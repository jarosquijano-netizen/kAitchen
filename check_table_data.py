import sqlite3

conn = sqlite3.connect('family_kitchen.db')
cursor = conn.cursor()

# Check recipes table
print("=== RECIPES TABLE ===")
cursor.execute("SELECT COUNT(*) FROM recipes")
recipe_count = cursor.fetchone()[0]
print(f"Total recipes: {recipe_count}")

if recipe_count > 0:
    cursor.execute("SELECT title, url FROM recipes LIMIT 5")
    recipes = cursor.fetchall()
    print("Recent recipes:")
    for title, url in recipes:
        print(f"  - {title} ({url})")
else:
    print("No recipes found")

# Check weekly_menus table  
print("\n=== WEEKLY_MENUS TABLE ===")
cursor.execute("SELECT COUNT(*) FROM weekly_menus")
menu_count = cursor.fetchone()[0]
print(f"Total menus: {menu_count}")

if menu_count > 0:
    cursor.execute("SELECT week_start_date, created_at FROM weekly_menus ORDER BY created_at DESC LIMIT 3")
    menus = cursor.fetchall()
    print("Recent menus:")
    for week_start, created_at in menus:
        print(f"  - Week: {week_start}, Created: {created_at}")
else:
    print("No menus found")

# Check adults/children tables
print("\n=== FAMILY PROFILES ===")
cursor.execute("SELECT COUNT(*) FROM adults")
adult_count = cursor.fetchone()[0]
cursor.execute("SELECT COUNT(*) FROM children")  
child_count = cursor.fetchone()[0]
print(f"Adults: {adult_count}, Children: {child_count}")

if adult_count > 0:
    cursor.execute("SELECT nombre, edad FROM adults LIMIT 3")
    adults = cursor.fetchall()
    print("Adults:")
    for nombre, edad in adults:
        print(f"  - {nombre} ({edad} years)")

if child_count > 0:
    cursor.execute("SELECT nombre, edad FROM children LIMIT 3")
    children = cursor.fetchall()
    print("Children:")
    for nombre, edad in children:
        print(f"  - {nombre} ({edad} years)")

conn.close()
