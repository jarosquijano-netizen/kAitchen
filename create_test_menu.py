import requests

# Create a test menu for the current week
menu_data = {
    "week_start": "2026-01-12",
    "menu": {
        "lunes": {
            "adultos": {
                "desayuno": "Tostadas con aguacate",
                "almuerzo": "Ensalada César con pollo",
                "cena": "Pasta a la boloñesa"
            },
            "niños": {
                "desayuno": "Cereal con leche",
                "almuerzo": "Sandwich de jamón y queso",
                "cena": "Pasta con tomate"
            }
        },
        "martes": {
            "adultos": {
                "desayuno": "Huevos revueltos",
                "almuerzo": "Sopa de verduras",
                "cena": "Pollo asado con patatas"
            },
            "niños": {
                "desayuno": "Tostadas con mermelada",
                "almuerzo": "Sopa de letras",
                "cena": "Nuggets de pollo"
            }
        }
    }
}

response = requests.post('http://localhost:7000/api/menu/generate', json=menu_data)
print("Create menu response:", response.status_code, response.json())

# Check if menu exists now
response = requests.get('http://localhost:7000/api/menu/week/2026-01-12')
print("Check menu response:", response.status_code, response.json())
