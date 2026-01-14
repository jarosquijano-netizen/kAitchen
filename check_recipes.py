import requests

# Check recipes endpoint
response = requests.get('http://localhost:7000/api/recipes')
if response.status_code == 200:
    data = response.json()
    print(f"Status: {data.get('success')}")
    print(f"Count: {data.get('count', 0)}")
    
    if data.get('data'):
        recipes = data['data']
        print(f"Recipes found: {len(recipes)}")
        
        if recipes:
            print("First 3 recipes:")
            for i, recipe in enumerate(recipes[:3], 1):
                print(f"  {i}. {recipe.get('title', 'No title')}")
        else:
            print("No recipes in data")
    else:
        print("No data field in response")
else:
    print(f"Error: {response.status_code} - {response.text}")
