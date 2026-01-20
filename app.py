from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.exceptions import NotFound, InternalServerError
from flask_cors import CORS
import os
import json
from dotenv import load_dotenv
from database import Database
from recipe_extractor import RecipeExtractor
from menu_generator import MenuGenerator
from cleaning_manager import CleaningManager
from datetime import datetime, timedelta

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ .env file loaded successfully")
except Exception as e:
    print(f"Warning: Error loading .env file with dotenv: {e}")
    # Fallback: load manually
    try:
        with open('.env', 'r', encoding='utf-8') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key.strip()] = value.strip()
        print("✅ Environment variables loaded manually")
    except Exception as e2:
        print(f"Warning: Error manual loading .env: {e2}")

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', os.urandom(24))
# Disable ALL cache to force reload
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.jinja_env.auto_reload = True
app.jinja_env.cache = None
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

# CORS Configuration
cors_origins = os.getenv('CORS_ORIGINS', '*').split(',')
CORS(app, origins=cors_origins)

# Error handlers for JSON responses - MUST be defined before routes
@app.errorhandler(NotFound)
def not_found(error):
    """Return JSON for 404 errors on API routes"""
    if request.path.startswith('/api/'):
        return jsonify({
            'success': False,
            'error': f'Recurso no encontrado: {request.path}'
        }), 404
    return error

@app.errorhandler(InternalServerError)
def internal_error(error):
    """Return JSON for 500 errors on API routes"""
    if request.path.startswith('/api/'):
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor'
        }), 500
    return error

# Initialize components with environment-aware database
db = Database()
cleaning_manager = CleaningManager(db)

# Force database initialization to ensure all tables exist
print("Forzando inicializacion de base de datos...")
try:
    # This will create all tables if they don't exist
    db.init_database()
    print("Base de datos inicializada correctamente")
except Exception as e:
    print(f"Error inicializando base de datos: {str(e)}")

extractor = RecipeExtractor()

# Menu generator will be initialized when needed (requires API key)
menu_gen = None

def get_menu_generator():
    """Lazy initialization of menu generator"""
    global menu_gen
    if menu_gen is None:
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if api_key:
            menu_gen = MenuGenerator(api_key)
        else:
            raise ValueError("ANTHROPIC_API_KEY no configurada")
    return menu_gen

# ==================== WEB ROUTES ====================

@app.route('/')
def index():
    """Main admin interface"""
    return render_template('index.html')

@app.route('/tv')
def tv_view():
    """TV-friendly menu display"""
    return render_template('tv_display_new.html')

@app.route('/tv2')
def tv_view2():
    """TV-friendly menu display - NEW CLEAN VERSION"""
    return render_template('tv_display_new.html')

@app.route('/menu/visualizer')
def menu_visualizer():
    """Menu visualizer page"""
    return render_template('menu_visualizer.html')

@app.route('/recover-api-key')
def recover_api_key():
    """Temporary page to recover API key from server memory (LOCAL ONLY)"""
    # Only allow from localhost
    if request.remote_addr not in ['127.0.0.1', '::1', 'localhost']:
        return "This page is only available from localhost", 403
    return render_template('recover_api_key.html')

# ==================== ADULT PROFILES API ====================

@app.route('/api/adults', methods=['GET'])
def get_adults():
    """Get all adult profiles"""
    try:
        adults = db.get_all_adults()
        return jsonify({
            'success': True,
            'data': adults,
            'count': len(adults)
        })
    except Exception as e:
        import traceback
        print(f"[ERROR] get_adults: {str(e)}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Error al obtener adultos: {str(e)}'
        }), 500

@app.route('/api/adults', methods=['POST'])
def add_adult():
    """Add a new adult profile"""
    try:
        data = request.json
        adult_id = db.add_adult(data)
        return jsonify({
            'success': True,
            'message': 'Perfil de adulto añadido correctamente',
            'id': adult_id
        }), 201
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/adults/<int:adult_id>', methods=['PUT'])
def update_adult(adult_id):
    """Update an adult profile"""
    try:
        data = request.json
        success = db.update_adult(adult_id, data)
        if success:
            return jsonify({
                'success': True,
                'message': 'Perfil de adulto actualizado correctamente'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Perfil no encontrado'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/adults/<int:adult_id>', methods=['DELETE'])
def delete_adult(adult_id):
    """Delete an adult profile"""
    try:
        success = db.delete_adult(adult_id)
        if success:
            return jsonify({
                'success': True,
                'message': 'Perfil eliminado correctamente'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Perfil no encontrado'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

# ==================== CHILDREN PROFILES API ====================

@app.route('/api/children', methods=['GET'])
def get_children():
    """Get all children profiles"""
    try:
        children = db.get_all_children()
        return jsonify({
            'success': True,
            'data': children,
            'count': len(children)
        })
    except Exception as e:
        import traceback
        print(f"[ERROR] get_children: {str(e)}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Error al obtener niños: {str(e)}'
        }), 500

@app.route('/api/children', methods=['POST'])
def add_child():
    """Add a new child profile"""
    try:
        data = request.json
        child_id = db.add_child(data)
        return jsonify({
            'success': True,
            'message': 'Perfil de niño añadido correctamente',
            'id': child_id
        }), 201
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/children/<int:child_id>', methods=['PUT'])
def update_child(child_id):
    """Update a child profile"""
    try:
        data = request.json
        success = db.update_child(child_id, data)
        if success:
            return jsonify({
                'success': True,
                'message': 'Perfil de niño actualizado correctamente'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Perfil no encontrado'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/children/<int:child_id>', methods=['DELETE'])
def delete_child(child_id):
    """Delete a child profile"""
    try:
        success = db.delete_child(child_id)
        if success:
            return jsonify({
                'success': True,
                'message': 'Perfil eliminado correctamente'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Perfil no encontrado'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

# ==================== RECIPE EXTRACTION API ====================

@app.route('/api/recipes/extract', methods=['POST'])
def extract_recipe():
    """Extract recipe from URL"""
    try:
        data = request.json
        url = data.get('url')
        
        if not url:
            return jsonify({
                'success': False,
                'error': 'URL es requerida'
            }), 400
        
        print(f"[ExtractRecipe] Extracting recipe from URL: {url}")
        
        # Extract recipe
        recipe_data = extractor.extract_from_url(url)
        
        if recipe_data.get('error'):
            print(f"[ExtractRecipe] Extraction error: {recipe_data['error']}")
            return jsonify({
                'success': False,
                'error': recipe_data['error']
            }), 400
        
        print(f"[ExtractRecipe] Recipe extracted: {recipe_data.get('title', 'Unknown')}")
        print(f"[ExtractRecipe] Recipe data keys: {list(recipe_data.keys())}")
        
        # Save to database
        try:
            recipe_id = db.add_recipe(recipe_data)
            recipe_data['id'] = recipe_id
            print(f"[ExtractRecipe] Recipe saved successfully with ID: {recipe_id}")
        except Exception as db_error:
            print(f"[ExtractRecipe] Database error: {str(db_error)}")
            import traceback
            print(f"[ExtractRecipe] Traceback: {traceback.format_exc()}")
            return jsonify({
                'success': False,
                'error': f'Error al guardar la receta: {str(db_error)}'
            }), 500
        
        return jsonify({
            'success': True,
            'message': 'Receta extraída y guardada correctamente',
            'data': recipe_data
        })
        
    except Exception as e:
        import traceback
        print(f"[ExtractRecipe] Unexpected error: {str(e)}")
        print(f"[ExtractRecipe] Traceback: {traceback.format_exc()}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/recipes/<int:recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    """Delete a recipe"""
    try:
        # Verify recipe exists first
        recipes = db.get_all_recipes()
        recipe_exists = any(r.get('id') == recipe_id for r in recipes)
        
        if not recipe_exists:
            return jsonify({
                'success': False,
                'error': f'Receta con ID {recipe_id} no encontrada'
            }), 404
        
        success = db.delete_recipe(recipe_id)
        if success:
            return jsonify({
                'success': True,
                'message': 'Receta eliminada correctamente'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo eliminar la receta'
            }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/recipes', methods=['GET'])
def get_recipes():
    """Get all recipes"""
    recipes = db.get_all_recipes()
    return jsonify({
        'success': True,
        'data': recipes,
        'count': len(recipes)
    })

@app.route('/api/recipes/search', methods=['GET'])
def search_recipe():
    """Search for a recipe by title (case-insensitive)"""
    try:
        title = request.args.get('title', '').strip()
        if not title:
            return jsonify({
                'success': False,
                'error': 'Title parameter is required'
            }), 400
        
        # Use the database method to find recipe by title
        recipe = db._find_recipe_by_title(title)
        
        if recipe:
            return jsonify({
                'success': True,
                'data': {
                    'id': recipe.get('id'),
                    'title': recipe.get('title'),
                    'url': recipe.get('url'),
                    'instructions': recipe.get('instructions')
                }
            })
        else:
            return jsonify({
                'success': False,
                'data': None
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/recipe/view')
def view_recipe():
    """Display recipe page for mobile viewing"""
    try:
        title = request.args.get('title', '').strip()
        if not title:
            return render_template('recipe_view.html', error='No se especificó el título de la receta')
        
        # Find recipe by title
        recipe = db._find_recipe_by_title(title)
        
        if not recipe:
            return render_template('recipe_view.html', error=f'Receta "{title}" no encontrada')
        
        # Parse ingredients if stored as JSON string
        ingredients = recipe.get('ingredients', '')
        if isinstance(ingredients, str):
            try:
                ingredients = json.loads(ingredients) if ingredients else []
            except:
                ingredients = [ingredients] if ingredients else []
        
        # Parse instructions
        instructions = recipe.get('instructions', '')
        if isinstance(instructions, str) and instructions:
            # Split by newlines or numbers if formatted as steps
            if '\n' in instructions:
                instructions = [step.strip() for step in instructions.split('\n') if step.strip()]
            else:
                instructions = [instructions]
        else:
            instructions = []
        
        recipe_data = {
            'title': recipe.get('title', title),
            'url': recipe.get('url', ''),
            'ingredients': ingredients if isinstance(ingredients, list) else [ingredients] if ingredients else [],
            'instructions': instructions,
            'prep_time': recipe.get('prep_time'),
            'cook_time': recipe.get('cook_time'),
            'servings': recipe.get('servings'),
            'cuisine_type': recipe.get('cuisine_type', ''),
            'meal_type': recipe.get('meal_type', ''),
            'difficulty': recipe.get('difficulty', ''),
            'image_url': recipe.get('image_url', ''),
            'description': recipe.get('extracted_data', '')
        }
        
        return render_template('recipe_view.html', recipe=recipe_data)
    except Exception as e:
        return render_template('recipe_view.html', error=f'Error al cargar la receta: {str(e)}')

@app.route('/api/recipes/batch', methods=['POST'])
def extract_multiple_recipes():
    """Extract multiple recipes from URLs"""
    try:
        data = request.json
        urls = data.get('urls', [])
        
        if not urls:
            return jsonify({
                'success': False,
                'error': 'Se requiere al menos una URL'
            }), 400
        
        results = []
        for url in urls:
            recipe_data = extractor.extract_from_url(url)
            if not recipe_data.get('error'):
                recipe_id = db.add_recipe(recipe_data)
                recipe_data['id'] = recipe_id
            results.append(recipe_data)
        
        success_count = sum(1 for r in results if not r.get('error'))
        
        return jsonify({
            'success': True,
            'message': f'{success_count}/{len(urls)} recetas extraídas correctamente',
            'data': results
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

# ==================== MENU GENERATION API ====================

@app.route('/api/menu/generate', methods=['POST'])
def generate_menu():
    """Generate weekly menu using AI"""
    try:
        # Get family profiles
        adults = db.get_all_adults()
        children = db.get_all_children()
        
        if not adults and not children:
            return jsonify({
                'success': False,
                'error': 'Debes añadir al menos un perfil familiar primero'
            }), 400
        
        # Get optional parameters from request
        data = request.json or {}
        preferences = data.get('preferences', {})
        day_settings = data.get('day_settings', None)  # NEW: day cooking settings
        week_start_date = data.get('week_start_date', None)  # NEW: specific week start date
        
        # Calculate week start date if not provided
        if not week_start_date:
            # Default to current week (Monday of current week)
            today = datetime.now()
            days_since_monday = today.weekday()  # 0 = Monday, 6 = Sunday
            week_start = (today - timedelta(days=days_since_monday)).strftime('%Y-%m-%d')
            print(f"[GenerateMenu] No week_start_date provided, using current week: {week_start}")
        else:
            # Clean and validate provided date
            try:
                # Remove any whitespace and ensure clean format
                cleaned_date = str(week_start_date).strip()
                print(f"[GenerateMenu] Original week_start_date: '{week_start_date}'")
                print(f"[GenerateMenu] Cleaned week_start_date: '{cleaned_date}'")
                
                # Validate date format
                provided_date = datetime.strptime(cleaned_date, '%Y-%m-%d')
                
                # Use the cleaned date
                week_start = cleaned_date
                print(f"[GenerateMenu] Using provided week_start_date: {week_start}")
                
                # Log warning if it's not a Monday (for debugging)
                if provided_date.weekday() != 0:
                    print(f"[GenerateMenu] WARNING: week_start_date {week_start} is not a Monday (weekday: {provided_date.weekday()})")
                    
            except ValueError as e:
                print(f"[GenerateMenu] Date validation error: {str(e)}")
                print(f"[GenerateMenu] Invalid date format received: '{week_start_date}'")
                return jsonify({
                    'success': False,
                    'error': f'Formato de fecha inválido. Usa YYYY-MM-DD. Recibido: {str(week_start_date)[:50]}'
                }), 400
        
        # Get menu preferences from database
        menu_prefs = db.get_menu_preferences()
        preferences.update({
            'include_weekend': menu_prefs.get('include_weekend', True),
            'include_breakfast': menu_prefs.get('include_breakfast', True),
            'include_lunch': menu_prefs.get('include_lunch', True),
            'include_dinner': menu_prefs.get('include_dinner', True),
            'excluded_days': menu_prefs.get('excluded_days', [])
        })
        
        # Get recipes
        recipes = db.get_all_recipes()
        
        # Get historical ratings for learning
        historical_ratings = db.get_all_menu_ratings(limit=30)
        
        # Generate menu with enhanced parameters
        gen = get_menu_generator()
        result = gen.generate_weekly_menu(
            adults=adults, 
            children=children, 
            recipes=recipes, 
            preferences=preferences,
            day_settings=day_settings,  # Pass day settings to generator
            historical_ratings=historical_ratings  # Pass historical ratings for learning
        )
        
        if not result['success']:
            return jsonify(result), 400
        
        # Save menu to database with specific week_start
        
        # Include raw_response in metadata so frontend can use it if menu parsing fails
        metadata = {
            'generated_at': result['generated_at'],
            'day_settings': day_settings,
            'preferences': preferences,
            'raw_response': result.get('raw_response', '')  # Include raw response for fallback
        }
        
        menu_id = db.save_weekly_menu(
            week_start, 
            result['menu'],
            metadata
        )
        
        # Extract and save recipes from the generated menu
        try:
            saved_recipe_ids = db.extract_and_save_recipes_from_menu(result['menu'])
            print(f"[GenerateMenu] Saved {len(saved_recipe_ids)} recipes from menu")
        except Exception as e:
            print(f"[GenerateMenu] Error saving recipes from menu: {e}")
            # Don't fail menu generation if recipe saving fails
        
        result['menu_id'] = menu_id
        result['week_start'] = week_start  # Include the week_start in response
        
        return jsonify(result)
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Configura la variable de entorno ANTHROPIC_API_KEY'
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/menu/latest', methods=['GET'])
def get_latest_menu():
    """Get the most recent menu"""
    try:
        menu = db.get_latest_menu()
        
        if not menu:
            return jsonify({
                'success': False,
                'error': 'No hay menús disponibles'
            }), 404
        
        return jsonify({
            'success': True,
            'data': menu
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/menu/week/<week_start>', methods=['GET'])
def get_menu_by_week(week_start):
    """Get menu for a specific week start date (YYYY-MM-DD)"""
    try:
        menu = db.get_menu_by_week_start(week_start)
        
        if not menu:
            return jsonify({
                'success': False,
                'error': f'No hay menú disponible para la semana del {week_start}',
                'week_start': week_start
            }), 404
        
        return jsonify({
            'success': True,
            'data': menu,
            'week_start': week_start
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/menu/current-week', methods=['GET'])
def get_current_week_menu():
    """Get menu for current week (Monday of current week) with fallback to latest menu"""
    try:
        today = datetime.now()
        days_since_monday = today.weekday()  # 0 = Monday, 6 = Sunday
        week_start = (today - timedelta(days=days_since_monday)).strftime('%Y-%m-%d')
        
        print(f"[GetCurrentWeekMenu] Calculating current week start: {week_start} (today: {today.strftime('%Y-%m-%d')})")
        
        menu = db.get_menu_by_week_start(week_start)
        
        if not menu:
            # Fallback to latest menu if no menu for current week
            print(f"[GetCurrentWeekMenu] No menu found for week {week_start}, trying latest menu...")
            latest_menu = db.get_latest_menu()
            
            if latest_menu:
                print(f"[GetCurrentWeekMenu] Using latest menu as fallback (week_start: {latest_menu.get('week_start_date', 'unknown')})")
                return jsonify({
                    'success': True,
                    'data': latest_menu,
                    'week_start': latest_menu.get('week_start_date', week_start),
                    'is_fallback': True  # Indicate this is a fallback
                })
            else:
                return jsonify({
                    'success': False,
                    'error': 'No hay menú disponible para esta semana',
                    'week_start': week_start
                }), 404
        
        return jsonify({
            'success': True,
            'data': menu,
            'week_start': week_start,
            'is_fallback': False
        })
        
    except Exception as e:
        print(f"[GetCurrentWeekMenu] Error: {e}")
        # Try fallback even on error
        try:
            latest_menu = db.get_latest_menu()
            if latest_menu:
                print(f"[GetCurrentWeekMenu] Using latest menu as error fallback")
                return jsonify({
                    'success': True,
                    'data': latest_menu,
                    'week_start': latest_menu.get('week_start_date', 'unknown'),
                    'is_fallback': True
                })
        except:
            pass
        
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/menu/next-week', methods=['GET'])
def get_next_week_menu():
    """Get menu for next week (Monday of next week)"""
    try:
        today = datetime.now()
        days_since_monday = today.weekday()  # 0 = Monday, 6 = Sunday
        current_week_start = today - timedelta(days=days_since_monday)
        next_week_start = (current_week_start + timedelta(days=7)).strftime('%Y-%m-%d')
        
        menu = db.get_menu_by_week_start(next_week_start)
        
        if not menu:
            return jsonify({
                'success': False,
                'error': 'No hay menú disponible para la próxima semana',
                'week_start': next_week_start
            }), 404
        
        return jsonify({
            'success': True,
            'data': menu,
            'week_start': next_week_start
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/shopping/list/<week_start>', methods=['GET'])
def get_shopping_list(week_start):
    """Get shopping list for a specific week"""
    try:
        # Get menu for week
        menu = db.get_menu_by_week_start(week_start)
        
        if not menu:
            return jsonify({
                'success': False,
                'error': 'No hay menú disponible para esta semana'
            }), 404
        
        # Parse menu data
        menu_data = menu['menu_data'] if isinstance(menu['menu_data'], dict) else json.loads(menu['menu_data'])
        
        # Get family profiles
        adults = db.get_all_adults()
        children = db.get_all_children()
        
        # Generate shopping list using menu data
        # Extract ingredients from menu and create shopping list structure
        shopping_list = {
            'categories': {},
            'total_items': 0,
            'week_start': week_start
        }
        
        # Simple shopping list generation from menu
        all_ingredients = []
        
        # Extract ingredients from adult menu
        if 'menu_adultos' in menu_data and 'dias' in menu_data['menu_adultos']:
            for day_data in menu_data['menu_adultos']['dias'].values():
                for meal_data in day_data.values():
                    if isinstance(meal_data, dict) and 'ingredientes' in meal_data:
                        all_ingredients.extend(meal_data['ingredientes'])
        
        # Extract ingredients from children menu
        if 'menu_ninos' in menu_data and 'dias' in menu_data['menu_ninos']:
            for day_data in menu_data['menu_ninos']['dias'].values():
                for meal_data in day_data.values():
                    if isinstance(meal_data, dict) and 'ingredientes' in meal_data:
                        all_ingredients.extend(meal_data['ingredientes'])
        
        # Group ingredients by category
        categories = {}
        for ingredient in all_ingredients:
            if isinstance(ingredient, dict):
                category = ingredient.get('categoria', 'Otros')
                name = ingredient.get('nombre', 'Ingrediente')
                quantity = ingredient.get('cantidad', '1')
                
                if category not in categories:
                    categories[category] = []
                
                categories[category].append({
                    'name': name,
                    'quantity': quantity,
                    'unit': ingredient.get('unidad', 'unidades')
                })
        
        shopping_list['categories'] = categories
        shopping_list['total_items'] = sum(len(items) for items in categories.values())
        
        return jsonify({
            'success': True,
            'data': shopping_list
        })
            
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Error al obtener lista de compras: {str(e)}'
        }), 500

@app.route('/api/menu/all', methods=['GET'])
def get_all_menus():
    """Get all available weekly menus"""
    try:
        menus = db.get_all_menus()
        
        return jsonify({
            'success': True,
            'data': menus,
            'count': len(menus)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/menu/rate-day', methods=['POST'])
def rate_menu_day():
    """Rate a specific day menu (adults or children)"""
    try:
        data = request.json
        menu_id = data.get('menu_id')
        week_start_date = data.get('week_start_date')
        day_name = data.get('day_name')
        menu_type = data.get('menu_type')  # 'adultos' or 'ninos'
        rating = data.get('rating')
        
        if not all([menu_id, week_start_date, day_name, menu_type, rating]):
            return jsonify({
                'success': False,
                'error': 'Faltan parámetros requeridos'
            }), 400
        
        if menu_type not in ['adultos', 'ninos']:
            return jsonify({
                'success': False,
                'error': 'menu_type debe ser "adultos" o "ninos"'
            }), 400
        
        if rating < 1 or rating > 5:
            return jsonify({
                'success': False,
                'error': 'Rating debe estar entre 1 y 5'
            }), 400
        
        success = db.rate_menu_day(menu_id, week_start_date, day_name, menu_type, rating)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Rating guardado correctamente'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Error al guardar el rating'
            }), 400
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/menu/get-day-rating', methods=['GET'])
def get_menu_day_rating():
    """Get rating for a specific day menu"""
    try:
        menu_id = request.args.get('menu_id', type=int)
        day_name = request.args.get('day_name')
        menu_type = request.args.get('menu_type')
        
        if not all([menu_id, day_name, menu_type]):
            return jsonify({
                'success': False,
                'error': 'Faltan parámetros requeridos'
            }), 400
        
        rating = db.get_menu_day_rating(menu_id, day_name, menu_type)
        
        return jsonify({
            'success': True,
            'data': {
                'rating': rating
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/menu/regenerate-meal', methods=['POST'])
def regenerate_individual_meal():
    """Regenerate a specific meal for a specific day"""
    try:
        data = request.json
        week_start_date = data.get('week_start_date')
        day_index = data.get('day_index')
        day_name = data.get('day_name')
        meal_type = data.get('meal_type')  # 'desayuno', 'comida', 'merienda', 'cena'
        current_menu_data = data.get('current_menu_data')
        
        if not all([week_start_date, day_name is not None, day_index is not None, meal_type]):
            return jsonify({
                'success': False,
                'error': 'Faltan parámetros requeridos'
            }), 400
        
        # Get current menu
        menu = db.get_menu_by_week_start(week_start_date)
        if not menu:
            return jsonify({
                'success': False,
                'error': 'Menú no encontrado'
            }), 404
        
        # Get family profiles
        adults = db.get_all_adults()
        children = db.get_all_children()
        
        if not adults and not children:
            return jsonify({
                'success': False,
                'error': 'Debes añadir al menos un perfil familiar primero'
            }), 400
        
        # Get recipes
        recipes = db.get_all_recipes()
        
        # Get menu preferences
        menu_prefs = db.get_menu_preferences()
        preferences = {
            'include_weekend': menu_prefs.get('include_weekend', True),
            'include_breakfast': menu_prefs.get('include_breakfast', True),
            'include_lunch': menu_prefs.get('include_lunch', True),
            'include_dinner': menu_prefs.get('include_dinner', True),
            'excluded_days': menu_prefs.get('excluded_days', [])
        }
        
        # Get historical ratings for learning
        historical_ratings = db.get_all_menu_ratings(limit=30)
        
        # Generate menu for single meal
        gen = get_menu_generator()
        
        # Start with existing menu data
        menu_data = menu['menu_data'] if isinstance(menu['menu_data'], dict) else json.loads(menu['menu_data'])
        
        # Determine target group (adultos or ninos) based on current day data
        target_group = None
        if (menu_data.get('menu_adultos', {}).get('dias', {}).get(day_name, {}).get(meal_type)):
            target_group = 'adultos'
        elif (menu_data.get('menu_ninos', {}).get('dias', {}).get(day_name, {}).get(meal_type)):
            target_group = 'ninos'
        
        if not target_group:
            return jsonify({
                'success': False,
                'error': f'No se encontró la comida {meal_type} para el día {day_name}'
            }), 404
        
        # Generate for the specific group
        if target_group == 'adultos':
            result = gen.generate_single_day_menu(
                adults=adults,
                children=[],
                recipes=recipes,
                preferences=preferences,
                day_name=day_name,
                menu_type='adultos',
                specific_meal=meal_type,  # Only generate this specific meal
                historical_ratings=historical_ratings
            )
            
            if result['success'] and 'day_menu' in result and meal_type in result['day_menu']:
                if 'menu_adultos' not in menu_data:
                    menu_data['menu_adultos'] = {'dias': {}}
                if 'dias' not in menu_data['menu_adultos']:
                    menu_data['menu_adultos']['dias'] = {}
                if day_name not in menu_data['menu_adultos']['dias']:
                    menu_data['menu_adultos']['dias'][day_name] = {}
                menu_data['menu_adultos']['dias'][day_name][meal_type] = result['day_menu'][meal_type]
        
        elif target_group == 'ninos':
            result = gen.generate_single_day_menu(
                adults=[],
                children=children,
                recipes=recipes,
                preferences=preferences,
                day_name=day_name,
                menu_type='ninos',
                specific_meal=meal_type,  # Only generate this specific meal
                historical_ratings=historical_ratings
            )
            
            if result['success'] and 'day_menu' in result and meal_type in result['day_menu']:
                if 'menu_ninos' not in menu_data:
                    menu_data['menu_ninos'] = {'dias': {}}
                if 'dias' not in menu_data['menu_ninos']:
                    menu_data['menu_ninos']['dias'] = {}
                if day_name not in menu_data['menu_ninos']['dias']:
                    menu_data['menu_ninos']['dias'][day_name] = {}
                menu_data['menu_ninos']['dias'][day_name][meal_type] = result['day_menu'][meal_type]
        
        # Save updated menu
        metadata = menu.get('metadata', {})
        if isinstance(metadata, str):
            try:
                metadata = json.loads(metadata)
            except:
                metadata = {}
        
        # Update metadata
        metadata['last_regenerated_meal'] = f'{day_name}_{meal_type}'
        metadata['last_regenerated_date'] = datetime.now().isoformat()
        
        db.save_weekly_menu(week_start_date, menu_data, metadata)
        
        return jsonify({
            'success': True,
            'message': f'{meal_type} regenerado para {day_name}',
            'data': {
                'menu_data': menu_data
            }
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/menu/regenerate-day', methods=['POST'])
def regenerate_menu_day():
    """Regenerate menu for a specific day (both adults and children)"""
    try:
        data = request.json
        week_start_date = data.get('week_start_date')
        day_index = data.get('day_index')
        day_name = data.get('day_name')
        current_menu_data = data.get('current_menu_data')
        
        if not all([week_start_date, day_name is not None, day_index is not None]):
            return jsonify({
                'success': False,
                'error': 'Faltan parámetros requeridos'
            }), 400
        
        # Get current menu
        menu = db.get_menu_by_week_start(week_start_date)
        if not menu:
            return jsonify({
                'success': False,
                'error': 'Menú no encontrado'
            }), 404
        
        # Get family profiles
        adults = db.get_all_adults()
        children = db.get_all_children()
        
        if not adults and not children:
            return jsonify({
                'success': False,
                'error': 'Debes añadir al menos un perfil familiar primero'
            }), 400
        
        # Get recipes
        recipes = db.get_all_recipes()
        
        # Get menu preferences
        menu_prefs = db.get_menu_preferences()
        preferences = {
            'include_weekend': menu_prefs.get('include_weekend', True),
            'include_breakfast': menu_prefs.get('include_breakfast', True),
            'include_lunch': menu_prefs.get('include_lunch', True),
            'include_dinner': menu_prefs.get('include_dinner', True),
            'excluded_days': menu_prefs.get('excluded_days', [])
        }
        
        # Get historical ratings for learning
        historical_ratings = db.get_all_menu_ratings(limit=30)
        
        # Generate menu for single day for both adults and children
        gen = get_menu_generator()
        
        # Start with existing menu data
        menu_data = menu['menu_data'] if isinstance(menu['menu_data'], dict) else json.loads(menu['menu_data'])
        
        # Generate for adults if they exist
        if adults:
            result_adults = gen.generate_single_day_menu(
                adults=adults,
                children=[],  # Only adults
                recipes=recipes,
                preferences=preferences,
                day_name=day_name,
                menu_type='adultos',
                historical_ratings=historical_ratings
            )
            
            if result_adults['success']:
                if 'menu_adultos' not in menu_data:
                    menu_data['menu_adultos'] = {'dias': {}}
                if 'dias' not in menu_data['menu_adultos']:
                    menu_data['menu_adultos']['dias'] = {}
                menu_data['menu_adultos']['dias'][day_name] = result_adults['day_menu']
        
        # Generate for children if they exist
        if children:
            result_children = gen.generate_single_day_menu(
                adults=[],  # Only children
                children=children,
                recipes=recipes,
                preferences=preferences,
                day_name=day_name,
                menu_type='ninos',
                historical_ratings=historical_ratings
            )
            
            if result_children['success']:
                if 'menu_ninos' not in menu_data:
                    menu_data['menu_ninos'] = {'dias': {}}
                if 'dias' not in menu_data['menu_ninos']:
                    menu_data['menu_ninos']['dias'] = {}
                menu_data['menu_ninos']['dias'][day_name] = result_children['day_menu']
        
        # Save updated menu
        metadata = menu.get('metadata', {})
        if isinstance(metadata, str):
            try:
                metadata = json.loads(metadata)
            except:
                metadata = {}
        
        # Update metadata
        metadata['last_regenerated_day'] = day_name
        metadata['last_regenerated_date'] = datetime.now().isoformat()
        
        db.save_weekly_menu(week_start_date, menu_data, metadata)
        
        return jsonify({
            'success': True,
            'message': f'Menú regenerado para {day_name}',
            'data': {
                'menu_data': menu_data
            }
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/family/summary', methods=['GET'])
def family_summary():
    """Get family summary"""
    adults = db.get_all_adults()
    children = db.get_all_children()
    
    return jsonify({
        'success': True,
        'data': {
            'adults': adults,
            'children': children,
            'total_members': len(adults) + len(children)
        }
    })

# ==================== SETTINGS API ====================

@app.route('/api/settings', methods=['GET'])
def get_settings():
    """Get current settings (API key status and menu preferences)"""
    api_key = os.getenv('ANTHROPIC_API_KEY', '')
    menu_prefs = db.get_menu_preferences()
    
    return jsonify({
        'success': True,
        'data': {
            'has_api_key': bool(api_key and api_key != 'sk-ant-api03-your-key-here'),
            'api_key_preview': f"{api_key[:15]}..." if api_key and len(api_key) > 15 else None,
            'port': int(os.getenv('PORT', 7000)),
            'mode': os.getenv('FLASK_ENV', 'development'),
            'menu_preferences': menu_prefs
        }
    })

@app.route('/api/settings', methods=['POST'])
def save_settings():
    """Save settings (API key and/or menu preferences)"""
    try:
        data = request.json or {}
        
        # Debug logging
        print(f"[Settings] Received data keys: {list(data.keys())}")
        print(f"[Settings] Has anthropic_api_key: {'anthropic_api_key' in data}")
        print(f"[Settings] Has menu_preferences: {'menu_preferences' in data}")
        
        # Handle API key if provided
        api_key = data.get('anthropic_api_key', '').strip() if data.get('anthropic_api_key') else ''
        print(f"[Settings] API key provided: {bool(api_key)}, length: {len(api_key) if api_key else 0}")
        
        if api_key:
            if not api_key.startswith('sk-ant-'):
                return jsonify({
                    'success': False,
                    'error': 'La API key de Anthropic debe comenzar con "sk-ant-"'
                }), 400
            
            # Read existing .env file or create from example
            env_path = '.env'
            env_example_path = '.env.example'
            
            env_content = ''
            if os.path.exists(env_path):
                with open(env_path, 'r', encoding='utf-8') as f:
                    env_content = f.read()
            elif os.path.exists(env_example_path):
                with open(env_example_path, 'r', encoding='utf-8') as f:
                    env_content = f.read()
            else:
                # Create basic .env structure
                env_content = """# k[AI]tchen - Environment Variables
ANTHROPIC_API_KEY=
SECRET_KEY=
DATABASE_URL=
FLASK_ENV=development
PORT=7000
"""
            
            # Update or add ANTHROPIC_API_KEY
            lines = env_content.split('\n')
            updated_lines = []
            api_key_found = False
            
            for line in lines:
                if line.strip().startswith('ANTHROPIC_API_KEY='):
                    updated_lines.append(f'ANTHROPIC_API_KEY={api_key}')
                    api_key_found = True
                else:
                    updated_lines.append(line)
            
            if not api_key_found:
                # Add at the beginning if not found
                updated_lines.insert(0, f'ANTHROPIC_API_KEY={api_key}')
            
            # Write back to .env
            with open(env_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(updated_lines))
            
            # Reload environment variables
            from dotenv import load_dotenv
            load_dotenv(override=True)
            
            # Update menu generator if it exists
            global menu_gen
            menu_gen = None  # Force reinitialization
        
        # Handle menu preferences if provided
        menu_preferences = data.get('menu_preferences')
        print(f"[Settings] Menu preferences provided: {bool(menu_preferences)}")
        
        if menu_preferences:
            try:
                print(f"[Settings] Saving menu preferences: {menu_preferences}")
                db.save_menu_preferences(menu_preferences)
                print(f"[Settings] Menu preferences saved successfully")
            except Exception as e:
                print(f"[Settings] Error saving menu preferences: {str(e)}")
                import traceback
                traceback.print_exc()
                return jsonify({
                    'success': False,
                    'error': f'Error al guardar preferencias del menú: {str(e)}'
                }), 400
        
        # Validate that at least one thing was provided
        if not api_key and not menu_preferences:
            print(f"[Settings] Error: Neither API key nor menu preferences provided")
            return jsonify({
                'success': False,
                'error': 'Debes proporcionar al menos una API key o preferencias del menú'
            }), 400
        
        print(f"[Settings] Settings saved successfully")
        
        return jsonify({
            'success': True,
            'message': 'Configuración guardada correctamente.' + (' El servidor necesita reiniciarse para aplicar cambios de API key.' if api_key else '')
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/settings/test', methods=['POST'])
def test_api_key():
    """Test if the API key is valid"""
    try:
        data = request.json
        api_key = data.get('anthropic_api_key', '').strip()
        
        if not api_key:
            return jsonify({
                'success': False,
                'error': 'Proporciona una API key para probar'
            }), 400
        
        # Try to initialize menu generator with the key
        from menu_generator import MenuGenerator
        test_gen = MenuGenerator(api_key)
        
        # Try a simple test (this will make a minimal API call)
        # For now, just check if it initializes without error
        return jsonify({
            'success': True,
            'message': 'API key válida. El formato es correcto.'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error al validar la API key: {str(e)}'
        }), 400

# ==================== CLEANING CAPACITY API ====================

@app.route('/api/cleaning/capacity', methods=['GET'])
def get_cleaning_capacity():
    """Get cleaning capacity settings"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM cleaning_capacity ORDER BY member_type')
        capacities = cursor.fetchall()
        conn.close()
        
        # Convert to dictionary format
        capacity_dict = {}
        for cap in capacities:
            capacity_dict[cap[1]] = {  # member_type is index 1
                'id': cap[0],
                'member_type': cap[1],
                'max_daily_percentage': cap[2],
                'max_weekly_hours': cap[3],
                'task_difficulty_max': cap[4],
                'preferred_areas': json.loads(cap[5]) if cap[5] else [],
                'can_do_complex_tasks': bool(cap[6]),
                'created_at': cap[7],
                'updated_at': cap[8]
            }
        
        return jsonify({
            'success': True,
            'data': capacity_dict
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/cleaning/capacity', methods=['POST'])
def save_cleaning_capacity():
    """Save cleaning capacity settings"""
    try:
        data = request.json
        print(f"[CleaningCapacity] Received capacity settings: {data}")
        
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # Update each capacity type
        for member_type, settings in data.items():
            cursor.execute('''
                UPDATE cleaning_capacity SET 
                max_daily_percentage = ?, max_weekly_hours = ?, task_difficulty_max = ?,
                preferred_areas = ?, can_do_complex_tasks = ?, updated_at = CURRENT_TIMESTAMP
                WHERE member_type = ?
            ''', (
                settings.get('max_daily_percentage', 100),
                settings.get('max_weekly_hours', 40),
                settings.get('task_difficulty_max', 5),
                json.dumps(settings.get('preferred_areas', [])),
                1 if settings.get('can_do_complex_tasks') else 0,
                member_type
            ))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Capacidades de limpieza guardadas correctamente'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ==================== HOUSE CONFIGURATION API ====================

@app.route('/api/house/config', methods=['GET'])
def get_house_config():
    """Get house configuration"""
    try:
        # Get configuration from database
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM house_config ORDER BY id DESC LIMIT 1')
        config = cursor.fetchone()
        conn.close()
        
        if config:
            # Parse config_data from JSON
            import json
            try:
                config_data = json.loads(config[1]) if config[1] else {}
            except:
                config_data = {}
                
            return jsonify({
                'success': True,
                'data': {
                    'id': config[0],
                    'config_data': config_data,
                    'created_at': config[2].isoformat() if config[2] else None,
                    'updated_at': config[3].isoformat() if config[3] else None
                }
            })
        else:
            # Return default configuration if none exists
            default_config = {
                "house_size": "mediana",
                "rooms": ["cocina", "sala", "banos", "dormitorios"],
                "cleaning_frequency": "semanal",
                "residents_count": 5
            }
            return jsonify({
                'success': True,
                'data': {
                    'config_data': default_config
                }
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/house/config', methods=['POST'])
def save_house_config():
    """Save house configuration"""
    try:
        data = request.json
        print(f"[HouseConfig] Received configuration: {data}")
        
        # Get connection and save to database
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # Check if there's already a record
        cursor.execute('SELECT id FROM house_config ORDER BY id DESC LIMIT 1')
        existing = cursor.fetchone()
        
        import json
        config_json = json.dumps(data)
        
        if existing:
            # Update existing record
            cursor.execute('''
                UPDATE house_config SET 
                config_data = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (config_json, existing[0]))
            print(f"[HouseConfig] Updated {cursor.rowcount} rows")
        else:
            # Insert new record
            cursor.execute('''
                INSERT INTO house_config (config_data)
                VALUES (?)
            ''', (config_json,))
            print(f"[HouseConfig] Inserted new record")
        
        # Commit changes
        conn.commit()
        
        # Close connection
        db._close_connection(conn)
        
        return jsonify({
            'success': True,
            'message': 'Configuración guardada correctamente en la base de datos'
        })
            
    except Exception as e:
        print(f"[HouseConfig] Error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/cleaning/generate-smart-plan', methods=['POST'])
def generate_smart_cleaning_plan():
    """
    Genera plan de limpieza personalizado con IA
    basado en configuración de casa
    """
    try:
        # Get house configuration from database
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM house_config ORDER BY id DESC LIMIT 1')
        house_config_record = cursor.fetchone()
        conn.close()
        
        if house_config_record:
            # Parse config_data from JSON
            import json
            try:
                config_data = json.loads(house_config_record[1]) if house_config_record[1] else {}
            except:
                config_data = {}
            
            # Use config_data or defaults
            house_config = {
                'num_habitaciones': config_data.get('num_habitaciones', 3),
                'num_banos': config_data.get('num_banos', 2),
                'num_salas': config_data.get('num_salas', 2),
                'num_cocinas': config_data.get('num_cocinas', 1),
                'superficie_total': config_data.get('superficie_total', 120),
                'tipo_piso': config_data.get('tipo_piso', 'apartamento'),
                'tiene_jardin': config_data.get('tiene_jardin', False),
                'mascotas': config_data.get('mascotas', 'no'),
                'notas_casa': config_data.get('notas_casa', '')
            }
        else:
            # Use defaults if no configuration found
            house_config = {
                'num_habitaciones': 3,
                'num_banos': 2,
                'num_salas': 2,
                'num_cocinas': 1,
                'superficie_total': 120,
                'tipo_piso': 'apartamento',
                'tiene_jardin': False,
                'mascotas': 'no',
                'notas_casa': ''
            }
        
        # Get real family members with their capacities
        adults = db.get_all_adults()
        children = db.get_all_children()
        
        # Get cleaning capacities
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT member_type, max_daily_percentage, max_weekly_hours, task_difficulty_max, preferred_areas, can_do_complex_tasks FROM cleaning_capacity')
        capacities = cursor.fetchall()
        conn.close()
        
        # Convert capacities to dictionary
        capacity_dict = {}
        for cap in capacities:
            capacity_dict[cap[0]] = {
                'max_daily_percentage': cap[1],
                'max_weekly_hours': cap[2],
                'task_difficulty_max': cap[3],
                'preferred_areas': json.loads(cap[4]) if cap[4] else [],
                'can_do_complex_tasks': bool(cap[5])
            }
        
        # Create enhanced family member objects
        family_members = []
        
        # Add adults with capacities
        for adult in adults:
            member_data = {
                'id': adult['id'],
                'nombre': adult['nombre'],
                'edad': adult['edad'],
                'tipo': 'adulto',
                'capacidad': capacity_dict.get('adulto', {}),
                'available_hours': capacity_dict.get('adulto', {}).get('max_weekly_hours', 40),
                'max_difficulty': capacity_dict.get('adulto', {}).get('task_difficulty_max', 5)
            }
            family_members.append(member_data)
        
        # Add children with capacities (adjust based on age)
        for child in children:
            child_capacity = capacity_dict.get('niño', {}).copy()
            
            # Adjust capacity based on age
            if child['edad'] <= 6:
                # Very young children - only basic tasks
                child_capacity['task_difficulty_max'] = min(child_capacity.get('task_difficulty_max', 2), 1)
                child_capacity['max_weekly_hours'] = min(child_capacity.get('max_weekly_hours', 10), 5)
            elif child['edad'] <= 10:
                # Young children - basic to intermediate tasks
                child_capacity['task_difficulty_max'] = min(child_capacity.get('task_difficulty_max', 2), 2)
                child_capacity['max_weekly_hours'] = min(child_capacity.get('max_weekly_hours', 10), 8)
            elif child['edad'] <= 14:
                # Pre-teens - intermediate tasks
                child_capacity['task_difficulty_max'] = min(child_capacity.get('task_difficulty_max', 2), 3)
                child_capacity['max_weekly_hours'] = min(child_capacity.get('max_weekly_hours', 10), 12)
            
            member_data = {
                'id': child['id'],
                'nombre': child['nombre'],
                'edad': child['edad'],
                'tipo': 'niño',
                'capacidad': child_capacity,
                'available_hours': child_capacity.get('max_weekly_hours', 10),
                'max_difficulty': child_capacity.get('task_difficulty_max', 2)
            }
            family_members.append(member_data)
        
        print(f"[SmartPlan] Family members loaded: {len(family_members)} total")
        for member in family_members:
            print(f"  - {member['nombre']} ({member['edad']} años, {member['tipo']}): max_difficulty={member['max_difficulty']}, hours={member['available_hours']}")
        
        # Generate smart plan based on actual house configuration
        tasks = []
        
        # Bathroom tasks based on actual number
        for i in range(house_config['num_banos']):
            tasks.append({
                'nombre': f'Limpiar baño {"principal" if i == 0 else f"secundario {i+1}"}',
                'area': 'Baño',
                'frecuencia': 'semanal',
                'dificultad': 4,
                'tiempo_estimado': 30  # Reduced from 45 to 30 minutes
            })
        
        # Kitchen tasks based on actual number
        for i in range(house_config['num_cocinas']):
            tasks.append({
                'nombre': f'Limpiar cocina {"principal" if i == 0 else f"secundaria {i+1}"}',
                'area': 'Cocina',
                'frecuencia': 'diaria',
                'dificultad': 3,
                'tiempo_estimado': 30
            })
        
        # Room tasks based on actual number
        for i in range(house_config['num_habitaciones']):
            tasks.append({
                'nombre': f'Ordenar habitación {i+1}',
                'area': 'Habitacion',
                'frecuencia': 'diaria',
                'dificultad': 1,
                'tiempo_estimado': 15
            })
        
        # Living room tasks
        for i in range(house_config['num_salas']):
            tasks.append({
                'nombre': f'Limpiar sala {"principal" if i == 0 else f"secundaria {i+1}"}',
                'area': 'Sala',
                'frecuencia': 'semanal',
                'dificultad': 2,
                'tiempo_estimado': 60
            })
        
        # Pet tasks if applicable
        if house_config['mascotas'] and house_config['mascotas'].lower() != 'no':
            tasks.append({
                'nombre': f'Tareas de cuidado para {house_config["mascotas"]}',
                'nombre': 'Mantenimiento de jardín',
                'area': 'Exterior',
                'frecuencia': 'quincenal',
                'tiempo_estimado': 120,
                'dificultad': 5,
                'asignado_a': 'adultos'
            })
        
        # Adjust frequency based on surface area
        frequency_multiplier = 1.0
        if house_config['superficie_total'] > 200:
            frequency_multiplier = 1.3
        elif house_config['superficie_total'] > 100:
            frequency_multiplier = 1.1
        
        # Apply frequency multiplier
        for task in tasks:
            if task['frecuencia'] == 'semanal':
                task['frecuencia'] = f'semanal (ajustada x{frequency_multiplier})'
        
        # Smart task assignment based on member capacities and age
        assigned_tasks = []
        
        print(f"[SmartPlan] Starting assignment for {len(tasks)} tasks to {len(family_members)} members")
        
        for task in tasks:
            print(f"[SmartPlan] Processing task: {task['nombre']} (area: {task['area']}, difficulty: {task['dificultad']})")
            # Find suitable members for this task
            suitable_members = []
            
            for member in family_members:
                # Simple assignment logic
                can_do_task = task['dificultad'] <= member['max_difficulty']
                hours_used = sum(t['tiempo_estimado'] for t in assigned_tasks if t.get('asignado_a_id') == member['id']) / 60
                has_hours = hours_used < member['available_hours']
                
                print(f"[SmartPlan] {member['nombre']} (edad: {member['edad']}, tipo: {member['tipo']}): can_do={can_do_task}, hours_used={hours_used:.1f}h, available={member['available_hours']}h, has_hours={has_hours}")
                
                if can_do_task and has_hours:
                    suitable_members.append(member)
            
            print(f"[SmartPlan] Suitable members for {task['nombre']}: {[m['nombre'] for m in suitable_members]}")
            
            # Assign to the most suitable member (least loaded)
            if suitable_members:
                # Sort by current load (hours used)
                suitable_members.sort(key=lambda m: sum(t['tiempo_estimado'] for t in assigned_tasks if t.get('asignado_a_id') == m['id']))
                assigned_member = suitable_members[0]
                
                task_with_assignment = task.copy()
                task_with_assignment['asignado_a'] = assigned_member['nombre']
                task_with_assignment['asignado_a_id'] = assigned_member['id']
                task_with_assignment['asignado_a_edad'] = assigned_member['edad']
                task_with_assignment['asignado_a_tipo'] = assigned_member['tipo']
                assigned_tasks.append(task_with_assignment)
                
                print(f"[SmartPlan] ✓ Task '{task['nombre']}' assigned to {assigned_member['nombre']} ({assigned_member['edad']} años)")
            else:
                # Unassigned task
                task_with_assignment = task.copy()
                task_with_assignment['asignado_a'] = 'Sin asignar'
                task_with_assignment['asignado_a_id'] = None
                assigned_tasks.append(task_with_assignment)
                print(f"[SmartPlan] ✗ Task '{task['nombre']}' could not be assigned (no suitable member)")
            
            print(f"[SmartPlan] ---")
        
        # Create distribution summary by member
        distribution_by_member = {}
        for task in assigned_tasks:
            if task['asignado_a'] != 'Sin asignar':
                member_name = task['asignado_a']
                if member_name not in distribution_by_member:
                    distribution_by_member[member_name] = {
                        'tasks': [],
                        'total_hours': 0,
                        'total_difficulty': 0,
                        'edad': task['asignado_a_edad'],
                        'tipo': task['asignado_a_tipo']
                    }
                
                distribution_by_member[member_name]['tasks'].append(task['nombre'])
                distribution_by_member[member_name]['total_hours'] += task.get('tiempo_estimado', 0) / 60  # Convert minutes to hours
                distribution_by_member[member_name]['total_difficulty'] += task.get('dificultad', 0)
        
        # Calculate percentages
        total_hours = sum(member['total_hours'] for member in distribution_by_member.values())
        for member_name, member_data in distribution_by_member.items():
            if total_hours > 0:
                member_data['percentage'] = round((member_data['total_hours'] / total_hours) * 100, 1)
            else:
                member_data['percentage'] = 0
        
        return jsonify({
            'success': True,
            'plan': {
                'tasks': assigned_tasks,
                'distribution': distribution_by_member,
                'house_config_used': house_config,
                'total_tasks': len(assigned_tasks),
                'assigned_tasks': len([t for t in assigned_tasks if t['asignado_a'] != 'Sin asignar']),
                'unassigned_tasks': len([t for t in assigned_tasks if t['asignado_a'] == 'Sin asignar']),
                'estimated_weekly_hours': sum(task['tiempo_estimado'] for task in assigned_tasks) / 60,
                'family_members': family_members
            }
        })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ==================== CLEANING API ====================

@app.route('/api/cleaning/tasks', methods=['GET'])
def get_cleaning_tasks():
    """Get all cleaning tasks"""
    try:
        tasks = db.get_all_cleaning_tasks()
        return jsonify({
            'success': True,
            'data': tasks,
            'count': len(tasks)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error al obtener tareas: {str(e)}'
        }), 500

@app.route('/api/cleaning/tasks', methods=['POST'])
def add_cleaning_task():
    """Add a new cleaning task"""
    try:
        task_data = request.get_json()
        task_id = db.add_cleaning_task(task_data)
        return jsonify({
            'success': True,
            'task_id': task_id,
            'message': 'Tarea creada exitosamente'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/cleaning/schedule/<week_start>', methods=['GET'])
def get_cleaning_schedule(week_start):
    """Get cleaning schedule for a specific week"""
    try:
        schedule_result = cleaning_manager.get_weekly_schedule(week_start)
        return jsonify(schedule_result)
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error al obtener horario: {str(e)}'
        }), 500

@app.route('/api/cleaning/assign', methods=['POST'])
def assign_cleaning_tasks():
    """Assign cleaning tasks for a week"""
    try:
        data = request.get_json()
        week_start = data.get('week_start')
        result = cleaning_manager.assign_tasks_for_week(week_start)
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error al asignar tareas: {str(e)}'
        }), 500

@app.route('/api/cleaning/complete/<int:assignment_id>', methods=['POST'])
def complete_cleaning_task(assignment_id):
    """Mark a cleaning task as completed"""
    try:
        data = request.get_json()
        completado = data.get('completado', True)
        notas = data.get('notas')
        success = cleaning_manager.update_task_completion(assignment_id, completado, notas)
        return jsonify({
            'success': success,
            'message': 'Tarea actualizada exitosamente' if success else 'Error al actualizar tarea'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error al actualizar tarea: {str(e)}'
        }), 500

@app.route('/api/cleaning/preferences', methods=['GET'])
def get_cleaning_preferences():
    """Get cleaning preferences"""
    try:
        preferences = db.get_cleaning_preferences()
        return jsonify({
            'success': True,
            'preferences': preferences
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error al obtener preferencias: {str(e)}'
        }), 500

@app.route('/api/cleaning/preferences', methods=['POST'])
def save_cleaning_preferences():
    """Save cleaning preferences"""
    try:
        preferences = request.get_json()
        success = db.save_cleaning_preferences(preferences)
        return jsonify({
            'success': success,
            'message': 'Preferencias guardadas exitosamente' if success else 'Error al guardar preferencias'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error al guardar preferencias: {str(e)}'
        }), 500

@app.route('/api/cleaning/calendar/assign', methods=['POST'])
def assign_calendar_cleaning():
    """Assign cleaning tasks to calendar dates"""
    try:
        data = request.get_json()
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        
        if not start_date or not end_date:
            return jsonify({
                'success': False,
                'error': 'Se requieren fechas de inicio y fin'
            }), 400
        
        result = cleaning_manager.assign_tasks_to_calendar_dates(start_date, end_date)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error al asignar tareas de calendario: {str(e)}'
        }), 500

@app.route('/api/cleaning/calendar/<start_date>/<end_date>', methods=['GET'])
def get_calendar_cleaning(start_date, end_date):
    """Get cleaning schedule for a date range"""
    try:
        result = cleaning_manager.get_calendar_schedule(start_date, end_date)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error al obtener horario de calendario: {str(e)}'
        }), 500

@app.route('/api/cleaning/calendar/day/<date_str>', methods=['GET'])
def get_day_cleaning(date_str):
    """Get cleaning tasks for a specific day"""
    try:
        assignments = db.get_calendar_cleaning_assignments(date_str)
        return jsonify({
            'success': True,
            'date': date_str,
            'assignments': assignments,
            'total_tasks': len(assignments)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error al obtener tareas del día: {str(e)}'
        }), 500

@app.route('/api/cleaning/initialize', methods=['POST'])
def initialize_cleaning_tasks():
    """Initialize default cleaning tasks"""
    try:
        success = cleaning_manager.initialize_default_tasks()
        return jsonify({
            'success': success,
            'message': 'Tareas inicializadas exitosamente' if success else 'Error al inicializar tareas'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error al inicializar tareas: {str(e)}'
        }), 500

# ==================== HEALTH CHECK ====================

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat()
    })

# ==================== TEMPORARY: GET API KEY FOR .ENV ====================
# This endpoint is only for local development to save API key to .env file
# Remove or secure this endpoint in production

@app.route('/api/temp/get-api-key', methods=['GET'])
def temp_get_api_key():
    """Temporary endpoint to get full API key for saving to .env (LOCAL ONLY)"""
    # Only allow from localhost
    if request.remote_addr not in ['127.0.0.1', '::1', 'localhost']:
        return jsonify({
            'success': False,
            'error': 'This endpoint is only available from localhost'
        }), 403
    
    api_key = os.getenv('ANTHROPIC_API_KEY', '')
    if not api_key:
        return jsonify({
            'success': False,
            'error': 'API key not found in environment'
        }), 404
    
    return jsonify({
        'success': True,
        'api_key': api_key
    })

@app.route('/api/temp/save-api-key-to-env', methods=['POST'])
def temp_save_api_key_to_env():
    """Temporary endpoint to save API key from memory to .env file (LOCAL ONLY)"""
    # Only allow from localhost
    if request.remote_addr not in ['127.0.0.1', '::1', 'localhost']:
        return jsonify({
            'success': False,
            'error': 'This endpoint is only available from localhost'
        }), 403
    
    api_key = os.getenv('ANTHROPIC_API_KEY', '')
    if not api_key:
        return jsonify({
            'success': False,
            'error': 'API key not found in environment. The server may need to be restarted with the key in .env'
        }), 404
    
    # Read existing .env file
    env_path = '.env'
    env_content = ''
    
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            env_content = f.read()
    else:
        # Create basic structure
        env_content = """# k[AI]tchen - Environment Variables
ANTHROPIC_API_KEY=
SECRET_KEY=dda99c73a04fca83e4a492b2310fea5c90a957423faf37118270dd3b8b922e62
DATABASE_URL=
FLASK_ENV=development
PORT=7000
CORS_ORIGINS=*
"""
    
    # Update or add ANTHROPIC_API_KEY
    lines = env_content.split('\n')
    updated_lines = []
    api_key_found = False
    
    for line in lines:
        if line.strip().startswith('ANTHROPIC_API_KEY='):
            updated_lines.append(f'ANTHROPIC_API_KEY={api_key}')
            api_key_found = True
        else:
            updated_lines.append(line)
    
    if not api_key_found:
        # Add at the beginning if not found
        updated_lines.insert(0, f'ANTHROPIC_API_KEY={api_key}')
    
    # Write back to .env
    try:
        with open(env_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(updated_lines))
        
        return jsonify({
            'success': True,
            'message': 'API key guardada correctamente en .env',
            'preview': f"{api_key[:20]}..."
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error al guardar en .env: {str(e)}'
        }), 500

if __name__ == '__main__':
    try:
        # Create templates directory if it doesn't exist
        os.makedirs('templates', exist_ok=True)
        os.makedirs('static', exist_ok=True)
        
        # Get port from environment (Railway sets this)
        port = int(os.getenv('PORT', 7000))
        
        # Determine if running in production
        is_production = os.getenv('FLASK_ENV') == 'production'
        
        # Run the app
        # Use ASCII-safe characters for Windows compatibility
        print("\n" + "="*60)
        print("SISTEMA DE GESTION DE MENUS FAMILIARES")
        print("="*60)
        
        if is_production:
            print("\n[PRODUCTION] Running in PRODUCTION mode")
            print(f"Port: {port}")
        else:
            print("\n[DEV] Running in DEVELOPMENT mode")
            print(f"\nInterfaz de administracion: http://localhost:{port}")
            print(f"Vista de TV: http://localhost:{port}/tv")
            print(f"Vista de TV (NUEVA): http://localhost:{port}/tv2")
            print("\n[WARNING] Recuerda configurar ANTHROPIC_API_KEY en el archivo .env")
        
        print("="*60 + "\n")
        
        app.run(
            debug=False,  
            host='0.0.0.0',
            port=port,
            use_reloader=False  # Disable reloader to prevent crashes
        )
    except KeyboardInterrupt:
        print("\n\n[INFO] Servidor detenido por el usuario")
    except Exception as e:
        print(f"\n\n[ERROR] ERROR CRITICO: {str(e)}")
        print(f"Tipo de error: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        print("\n[WARNING] El servidor se ha detenido debido a un error.")
        print("Revisa los mensajes de error arriba para mas detalles.")
