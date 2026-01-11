import anthropic
import os
import json
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import httpx
import re

def repair_json_string(json_str: str) -> str:
    """
    Repair JSON string by fixing common issues like unescaped quotes.
    Uses a state machine to properly escape quotes inside string values.
    """
    result = []
    i = 0
    in_string = False
    escape_next = False
    
    while i < len(json_str):
        char = json_str[i]
        
        if escape_next:
            result.append(char)
            escape_next = False
        elif char == '\\':
            result.append(char)
            escape_next = True
        elif char == '"':
            # Check if this is the start or end of a string
            # Look ahead to see if this might be inside a string value
            if in_string:
                # We're inside a string, check if this quote should be escaped
                # Look ahead to see if there's a colon or comma after potential closing quote
                lookahead = i + 1
                while lookahead < len(json_str) and json_str[lookahead] in ' \t\n\r':
                    lookahead += 1
                
                if lookahead < len(json_str):
                    next_char = json_str[lookahead]
                    # If next char is : or , or } or ], this might be a closing quote
                    # But if it's a letter or other char, it's likely an unescaped quote inside the string
                    if next_char in ':,\n}]':
                        # This looks like a closing quote
                        result.append(char)
                        in_string = False
                    else:
                        # This looks like an unescaped quote inside the string
                        result.append('\\"')
                else:
                    # End of string, this is a closing quote
                    result.append(char)
                    in_string = False
            else:
                # Starting a new string
                result.append(char)
                in_string = True
        else:
            result.append(char)
        
        i += 1
    
    return ''.join(result)


class MenuGenerator:
    """AI-powered menu generator using Claude"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("API key de Anthropic no encontrada. Configura ANTHROPIC_API_KEY")
        
        # Create HTTP client with timeout
        timeout = httpx.Timeout(300.0, connect=10.0)  # 5 minutes total, 10 seconds to connect
        http_client = httpx.Client(timeout=timeout)
        
        self.client = anthropic.Anthropic(
            api_key=self.api_key,
            http_client=http_client
        )
    
    def generate_weekly_menu(self, 
                            adults: List[Dict], 
                            children: List[Dict],
                            recipes: Optional[List[Dict]] = None,
                            preferences: Optional[Dict] = None,
                            day_settings: Optional[Dict] = None,
                            highly_rated_menus: Optional[List[Dict]] = None,
                            historical_ratings: Optional[List[Dict]] = None) -> Dict:
        """
        Generate a personalized weekly menu for the family
        
        Args:
            adults: List of adult profiles
            children: List of children profiles
            recipes: Optional list of available recipes
            preferences: Optional additional preferences (budget, cooking time, etc.)
            day_settings: Optional dict with cooking settings per day
                         Example: {"lunes": {"meals": ["desayuno", "cena"], "no_cooking": False}}
        
        Returns:
            Dictionary with weekly menu and recommendations
        """
        
        # Build the prompt with family information
        prompt = self._build_menu_prompt(adults, children, recipes, preferences, day_settings, historical_ratings)
        
        # Call Claude API
        try:
            print(f"[MenuGenerator] Iniciando generación de menú...")
            print(f"[MenuGenerator] Perfiles: {len(adults)} adultos, {len(children)} niños")
            print(f"[MenuGenerator] Recetas disponibles: {len(recipes) if recipes else 0}")
            
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=16000,  # Increased for detailed nutritional info
                temperature=0.7,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            print(f"[MenuGenerator] Respuesta recibida de Claude API")
            
            # Parse response
            response_text = message.content[0].text
            print(f"[MenuGenerator] Longitud de respuesta: {len(response_text)} caracteres")
            
            # Try to extract JSON from response
            menu_data = self._parse_menu_response(response_text, adults, children)
            print(f"[MenuGenerator] Menú parseado correctamente")
            
            return {
                'success': True,
                'menu': menu_data,
                'raw_response': response_text,
                'generated_at': datetime.now().isoformat()
            }
            
        except anthropic.APIError as e:
            error_msg = f"Error de API de Anthropic: {e.message if hasattr(e, 'message') else str(e)}"
            print(f"[MenuGenerator] ERROR: {error_msg}")
            return {
                'success': False,
                'error': error_msg,
                'menu': None
            }
        except httpx.TimeoutException:
            error_msg = "Timeout: La generación del menú tardó demasiado tiempo (>5 minutos). Intenta de nuevo."
            print(f"[MenuGenerator] ERROR: {error_msg}")
            return {
                'success': False,
                'error': error_msg,
                'menu': None
            }
        except Exception as e:
            error_msg = f"Error inesperado: {str(e)}"
            print(f"[MenuGenerator] ERROR: {error_msg}")
            import traceback
            traceback.print_exc()
            return {
                'success': False,
                'error': error_msg,
                'menu': None
            }
    
    def generate_single_day_menu(self,
                                adults: List[Dict],
                                children: List[Dict],
                                recipes: Optional[List[Dict]] = None,
                                preferences: Optional[Dict] = None,
                                day_name: str = 'lunes',
                                menu_type: str = 'adultos',
                                specific_meal: Optional[str] = None,
                                historical_ratings: Optional[List[Dict]] = None) -> Dict:
        """
        Generate menu for a single day (adults or children only)
        
        Args:
            adults: List of adult profiles
            children: List of children profiles
            recipes: Optional list of available recipes
            preferences: Optional additional preferences
            day_name: Day name (lunes, martes, etc.)
            menu_type: 'adultos' or 'ninos'
            specific_meal: Optional specific meal to generate (desayuno, comida, merienda, cena)
            historical_ratings: Optional historical ratings for learning
        
        Returns:
            Dictionary with day menu
        """
        # Build prompt for single day
        prompt = self._build_single_day_prompt(adults, children, recipes, preferences, day_name, menu_type, specific_meal, historical_ratings)
        
        try:
            print(f"[MenuGenerator] Generating single day menu for {day_name} ({menu_type})...")
            
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=8000,
                temperature=0.7,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            response_text = message.content[0].text
            print(f"[MenuGenerator] Response received, length: {len(response_text)}")
            
            # Parse response
            day_menu = self._parse_single_day_response(response_text, menu_type)
            
            return {
                'success': True,
                'day_menu': day_menu,
                'raw_response': response_text
            }
            
        except Exception as e:
            error_msg = f"Error generando menú: {str(e)}"
            print(f"[MenuGenerator] ERROR: {error_msg}")
            import traceback
            traceback.print_exc()
            return {
                'success': False,
                'error': error_msg,
                'day_menu': None
            }
    
    def _build_single_day_prompt(self,
                                adults: List[Dict],
                                children: List[Dict],
                                recipes: Optional[List[Dict]],
                                preferences: Optional[Dict],
                                day_name: str,
                                menu_type: str,
                                specific_meal: Optional[str] = None,
                                historical_ratings: Optional[List[Dict]] = None) -> str:
        """Build prompt for single day menu generation"""
        
        if specific_meal:
            prompt = f"""Eres un nutricionista y chef experto. Genera UNA SOLA COMIDA para {menu_type}.

**DÍA:** {day_name.capitalize()}
**TIPO:** {menu_type.capitalize()}
**COMIDA ESPECÍFICA:** {specific_meal.upper()}

"""
        else:
            prompt = f"""Eres un nutricionista y chef experto. Genera UN SOLO DÍA de menú para {menu_type}.

**DÍA:** {day_name.capitalize()}
**TIPO:** {menu_type.capitalize()}

"""
        
        # Add family profiles (simplified) - only if not generating specific meal
        if not specific_meal:
            if menu_type == 'adultos' and adults:
                prompt += "**PERFILES DE ADULTOS:**\n\n"
                for adult in adults:
                    prompt += f"- {adult.get('nombre', 'Sin nombre')}: "
                    if adult.get('alergias'):
                        prompt += f"ALERGIAS: {adult['alergias']}. "
                    if adult.get('ingredientes_favoritos'):
                        prompt += f"Le gusta: {adult['ingredientes_favoritos']}. "
                    if adult.get('ingredientes_no_gustan'):
                        prompt += f"No le gusta: {adult['ingredientes_no_gustan']}. "
                    prompt += "\n"
            elif menu_type == 'ninos' and children:
                prompt += "**PERFILES DE NIÑOS:**\n\n"
                for child in children:
                    prompt += f"- {child.get('nombre', 'Sin nombre')}: "
                    if child.get('alergias'):
                        prompt += f"ALERGIAS: {child['alergias']}. "
                    if child.get('ingredientes_favoritos'):
                        prompt += f"Le encanta: {child['ingredientes_favoritos']}. "
                    if child.get('ingredientes_rechaza'):
                        prompt += f"RECHAZA: {child['ingredientes_rechaza']}. "
                    prompt += "\n"
        
        # Add historical ratings - only if not generating specific meal
        if not specific_meal and historical_ratings:
            prompt += "\n**⭐ APRENDE DE ESTOS RATINGS:**\n\n"
            high_ratings = [r for r in historical_ratings if r.get('rating', 0) >= 4 and r.get('menu_type') == menu_type]
            low_ratings = [r for r in historical_ratings if r.get('rating', 0) <= 2 and r.get('menu_type') == menu_type]
            
            if high_ratings:
                prompt += "✅ REPITE estilos similares a estos (4-5⭐):\n"
                for rating in high_ratings[:5]:
                    menu_data = rating.get('menu_data', {})
                    day_data = menu_data.get(f'menu_{menu_type}', {}).get('dias', {}).get(day_name, {})
                    if day_data:
                        for meal_type in ['desayuno', 'comida', 'merienda', 'cena']:
                            if meal_type in day_data:
                                meal_name = day_data[meal_type].get('nombre', '')
                                if isinstance(meal_name, dict):
                                    meal_name = meal_name.get('name', '')
                                if meal_name:
                                    prompt += f"  • {meal_name}\n"
                prompt += "\n"
            
            if low_ratings:
                prompt += "❌ EVITA estos platos (1-2⭐):\n"
                for rating in low_ratings[:3]:
                    menu_data = rating.get('menu_data', {})
                    day_data = menu_data.get(f'menu_{menu_type}', {}).get('dias', {}).get(day_name, {})
                    if day_data:
                        for meal_type in ['desayuno', 'comida', 'merienda', 'cena']:
                            if meal_type in day_data:
                                meal_name = day_data[meal_type].get('nombre', '')
                                if isinstance(meal_name, dict):
                                    meal_name = meal_name.get('name', '')
                                if meal_name:
                                    prompt += f"  • NO: {meal_name}\n"
                prompt += "\n"
        
        # Add meal types
        if specific_meal:
            prompt += f"""**GENERA SOLO esta comida:**\n
- {specific_meal}

**FORMATO JSON (solo la comida solicitada):**
{{
  "{specific_meal}": {{
    "nombre": "Nombre del plato",
    "ingredientes": ["ing1", "ing2"],
    "tiempo_prep": 15,
    "calorias": 350,
    "nutrientes": {{
      "proteinas": "20g",
      "carbohidratos": "40g",
      "grasas": "12g"
    }},
    "instrucciones": "Pasos de preparación",
    "receta_base": "Nombre o 'Original'",
    "porque_seleccionada": "Por qué es buena para esta familia"
  }}
}}

**IMPORTANTE:**
- Respeta TODAS las alergias e intolerancias
- Usa ingredientes que les gustan
- Evita ingredientes que rechazan
- Genera SOLO la comida {specific_meal}, no otras comidas
- Genera SOLO el JSON, sin texto adicional

**GENERA LA COMIDA AHORA:**
"""
        else:
            if menu_type == 'adultos':
                prompt += "**GENERA estas comidas para este día:**\n"
                prompt += "- desayuno\n"
                prompt += "- comida\n"
                prompt += "- cena\n\n"
            else:
                prompt += "**GENERA estas comidas para este día:**\n"
                prompt += "- desayuno\n"
                prompt += "- comida\n"
                prompt += "- merienda\n"
                prompt += "- cena\n\n"
            
            prompt += """**FORMATO JSON (solo el día solicitado):**

{
  "desayuno": {
    "nombre": "Nombre del plato",
    "ingredientes": ["ing1", "ing2"],
    "tiempo_prep": 15,
    "calorias": 350,
    "nutrientes": {
      "proteinas": "20g",
      "carbohidratos": "40g",
      "grasas": "12g"
    },
    "instrucciones": "Pasos de preparación",
    "receta_base": "Nombre o 'Original'",
    "porque_seleccionada": "Por qué es buena para esta familia"
  },
  "comida": { /* misma estructura */ },
  "merienda": { /* solo para niños */ },
  "cena": { /* misma estructura */ }
}

**IMPORTANTE:**
- Respeta TODAS las alergias e intolerancias
- Usa ingredientes que les gustan
- Evita ingredientes que rechazan
- Aprende de los ratings históricos
- Genera SOLO el JSON, sin texto adicional

**GENERA EL MENÚ AHORA:**
"""
        
        return prompt
    
    def _parse_single_day_response(self, response: str, menu_type: str) -> Dict:
        """Parse single day menu response"""
        import re
        
        try:
            # Try to find JSON in response
            json_match = re.search(r'```json\s*(.*?)\s*```', response, re.DOTALL)
            if json_match:
                json_str = json_match.group(1).strip()
            else:
                json_match = re.search(r'```\s*(.*?)\s*```', response, re.DOTALL)
                if json_match:
                    json_str = json_match.group(1).strip()
                else:
                    # Try to find JSON object
                    brace_count = 0
                    start_pos = -1
                    for i, char in enumerate(response):
                        if char == '{':
                            if brace_count == 0:
                                start_pos = i
                            brace_count += 1
                        elif char == '}':
                            brace_count -= 1
                            if brace_count == 0 and start_pos != -1:
                                json_str = response[start_pos:i+1]
                                break
                    else:
                        json_str = response
            
            # Clean JSON
            json_str = re.sub(r'//.*?$', '', json_str, flags=re.MULTILINE)
            json_str = re.sub(r',\s*}', '}', json_str)
            json_str = re.sub(r',\s*]', ']', json_str)
            
            day_menu = json.loads(json_str)
            return day_menu
            
        except Exception as e:
            print(f"[MenuGenerator] Error parsing single day response: {e}")
            return {}
    
    def _build_menu_prompt(self, 
                          adults: List[Dict], 
                          children: List[Dict],
                          recipes: Optional[List[Dict]],
                          preferences: Optional[Dict],
                          day_settings: Optional[Dict] = None,
                          highly_rated_menus: Optional[List[Dict]] = None,
                          historical_ratings: Optional[List[Dict]] = None) -> str:
        """Build the enhanced prompt for Claude with nutrition and day settings"""
        
        prompt = """Eres un nutricionista y chef experto con especialización en:
- Planificación de menús familiares equilibrados
- Análisis nutricional y conteo calórico
- Cocina mediterránea y española
- Adaptación de recetas para niños selectivos

Tu tarea es crear un menú semanal COMPLETO Y DETALLADO para una familia en Barcelona, España.

═══════════════════════════════════════════════════════════════════

**INFORMACIÓN DE LA FAMILIA:**

"""
        
        # Add adults information
        prompt += "**👨‍👩‍👧 ADULTOS DE LA FAMILIA:**\n\n"
        for i, adult in enumerate(adults, 1):
            prompt += f"**Adulto {i}: {adult.get('nombre', 'Sin nombre')}**\n"
            prompt += f"- Edad: {adult.get('edad', 'N/A')} años\n"
            
            if adult.get('objetivo_alimentario'):
                prompt += f"- 🎯 Objetivo nutricional: {adult['objetivo_alimentario']}\n"
            
            if adult.get('estilo_alimentacion'):
                prompt += f"- 🥗 Estilo alimentación: {adult['estilo_alimentacion']}\n"
            
            if adult.get('cocinas_favoritas'):
                prompt += f"- 🍽️ Cocinas favoritas: {adult['cocinas_favoritas']}\n"
            
            if adult.get('alergias'):
                prompt += f"- ⚠️ **ALERGIAS CRÍTICAS**: {adult['alergias']}\n"
            
            if adult.get('intolerancias'):
                prompt += f"- ⚠️ **INTOLERANCIAS**: {adult['intolerancias']}\n"
            
            if adult.get('restricciones_religiosas'):
                prompt += f"- 🕌 Restricciones religiosas: {adult['restricciones_religiosas']}\n"
            
            if adult.get('ingredientes_favoritos'):
                prompt += f"- ✅ Ingredientes favoritos: {adult['ingredientes_favoritos']}\n"
            
            if adult.get('ingredientes_no_gustan'):
                prompt += f"- ❌ No le gusta: {adult['ingredientes_no_gustan']}\n"
            
            if adult.get('tiempo_max_cocinar'):
                prompt += f"- ⏱️ Tiempo máximo cocina: {adult['tiempo_max_cocinar']} minutos\n"
            
            if adult.get('nivel_cocina'):
                prompt += f"- 👨‍🍳 Nivel de cocina: {adult['nivel_cocina']}\n"
            
            prompt += "\n"
        
        # Add children information
        if children:
            prompt += "**🧒 NIÑOS DE LA FAMILIA:**\n\n"
            for i, child in enumerate(children, 1):
                prompt += f"**Niño/a {i}: {child.get('nombre', 'Sin nombre')}**\n"
                prompt += f"- Edad: {child.get('edad', 'N/A')} años\n"
                
                if child.get('nivel_exigencia'):
                    prompt += f"- 😤 Nivel de exigencia: {child['nivel_exigencia']}\n"
                
                if child.get('acepta_comida_nueva'):
                    prompt += f"- 🆕 Acepta comida nueva: {child['acepta_comida_nueva']}\n"
                
                if child.get('alergias'):
                    prompt += f"- ⚠️ **ALERGIAS CRÍTICAS**: {child['alergias']}\n"
                
                if child.get('intolerancias'):
                    prompt += f"- ⚠️ **INTOLERANCIAS**: {child['intolerancias']}\n"
                
                if child.get('ingredientes_favoritos'):
                    prompt += f"- ✅ Le encanta: {child['ingredientes_favoritos']}\n"
                
                if child.get('ingredientes_rechaza'):
                    prompt += f"- ❌ RECHAZA completamente: {child['ingredientes_rechaza']}\n"
                
                if child.get('verduras_aceptadas'):
                    prompt += f"- 🥕 Verduras que acepta: {child['verduras_aceptadas']}\n"
                
                if child.get('verduras_rechazadas'):
                    prompt += f"- 🥦 Verduras que rechaza: {child['verduras_rechazadas']}\n"
                
                if child.get('texturas_no_gustan'):
                    prompt += f"- 👅 Texturas que no tolera: {child['texturas_no_gustan']}\n"
                
                if child.get('comentarios_padres'):
                    prompt += f"- 💬 Notas de los padres: {child['comentarios_padres']}\n"
                
                prompt += "\n"
        
        # Add day settings if provided
        if day_settings:
            prompt += "**📅 CONFIGURACIÓN DE DÍAS:**\n\n"
            dias_es = {
                'lunes': 'Lunes', 'martes': 'Martes', 'miercoles': 'Miércoles',
                'jueves': 'Jueves', 'viernes': 'Viernes', 'sabado': 'Sábado', 'domingo': 'Domingo'
            }
            for dia, config in day_settings.items():
                prompt += f"**{dias_es.get(dia, dia)}:**\n"
                if config.get('no_cooking'):
                    prompt += "  - ⚠️ NO SE COCINA este día (comen fuera o sobras)\n"
                elif config.get('meals'):
                    meals_str = ", ".join(config['meals'])
                    prompt += f"  - Comidas a preparar: {meals_str}\n"
                else:
                    prompt += "  - Todas las comidas (desayuno, comida, merienda, cena)\n"
            prompt += "\n"
        
        # Add available recipes with MORE DETAIL
        if recipes:
            prompt += "\n**📖 BASE DE DATOS DE RECETAS DISPONIBLES:**\n"
            prompt += "(Puedes inspirarte en estas recetas o adaptarlas para el menú)\n\n"
            for recipe in recipes[:20]:  # Increased to 20 recipes
                prompt += f"• **{recipe.get('title', 'Sin título')}**\n"
                if recipe.get('url'):
                    prompt += f"  URL: {recipe['url']}\n"
                if recipe.get('cuisine_type'):
                    prompt += f"  Tipo cocina: {recipe['cuisine_type']}\n"
                if recipe.get('prep_time'):
                    prompt += f"  Tiempo: {recipe['prep_time']} min\n"
                if recipe.get('ingredients'):
                    ings = recipe['ingredients'][:5]  # First 5 ingredients
                    prompt += f"  Ingredientes clave: {', '.join(ings)}\n"
                prompt += "\n"
        
        # Add menu preferences (days and meals)
        include_weekend = preferences.get('include_weekend', True) if preferences else True
        include_breakfast = preferences.get('include_breakfast', True) if preferences else True
        include_lunch = preferences.get('include_lunch', True) if preferences else True
        include_dinner = preferences.get('include_dinner', True) if preferences else True
        excluded_days = preferences.get('excluded_days', []) if preferences else []
        
        prompt += "**CONFIGURACIÓN DEL MENÚ:**\n\n"
        
        # Days configuration
        if include_weekend:
            prompt += "- **Días a incluir**: Lunes a Domingo (7 días completos)\n"
        else:
            prompt += "- **Días a incluir**: Lunes a Viernes solamente (5 días laborables)\n"
        
        if excluded_days:
            prompt += f"- **Días EXCLUIDOS**: {', '.join(excluded_days)} - NO generar menú para estos días\n"
        
        # Meals configuration
        meals_to_include = []
        if include_breakfast:
            meals_to_include.append('Desayuno')
        if include_lunch:
            meals_to_include.append('Comida/Almuerzo')
        if include_dinner:
            meals_to_include.append('Cena')
        
        prompt += f"- **Comidas a incluir**: {', '.join(meals_to_include)}\n"
        
        if not include_breakfast:
            prompt += "  ⚠️ NO incluyas desayuno en ningún día\n"
        if not include_lunch:
            prompt += "  ⚠️ NO incluyas comida/almuerzo en ningún día\n"
        if not include_dinner:
            prompt += "  ⚠️ NO incluyas cena en ningún día\n"
        
        prompt += "\n"
        
        # Add additional preferences
        if preferences:
            other_prefs = {k: v for k, v in preferences.items() 
                          if k not in ['include_weekend', 'include_breakfast', 'include_lunch', 'include_dinner', 'excluded_days']}
            if other_prefs:
                prompt += "**OTRAS PREFERENCIAS:**\n\n"
                for key, value in other_prefs.items():
                    prompt += f"- {key}: {value}\n"
                prompt += "\n"
        
        # Add historical ratings for learning
        if historical_ratings:
            prompt += "**⭐ HISTORIAL DE CALIFICACIONES (APRENDE DE ESTO):**\n\n"
            prompt += "La familia ha calificado estos menús anteriores. Usa esta información para entender sus gustos:\n\n"
            
            # Group by rating
            high_ratings = [r for r in historical_ratings if r.get('rating', 0) >= 4]
            low_ratings = [r for r in historical_ratings if r.get('rating', 0) <= 2]
            
            if high_ratings:
                prompt += "**✅ MENÚS QUE LES GUSTARON (4-5 estrellas):**\n"
                for rating in high_ratings[:10]:  # Top 10
                    menu_data = rating.get('menu_data', {})
                    day_name = rating.get('day_name', '')
                    menu_type = rating.get('menu_type', '')
                    rating_val = rating.get('rating', 0)
                    
                    if menu_data and day_name and menu_type:
                        menu_key = f'menu_{menu_type}'
                        if menu_key in menu_data and 'dias' in menu_data[menu_key]:
                            day_data = menu_data[menu_key]['dias'].get(day_name, {})
                            if day_data:
                                prompt += f"- {day_name.capitalize()} ({menu_type}): {rating_val}⭐\n"
                                # Add meal names
                                for meal_type in ['desayuno', 'comida', 'merienda', 'cena']:
                                    if meal_type in day_data:
                                        meal = day_data[meal_type]
                                        meal_name = meal.get('nombre', '')
                                        if isinstance(meal_name, dict):
                                            meal_name = meal_name.get('name', '')
                                        if meal_name:
                                            prompt += f"  • {meal_type}: {meal_name}\n"
                prompt += "\n"
            
            if low_ratings:
                prompt += "**❌ MENÚS QUE NO LES GUSTARON (1-2 estrellas):**\n"
                prompt += "EVITA generar menús similares a estos:\n"
                for rating in low_ratings[:5]:  # Top 5 worst
                    menu_data = rating.get('menu_data', {})
                    day_name = rating.get('day_name', '')
                    menu_type = rating.get('menu_type', '')
                    rating_val = rating.get('rating', 0)
                    
                    if menu_data and day_name and menu_type:
                        menu_key = f'menu_{menu_type}'
                        if menu_key in menu_data and 'dias' in menu_data[menu_key]:
                            day_data = menu_data[menu_key]['dias'].get(day_name, {})
                            if day_data:
                                prompt += f"- {day_name.capitalize()} ({menu_type}): {rating_val}⭐ - EVITAR:\n"
                                # Add meal names to avoid
                                for meal_type in ['desayuno', 'comida', 'merienda', 'cena']:
                                    if meal_type in day_data:
                                        meal = day_data[meal_type]
                                        meal_name = meal.get('nombre', '')
                                        if isinstance(meal_name, dict):
                                            meal_name = meal_name.get('name', '')
                                        if meal_name:
                                            prompt += f"  • NO repetir: {meal_name}\n"
                prompt += "\n"
            
            prompt += "**IMPORTANTE:**\n"
            prompt += "- Repite estilos y tipos de comida que recibieron 4-5 estrellas\n"
            prompt += "- Evita completamente los platos que recibieron 1-2 estrellas\n"
            prompt += "- Aprende de los ingredientes y combinaciones que funcionaron bien\n\n"
        
        # Enhanced instructions
        prompt += """
═══════════════════════════════════════════════════════════════════

**📋 INSTRUCCIONES DETALLADAS:**

**ESTRUCTURA DEL MENÚ:**

Genera DOS menús separados (uno para adultos, otro para niños) para TODA LA SEMANA (Lunes a Domingo).

**Para ADULTOS**, cada día incluye:
1. **Desayuno** (07:00-09:00) - Energético y balanceado
2. **Comida** (13:00-15:00) - Plato principal completo
3. **Cena** (20:00-22:00) - Ligero pero nutritivo

**Para NIÑOS**, cada día incluye:
1. **Desayuno** (07:00-09:00) - Rápido y atractivo
2. **Comida** (13:00-15:00) - Adaptado a sus gustos
3. **Merienda** (17:00-18:00) - Snack saludable
4. **Cena** (20:00-22:00) - Fácil de comer

**IMPORTANTE SOBRE LOS DÍAS:**
"""
        
        # Add day settings instructions
        if day_settings:
            prompt += "- Si un día tiene \"no_cooking: true\", NO generes recetas para ese día\n"
            prompt += "- Si un día especifica meals específicas, solo genera esas comidas\n"
        else:
            prompt += "- Si no hay configuración especial, genera todas las comidas\n"
        
        # Add meal preferences instructions
        if not include_breakfast:
            prompt += "- ⚠️ NO incluyas desayuno en ningún día\n"
        if not include_lunch:
            prompt += "- ⚠️ NO incluyas comida/almuerzo en ningún día\n"
        if not include_dinner:
            prompt += "- ⚠️ NO incluyas cena en ningún día\n"
        
        if excluded_days:
            prompt += f"- ⚠️ NO generes menú para estos días: {', '.join(excluded_days)}\n"
        
        if not include_weekend:
            prompt += "- ⚠️ Solo incluye días de Lunes a Viernes (NO sábado ni domingo)\n"
        
        prompt += """
═══════════════════════════════════════════════════════════════════

**🎯 CONSIDERACIONES CRÍTICAS:**

**ALERGIAS E INTOLERANCIAS:**
- ⚠️ NUNCA incluyas ingredientes que causen alergias o intolerancias
- Revisa TODOS los ingredientes antes de incluirlos
- Si hay duda, usa alternativas seguras

**BALANCE NUTRICIONAL:**
- Varía las proteínas: pollo, pescado, carne roja, legumbres, huevos
- Incluye 5+ raciones frutas/verduras diarias
- Equilibra carbohidratos complejos y simples
- Grasas saludables (aceite oliva, aguacate, frutos secos)
- Fibra adecuada para digestión

**PARA NIÑOS SELECTIVOS:**
- Presenta verduras de forma no visible si las rechazan
- Usa formas divertidas y colores atractivos
- Ofrece opciones que SABEMOS que aceptan
- Adapta texturas según sus preferencias
- Si un niño rechaza algo completamente, busca alternativas

**VARIEDAD Y PLANIFICACIÓN:**
- No repitas la misma proteína 2 días seguidos
- Alterna cocinas: española, mediterránea, asiática, italiana
- Considera tiempo de preparación (máximo indicado)
- Usa recetas de la base de datos cuando sea posible
- Planifica sobras estratégicas para días ocupados

**CALORÍAS Y NUTRIENTES:**
- Calcula calorías aproximadas por porción
- Incluye macronutrientes (proteínas, carbohidratos, grasas en gramos)
- Añade micronutrientes destacados (vitaminas, minerales principales)

**LISTA DE COMPRAS CON CANTIDADES (CRÍTICO - NO USES ARRAYS SIMPLES):**
- ⚠️ OBLIGATORIO: La estructura DEBE ser un objeto con "por_categoria", NO un array simple
- ⚠️ OBLIGATORIO: Cada ingrediente DEBE tener "nombre", "cantidad" y "notas" (puede ser string vacío)
- ⚠️ OBLIGATORIO: Incluye CANTIDADES ESPECÍFICAS para cada ingrediente (ej: "2 kg", "500g", "12 unidades", "1 litro", "3 piezas")
- Calcula las cantidades según el número de adultos y niños en la familia
- Considera las porciones estándar: adultos (150-200g proteína, 80-100g carbohidratos), niños (80-120g proteína, 60-80g carbohidratos)
- Agrupa ingredientes por categorías: frutas_verduras, carnes_pescados, lacteos_huevos, cereales_legumbres, despensa, congelados, otros
- Combina cantidades cuando el mismo ingrediente aparece en múltiples platos
- Incluye notas cuando sea relevante (ej: "sin piel", "maduros pero firmes")
- EJEMPLO CORRECTO: {"nombre": "Pechuga de pollo", "cantidad": "1.5 kg", "notas": "Sin piel"}
- EJEMPLO INCORRECTO: "pechuga de pollo" (sin cantidad)

═══════════════════════════════════════════════════════════════════

**📤 FORMATO DE RESPUESTA JSON:**

Devuelve SOLO JSON válido (sin markdown, sin ```json```), con esta estructura EXACTA:

{
  "semana": "2025-01-06",
  "recomendaciones_generales": "Descripción general del menú, consideraciones especiales, tips de organización",
  
  "menu_adultos": {
    "dias": {
      "lunes": {
        "desayuno": {
          "nombre": "Nombre descriptivo del plato",
          "ingredientes": ["ingrediente1", "ingrediente2", ...],
          "tiempo_prep": 15,
          "calorias": 350,
          "nutrientes": {
            "proteinas": "20g",
            "carbohidratos": "40g",
            "grasas": "12g",
            "fibra": "5g",
            "destacados": "Vitamina C, Hierro, Omega-3"
          },
          "instrucciones": "Pasos breves de preparación (3-4 pasos máximo)",
          "notas": "Tips especiales, adaptaciones, conservación",
          "receta_base": "Nombre de receta de BD si aplica o 'Original'",
          "porque_seleccionada": "Por qué es buena para esta familia"
        },
        "comida": { /* misma estructura */ },
        "cena": { /* misma estructura */ }
      },
      "martes": { /* ... */ },
      "miercoles": { /* ... */ },
      "jueves": { /* ... */ },
      "viernes": { /* ... */ },
      "sabado": { /* ... */ },
      "domingo": { /* ... */ }
    },
    "lista_compras": {
      "por_categoria": {
        "frutas_verduras": [
          {"nombre": "Tomates", "cantidad": "2 kg", "notas": "Maduros pero firmes"}
        ],
        "carnes_pescados": [
          {"nombre": "Pechuga de pollo", "cantidad": "1.5 kg", "notas": "Sin piel"}
        ],
        "lacteos_huevos": [
          {"nombre": "Huevos", "cantidad": "12 unidades", "notas": ""}
        ],
        "cereales_legumbres": [
          {"nombre": "Arroz integral", "cantidad": "500g", "notas": ""}
        ],
        "despensa": [
          {"nombre": "Aceite de oliva", "cantidad": "500ml", "notas": "Virgen extra"}
        ],
        "congelados": [],
        "otros": []
      },
      "resumen_cantidades": {
        "total_items": 15,
        "por_categoria": {
          "frutas_verduras": 5,
          "carnes_pescados": 3,
          "lacteos_huevos": 2,
          "cereales_legumbres": 2,
          "despensa": 3
        }
      }
    },
    "resumen_semanal": {
      "total_calorias_promedio_dia": 2000,
      "distribucion_macronutrientes": {
        "proteinas_pct": 25,
        "carbohidratos_pct": 50,
        "grasas_pct": 25
      },
      "variedad_proteinas": ["pollo: 3 veces", "pescado: 2 veces", "legumbres: 1 vez", "carne: 1 vez"]
    }
  },
  
  "menu_ninos": {
    "dias": {
      "lunes": {
        "desayuno": { /* misma estructura que adultos */ },
        "comida": { /* misma estructura */ },
        "merienda": { /* específica para niños */ },
        "cena": { /* misma estructura */ }
      }
      /* ... resto de días ... */
    },
    "lista_compras": {
      "por_categoria": {
        "frutas_verduras": [
          {"nombre": "Plátanos", "cantidad": "6 unidades", "notas": "Maduros"}
        ],
        "carnes_pescados": [
          {"nombre": "Pechuga de pollo", "cantidad": "800g", "notas": "Sin piel, cortado en tiras"}
        ],
        "lacteos_huevos": [
          {"nombre": "Leche entera", "cantidad": "1 litro", "notas": ""}
        ],
        "cereales_legumbres": [],
        "despensa": [],
        "congelados": [],
        "otros": []
      },
      "resumen_cantidades": {
        "total_items": 8,
        "por_categoria": {
          "frutas_verduras": 3,
          "carnes_pescados": 2,
          "lacteos_huevos": 3
        }
      }
    },
    "resumen_semanal": {
      "total_calorias_promedio_dia": 1600,
      "consideraciones_especiales": "Adaptaciones hechas para selectividad, texturas evitadas, etc."
    }
  },
  
  "preparacion_semanal": {
    "batch_cooking": ["Qué preparar el domingo para toda la semana"],
    "tips_organizacion": ["Consejos para organizarse mejor"],
    "orden_compra": {
      "frescos": ["comprar 2 veces por semana"],
      "no_perecederos": ["comprar 1 vez"],
      "congelados": ["tener siempre en stock"]
    }
  }
}

═══════════════════════════════════════════════════════════════════

**✅ CHECKLIST FINAL ANTES DE RESPONDER:**

- [ ] He revisado TODAS las alergias e intolerancias
- [ ] He incluido calorías y nutrientes en CADA comida
- [ ] He generado menús SEPARADOS para adultos y niños
- [ ] He usado recetas de la base de datos cuando posible
- [ ] He respetado la configuración de días
- [ ] He variado las proteínas a lo largo de la semana
- [ ] He adaptado platos para niños selectivos
- [ ] He incluido instrucciones claras de preparación
- [ ] He generado lista de compras completa CON CANTIDADES ESPECÍFICAS para cada ingrediente
- [ ] Las cantidades están calculadas según el número de adultos y niños en la familia
- [ ] He categorizado todos los ingredientes correctamente
- [ ] El JSON es válido y sigue la estructura exacta

**AHORA GENERA EL MENÚ COMPLETO:**
"""
        
        return prompt
    
    def _normalize_shopping_lists(self, menu_data: Dict, num_adults: int = 0, num_children: int = 0) -> Dict:
        """Convert simple array shopping lists to structured format with quantities"""
        import re
        
        def estimate_quantity(item_name: str, category: str, num_adults: int, num_children: int) -> str:
            """Estimate quantity based on item name, category, and family size"""
            item_lower = item_name.lower()
            total_people = num_adults + num_children
            
            # Protein estimates (per person per week)
            if any(word in item_lower for word in ['pollo', 'chicken', 'pavo', 'turkey']):
                return f"{total_people * 200}g"
            elif any(word in item_lower for word in ['cerdo', 'pork', 'ternera', 'beef', 'carne', 'meat']):
                return f"{total_people * 150}g"
            elif any(word in item_lower for word in ['pescado', 'fish', 'salmón', 'salmon', 'merluza', 'hake', 'bacalao', 'cod', 'gambas', 'shrimp', 'mejillones', 'mussels']):
                return f"{total_people * 150}g"
            elif 'huevo' in item_lower or 'egg' in item_lower:
                return f"{total_people * 6} unidades"
            
            # Vegetables (per person per week)
            elif any(word in item_lower for word in ['tomate', 'tomato', 'cebolla', 'onion', 'ajo', 'garlic', 'pimiento', 'pepper', 'calabacín', 'zucchini']):
                return f"{total_people * 500}g"
            elif any(word in item_lower for word in ['lechuga', 'lettuce', 'espinaca', 'spinach', 'brócoli', 'broccoli', 'coliflor', 'cauliflower']):
                return f"{total_people * 300}g"
            elif any(word in item_lower for word in ['zanahoria', 'carrot', 'patata', 'potato', 'papas']):
                return f"{total_people * 1} kg"
            
            # Dairy
            elif any(word in item_lower for word in ['leche', 'milk', 'queso', 'cheese', 'mantequilla', 'butter']):
                return f"{total_people * 500}ml" if 'leche' in item_lower or 'milk' in item_lower else f"{total_people * 200}g"
            
            # Grains
            elif any(word in item_lower for word in ['arroz', 'rice', 'pasta', 'harina', 'flour', 'pan', 'bread', 'quinoa']):
                return f"{total_people * 500}g"
            
            # Oils and condiments
            elif any(word in item_lower for word in ['aceite', 'oil', 'vinagre', 'vinegar', 'salsa', 'sauce']):
                return f"{total_people * 250}ml" if 'aceite' in item_lower or 'oil' in item_lower else f"{total_people * 200}ml"
            
            # Default
            return f"{total_people * 200}g"
        
        def categorize_item(item_name: str) -> str:
            """Categorize an item based on keywords"""
            item_lower = item_name.lower()
            
            if any(word in item_lower for word in ['fruta', 'fruit', 'verdura', 'vegetable', 'tomate', 'tomato', 'cebolla', 'onion', 'ajo', 'garlic', 'pimiento', 'pepper', 'calabacín', 'zucchini', 'lechuga', 'lettuce', 'espinaca', 'spinach', 'brócoli', 'broccoli', 'coliflor', 'cauliflower', 'zanahoria', 'carrot', 'patata', 'potato', 'papas']):
                return 'frutas_verduras'
            elif any(word in item_lower for word in ['pollo', 'chicken', 'cerdo', 'pork', 'ternera', 'beef', 'carne', 'meat', 'pescado', 'fish', 'salmón', 'salmon', 'merluza', 'hake', 'bacalao', 'cod', 'gambas', 'shrimp', 'mejillones', 'mussels']):
                return 'carnes_pescados'
            elif any(word in item_lower for word in ['leche', 'milk', 'queso', 'cheese', 'mantequilla', 'butter', 'huevo', 'egg']):
                return 'lacteos_huevos'
            elif any(word in item_lower for word in ['arroz', 'rice', 'pasta', 'harina', 'flour', 'pan', 'bread', 'quinoa', 'legumbre', 'legume']):
                return 'cereales_legumbres'
            elif any(word in item_lower for word in ['congelado', 'frozen']):
                return 'congelados'
            else:
                return 'despensa'
        
        # Normalize menu_adultos.lista_compras
        if 'menu_adultos' in menu_data and 'lista_compras' in menu_data['menu_adultos']:
            lista_compras = menu_data['menu_adultos']['lista_compras']
            if isinstance(lista_compras, list):
                print(f"[MenuGenerator] Converting adult shopping list from array to structured format")
                por_categoria = {}
                for item in lista_compras:
                    if isinstance(item, str):
                        category = categorize_item(item)
                        if category not in por_categoria:
                            por_categoria[category] = []
                        por_categoria[category].append({
                            "nombre": item,
                            "cantidad": estimate_quantity(item, category, num_adults, 0),
                            "notas": ""
                        })
                menu_data['menu_adultos']['lista_compras'] = {
                    "por_categoria": por_categoria,
                    "resumen_cantidades": {
                        "total_items": sum(len(items) for items in por_categoria.values()),
                        "por_categoria": {cat: len(items) for cat, items in por_categoria.items()}
                    }
                }
        
        # Normalize menu_ninos.lista_compras
        if 'menu_ninos' in menu_data and 'lista_compras' in menu_data['menu_ninos']:
            lista_compras = menu_data['menu_ninos']['lista_compras']
            if isinstance(lista_compras, list):
                print(f"[MenuGenerator] Converting children shopping list from array to structured format")
                por_categoria = {}
                for item in lista_compras:
                    if isinstance(item, str):
                        category = categorize_item(item)
                        if category not in por_categoria:
                            por_categoria[category] = []
                        por_categoria[category].append({
                            "nombre": item,
                            "cantidad": estimate_quantity(item, category, 0, num_children),
                            "notas": ""
                        })
                menu_data['menu_ninos']['lista_compras'] = {
                    "por_categoria": por_categoria,
                    "resumen_cantidades": {
                        "total_items": sum(len(items) for items in por_categoria.values()),
                        "por_categoria": {cat: len(items) for cat, items in por_categoria.items()}
                    }
                }
        
        return menu_data
    
    def _parse_menu_response(self, response: str, adults: List[Dict] = None, children: List[Dict] = None) -> Dict:
        """Parse Claude's response to extract menu data"""
        
        # Try to find JSON in the response
        try:
            # First, try to find JSON between ```json and ```
            json_match = re.search(r'```json\s*(.*?)\s*```', response, re.DOTALL)
            
            if json_match:
                json_str = json_match.group(1).strip()
                print(f"[MenuGenerator] Found JSON in code block, length: {len(json_str)}")
            else:
                # Try to find JSON between ``` and ``` (without json label)
                json_match = re.search(r'```\s*(.*?)\s*```', response, re.DOTALL)
                if json_match:
                    json_str = json_match.group(1).strip()
                    # Check if it looks like JSON (starts with { or [)
                    if json_str.startswith('{') or json_str.startswith('['):
                        print(f"[MenuGenerator] Found JSON in code block (no label), length: {len(json_str)}")
                    else:
                        json_str = None
                else:
                    json_str = None
                
                # If still no JSON found, try to find any {...} structure
                # Use a more robust approach to find the complete JSON object
                if not json_str:
                    # Try to find the outermost JSON object by counting braces
                    brace_count = 0
                    start_pos = -1
                    for i, char in enumerate(response):
                        if char == '{':
                            if brace_count == 0:
                                start_pos = i
                            brace_count += 1
                        elif char == '}':
                            brace_count -= 1
                            if brace_count == 0 and start_pos != -1:
                                json_str = response[start_pos:i+1]
                                print(f"[MenuGenerator] Found JSON structure by brace counting, length: {len(json_str)}")
                                break
                    
                    # Fallback to regex if brace counting didn't work
                    if not json_str:
                        json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', response, re.DOTALL)
                        if json_match:
                            json_str = json_match.group(0)
                            print(f"[MenuGenerator] Found JSON structure via regex, length: {len(json_str)}")
            
            if json_str:
                # Clean up the JSON string
                # Remove comments (// and /* */)
                json_str = re.sub(r'//.*?$', '', json_str, flags=re.MULTILINE)  # Single-line comments
                json_str = re.sub(r'/\*.*?\*/', '', json_str, flags=re.DOTALL)  # Multi-line comments
                
                # Remove trailing commas before closing braces/brackets
                json_str = re.sub(r',\s*}', '}', json_str)
                json_str = re.sub(r',\s*]', ']', json_str)
                
                # Try to fix unescaped quotes in string values
                # This is tricky - we need to be careful not to break valid JSON
                # Pattern: find string values that might have unescaped quotes
                # We'll use a state machine approach
                try:
                    # First attempt: parse as-is
                    menu_data = json.loads(json_str)
                    # Normalize shopping lists after parsing
                    menu_data = self._normalize_shopping_lists(menu_data, len(adults) if adults else 0, len(children) if children else 0)
                except json.JSONDecodeError as e:
                    print(f"[MenuGenerator] First parse attempt failed: {e}")
                    print(f"[MenuGenerator] Error at position {e.pos}, trying to fix...")
                    
                    # Try to fix common issues around the error position
                    error_pos = e.pos
                    if error_pos < len(json_str):
                        # Get context around error
                        start = max(0, error_pos - 100)
                        end = min(len(json_str), error_pos + 100)
                        context = json_str[start:end]
                        print(f"[MenuGenerator] Context around error: {context}")
                        
                        # Try to fix unescaped quotes - look for patterns like: "text"more text"
                        # This is a heuristic fix
                        fixed_json = json_str
                        
                        # Find string values and check for unescaped quotes
                        # Pattern: "key": "value" where value might contain unescaped quotes
                        # We'll try to escape quotes that appear to be inside string values
                        # This is risky but worth trying
                        
                        # More conservative approach: try parsing with json5-like fixes
                        # Remove any obvious syntax errors
                        fixed_json = re.sub(r',(\s*[}\]])', r'\1', fixed_json)  # Remove trailing commas
                        fixed_json = re.sub(r'//.*?$', '', fixed_json, flags=re.MULTILINE)  # Remove comments
                        fixed_json = re.sub(r'/\*.*?\*/', '', fixed_json, flags=re.DOTALL)  # Remove block comments
                        
                        # Try to repair unescaped quotes using state machine
                        try:
                            repaired_json = repair_json_string(fixed_json)
                            menu_data = json.loads(repaired_json)
                            print(f"[MenuGenerator] Successfully parsed after repair")
                            print(f"[MenuGenerator] Menu keys: {list(menu_data.keys())}")
                            # Normalize shopping lists after parsing
                            menu_data = self._normalize_shopping_lists(menu_data, len(adults) if 'adults' in locals() else 0, len(children) if 'children' in locals() else 0)
                            return menu_data
                        except json.JSONDecodeError as e2:
                            print(f"[MenuGenerator] Repair attempt also failed: {e2}")
                            print(f"[MenuGenerator] Error at position {e2.pos}")
                            # Return as text format so frontend can try to fix it
                            return {
                                'formato': 'texto',
                                'contenido': response
                            }
                    else:
                        # Return as text format
                        return {
                            'formato': 'texto',
                            'contenido': response
                        }
                
                # Remove any whitespace issues
                json_str = json_str.strip()
                
                print(f"[MenuGenerator] Successfully parsed JSON menu")
                print(f"[MenuGenerator] Menu keys: {list(menu_data.keys())}")
                # Normalize shopping lists after parsing
                menu_data = self._normalize_shopping_lists(menu_data, len(adults) if adults else 0, len(children) if children else 0)
                return menu_data
            else:
                # If no JSON found, return structured text
                print(f"[MenuGenerator] No JSON found in response, returning as text")
                return {
                    'formato': 'texto',
                    'contenido': response
                }
            
        except json.JSONDecodeError as e:
            print(f"[MenuGenerator] JSON decode error: {str(e)}")
            print(f"[MenuGenerator] Attempted to parse: {json_str[:200] if json_str else 'None'}...")
            # If JSON parsing fails, return as text
            return {
                'formato': 'texto',
                'contenido': response
            }
        except Exception as e:
            print(f"[MenuGenerator] Error parsing menu response: {str(e)}")
            import traceback
            traceback.print_exc()
            # Return as text on any error
            return {
                'formato': 'texto',
                'contenido': response
            }
    
    def suggest_meal_improvements(self, meal_name: str, family_profiles: Dict) -> str:
        """Get AI suggestions to improve a specific meal for the family"""
        
        prompt = f"""Como nutricionista experto, sugiere mejoras para el plato "{meal_name}" 
considerando los perfiles de esta familia:

{json.dumps(family_profiles, indent=2, ensure_ascii=False)}

Proporciona:
1. Sustituciones de ingredientes para hacerlo más saludable
2. Adaptaciones para los niños
3. Variantes para diferentes restricciones dietéticas
4. Tips de presentación para hacerlo más atractivo

Sé breve y práctico."""
        
        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return message.content[0].text
            
        except Exception as e:
            return f"Error al generar sugerencias: {str(e)}"

import re
