import sqlite3
import json

# Sample recipes to restore
sample_recipes = [
    {
        "title": "Tortilla Española",
        "url": "https://www.recetasgratis.net/receta-de-tortilla-espanola-tradicional-id.html",
        "cuisine_type": "Española",
        "prep_time": 25,
        "ingredients": ["huevos", "patatas", "cebolla", "aceite de oliva", "sal"],
        "difficulty": "Fácil"
    },
    {
        "title": "Paella Valenciana",
        "url": "https://www.recetasgratis.net/receta-de-paella-valenciana-id.html", 
        "cuisine_type": "Española",
        "prep_time": 60,
        "ingredients": ["arroz", "pollo", "conejo", "frijoles verdes", "garrofó", "tomate", "pimentón", "azafrán"],
        "difficulty": "Media"
    },
    {
        "title": "Gazpacho Andaluz",
        "url": "https://www.recetasgratis.net/receta-de-gazpacho-andaluz-id.html",
        "cuisine_type": "Española", 
        "prep_time": 15,
        "ingredients": ["tomate", "pimiento", "pepino", "cebolla", "ajo", "pan duro", "aceite de oliva", "vinagre", "sal"],
        "difficulty": "Fácil"
    },
    {
        "title": "Lentejas a la Riojana",
        "url": "https://www.recetasgratis.net/receta-de-lentejas-a-la-riojana-id.html",
        "cuisine_type": "Española",
        "prep_time": 45,
        "ingredients": ["lentejas", "chorizo", "morcilla", "cebolla", "ajo", "pimentón", "laurel"],
        "difficulty": "Media"
    },
    {
        "title": "Pollo al Chilindrón",
        "url": "https://www.recetasgratis.net/receta-de-pollo-al-chilindron-id.html",
        "cuisine_type": "Española",
        "prep_time": 40,
        "ingredients": ["pollo", "cebolla", "pimiento", "ajo", "tomate", "vino blanco", "aceite", "laurel"],
        "difficulty": "Fácil"
    }
]

def restore_recipes():
    print("Restaurando recetas de ejemplo...")
    
    conn = sqlite3.connect('family_kitchen.db')
    cursor = conn.cursor()
    
    try:
        for recipe in sample_recipes:
            # Insert recipe
            cursor.execute('''
                INSERT INTO recipes (title, url, cuisine_type, prep_time, ingredients, difficulty)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                recipe['title'],
                recipe['url'], 
                recipe['cuisine_type'],
                recipe['prep_time'],
                json.dumps(recipe['ingredients']),
                recipe['difficulty']
            ))
        
        conn.commit()
        print(f"OK: {len(sample_recipes)} recetas restauradas correctamente")
        
    except Exception as e:
        print(f"ERROR: Error restaurando recetas: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    restore_recipes()
