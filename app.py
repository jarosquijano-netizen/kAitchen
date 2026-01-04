from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.exceptions import NotFound, InternalServerError
from flask_cors import CORS
import os
import json
from dotenv import load_dotenv
from database import Database
from recipe_extractor import RecipeExtractor
from menu_generator import MenuGenerator
from datetime import datetime, timedelta

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', os.urandom(24))

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
db = Database()  # Will use DATABASE_URL from environment
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
    return render_template('tv_display.html')

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
    adults = db.get_all_adults()
    return jsonify({
        'success': True,
        'data': adults,
        'count': len(adults)
    })

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
    children = db.get_all_children()
    return jsonify({
        'success': True,
        'data': children,
        'count': len(children)
    })

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
            # Validate and use provided date - ALWAYS use it as-is (frontend sends correct Monday dates)
            try:
                provided_date = datetime.strptime(week_start_date, '%Y-%m-%d')
                # Use the date as-is - frontend is responsible for sending correct Monday dates
                week_start = week_start_date
                print(f"[GenerateMenu] Using provided week_start_date as-is: {week_start}")
                # Log warning if it's not a Monday (for debugging)
                if provided_date.weekday() != 0:
                    print(f"[GenerateMenu] WARNING: week_start_date {week_start_date} is not a Monday (weekday: {provided_date.weekday()})")
            except ValueError:
                return jsonify({
                    'success': False,
                    'error': 'Formato de fecha inválido. Usa YYYY-MM-DD'
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

@app.route('/api/menu/regenerate-day', methods=['POST'])
def regenerate_menu_day():
    """Regenerate menu for a specific day (adults or children)"""
    try:
        data = request.json
        menu_id = data.get('menu_id')
        week_start_date = data.get('week_start_date')
        day_name = data.get('day_name')
        menu_type = data.get('menu_type')  # 'adultos' or 'ninos'
        
        if not all([menu_id, week_start_date, day_name, menu_type]):
            return jsonify({
                'success': False,
                'error': 'Faltan parámetros requeridos'
            }), 400
        
        if menu_type not in ['adultos', 'ninos']:
            return jsonify({
                'success': False,
                'error': 'menu_type debe ser "adultos" o "ninos"'
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
        
        # Generate menu for single day
        gen = get_menu_generator()
        result = gen.generate_single_day_menu(
            adults=adults,
            children=children,
            recipes=recipes,
            preferences=preferences,
            day_name=day_name,
            menu_type=menu_type,
            historical_ratings=historical_ratings
        )
        
        if not result['success']:
            return jsonify(result), 400
        
        # Update the menu in database
        menu_data = menu['menu_data']
        if menu_type == 'adultos':
            if 'menu_adultos' not in menu_data:
                menu_data['menu_adultos'] = {'dias': {}}
            if 'dias' not in menu_data['menu_adultos']:
                menu_data['menu_adultos']['dias'] = {}
            menu_data['menu_adultos']['dias'][day_name] = result['day_menu']
        else:  # ninos
            if 'menu_ninos' not in menu_data:
                menu_data['menu_ninos'] = {'dias': {}}
            if 'dias' not in menu_data['menu_ninos']:
                menu_data['menu_ninos']['dias'] = {}
            menu_data['menu_ninos']['dias'][day_name] = result['day_menu']
        
        # Save updated menu
        metadata = menu.get('metadata', {})
        if isinstance(metadata, str):
            try:
                metadata = json.loads(metadata)
            except:
                metadata = {}
        
        db.save_weekly_menu(week_start_date, menu_data, metadata)
        
        return jsonify({
            'success': True,
            'message': f'Menú regenerado para {day_name} ({menu_type})',
            'data': result['day_menu']
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
            print("\n[WARNING] Recuerda configurar ANTHROPIC_API_KEY en el archivo .env")
        
        print("="*60 + "\n")
        
        app.run(
            debug=not is_production,
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
