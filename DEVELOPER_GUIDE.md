# 👨‍💻 Guía para Desarrolladores

Guía completa para desarrolladores que quieran contribuir o extender k[AI]tchen.

## 🚀 Configuración del Entorno de Desarrollo

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git (control de versiones)
- Editor de código (VS Code, PyCharm, etc.)

### Instalación

```bash
# 1. Clonar el repositorio
git clone <repository-url>
cd JAXOKITCHEN

# 2. Crear entorno virtual (recomendado)
python -m venv venv

# 3. Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Configurar variables de entorno
cp .env.example .env
# Editar .env y añadir tu ANTHROPIC_API_KEY

# 6. Inicializar base de datos
python init.py

# 7. Ejecutar servidor de desarrollo
python app.py
```

### Estructura del Proyecto

```
JAXOKITCHEN/
├── app.py                 # Servidor Flask principal
├── database.py            # Capa de acceso a datos
├── menu_generator.py      # Generador de menús con IA
├── recipe_extractor.py    # Extractor de recetas
├── init.py                # Script de inicialización
├── requirements.txt        # Dependencias Python
├── .env                   # Variables de entorno (no commitear)
├── .env.example           # Ejemplo de variables de entorno
├── Procfile               # Configuración Railway
├── railway.toml           # Configuración Railway
├── pytest.ini             # Configuración pytest
├── templates/             # Plantillas HTML
│   ├── index.html
│   ├── tv_display.html
│   ├── menu_visualizer.html
│   └── recipe_view.html
├── static/                # Archivos estáticos
│   ├── css/
│   └── js/
│       └── app.js
├── tests/                 # Tests automatizados
│   ├── test_database.py
│   ├── test_api.py
│   ├── test_menu_generator.py
│   └── test_recipe_extractor.py
└── docs/                  # Documentación adicional
    ├── API_DOCUMENTATION.md
    ├── ARCHITECTURE.md
    └── DEVELOPER_GUIDE.md
```

## 📝 Convenciones de Código

### Python

#### Estilo de Código

- Seguir **PEP 8** (guía de estilo de Python)
- Usar **type hints** en todas las funciones
- Documentar funciones con **docstrings** (formato Google)
- Máximo 100 caracteres por línea
- Usar **f-strings** en lugar de `.format()` o `%`

#### Ejemplo de Función Bien Documentada

```python
def add_adult(self, profile: Dict[str, Any]) -> int:
    """
    Añade un nuevo perfil de adulto a la base de datos.
    
    Args:
        profile: Diccionario con los datos del adulto. Debe incluir
                 al menos 'nombre'. Otros campos opcionales incluyen
                 'edad', 'objetivo_alimentario', etc.
    
    Returns:
        ID del adulto recién creado.
    
    Raises:
        ValueError: Si el nombre está vacío o es None.
        sqlite3.Error: Si hay un error de base de datos.
    """
    if not profile.get('nombre'):
        raise ValueError("El nombre es requerido")
    
    # ... código de implementación ...
    return adult_id
```

#### Nombres de Variables

- **snake_case** para variables y funciones
- **PascalCase** para clases
- **UPPER_CASE** para constantes
- Nombres descriptivos y en español para variables de dominio

#### Manejo de Errores

```python
# ✅ BIEN: Manejo específico de errores
try:
    result = db.add_recipe(recipe_data)
except sqlite3.IntegrityError as e:
    logger.error(f"Error de integridad: {e}")
    return jsonify({'success': False, 'error': 'Receta duplicada'}), 400
except Exception as e:
    logger.error(f"Error inesperado: {e}")
    return jsonify({'success': False, 'error': 'Error interno'}), 500

# ❌ MAL: Captura genérica sin logging
try:
    result = db.add_recipe(recipe_data)
except:
    return jsonify({'error': 'Error'}), 500
```

### JavaScript

#### Estilo de Código

- Usar **ES6+** (arrow functions, const/let, template literals)
- Preferir **const** sobre **let**, evitar **var**
- Usar **async/await** en lugar de `.then()`
- Máximo 100 caracteres por línea
- Comentarios en español para lógica de negocio

#### Ejemplo de Función Bien Escrita

```javascript
/**
 * Obtiene todos los perfiles de adultos desde la API
 * @returns {Promise<Array>} Array de perfiles de adultos
 */
async function fetchAdults() {
    try {
        const response = await fetchAPI('/api/adults');
        if (response.success) {
            return response.data;
        } else {
            console.error('Error al obtener adultos:', response.error);
            return [];
        }
    } catch (error) {
        console.error('Error de red:', error);
        showError('No se pudo conectar con el servidor');
        return [];
    }
}
```

## 🧪 Testing

### Ejecutar Tests

```bash
# Todos los tests
python run_tests.py

# Tests específicos
pytest tests/test_database.py -v

# Con cobertura
pytest tests/ --cov=. --cov-report=html

# Tests con output detallado
pytest tests/ -v -s
```

### Escribir Nuevos Tests

#### Estructura de un Test

```python
import pytest
from database import Database

def test_add_adult_success():
    """Test que añade un adulto correctamente"""
    db = Database()
    
    profile = {
        'nombre': 'Test User',
        'edad': 30,
        'objetivo_alimentario': 'Salud'
    }
    
    adult_id = db.add_adult(profile)
    
    assert adult_id is not None
    assert isinstance(adult_id, int)
    
    # Verificar que se guardó correctamente
    adults = db.get_all_adults()
    assert len(adults) > 0
    assert any(a['nombre'] == 'Test User' for a in adults)
```

#### Fixtures de pytest

```python
import pytest
from database import Database

@pytest.fixture
def db():
    """Fixture que proporciona una instancia de Database"""
    db = Database()
    # Setup: crear tablas si no existen
    db.init_database()
    yield db
    # Teardown: limpiar después del test
    # (opcional, dependiendo de si usas DB en memoria)

@pytest.fixture
def sample_adult():
    """Fixture con datos de ejemplo de adulto"""
    return {
        'nombre': 'María',
        'edad': 38,
        'objetivo_alimentario': 'Salud'
    }

def test_add_adult(db, sample_adult):
    """Test usando fixtures"""
    adult_id = db.add_adult(sample_adult)
    assert adult_id is not None
```

### Mocking de APIs Externas

```python
from unittest.mock import patch, MagicMock
from menu_generator import MenuGenerator

@patch('menu_generator.anthropic.Anthropic')
def test_generate_menu_success(mock_anthropic):
    """Test de generación de menú con mock de API"""
    # Configurar mock
    mock_client = MagicMock()
    mock_anthropic.return_value = mock_client
    
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text='{"menu": {...}}')]
    mock_client.messages.create.return_value = mock_response
    
    # Ejecutar test
    generator = MenuGenerator('fake-api-key')
    result = generator.generate_weekly_menu(
        adults=[], 
        children=[], 
        recipes=[]
    )
    
    # Verificar
    assert result['success'] == True
    mock_client.messages.create.assert_called_once()
```

## 🔧 Desarrollo de Nuevas Funcionalidades

### Proceso Recomendado

1. **Planificación**
   - Crear issue o documentar la funcionalidad
   - Diseñar la API si es necesario
   - Identificar cambios en base de datos

2. **Implementación**
   - Crear branch: `git checkout -b feature/nueva-funcionalidad`
   - Implementar backend primero
   - Añadir tests
   - Implementar frontend
   - Actualizar documentación

3. **Testing**
   - Ejecutar tests existentes
   - Escribir tests para nueva funcionalidad
   - Probar manualmente

4. **Revisión**
   - Revisar código propio
   - Verificar que sigue convenciones
   - Actualizar documentación

5. **Merge**
   - Merge a main/master
   - Tag de versión si es necesario

### Ejemplo: Añadir Nueva Funcionalidad

#### Paso 1: Añadir Endpoint en `app.py`

```python
@app.route('/api/recipes/favorite', methods=['POST'])
def favorite_recipe():
    """Marca una receta como favorita"""
    try:
        data = request.json
        recipe_id = data.get('recipe_id')
        favorite = data.get('favorite', True)
        
        if not recipe_id:
            return jsonify({
                'success': False,
                'error': 'recipe_id es requerido'
            }), 400
        
        success = db.set_recipe_favorite(recipe_id, favorite)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Receta marcada como favorita'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Receta no encontrada'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
```

#### Paso 2: Añadir Método en `database.py`

```python
def set_recipe_favorite(self, recipe_id: int, favorite: bool) -> bool:
    """
    Marca una receta como favorita o no favorita.
    
    Args:
        recipe_id: ID de la receta
        favorite: True para marcar como favorita, False para desmarcar
    
    Returns:
        True si se actualizó correctamente, False si la receta no existe
    """
    conn = self.get_connection()
    cursor = conn.cursor()
    
    try:
        # Primero verificar que existe
        cursor.execute('SELECT id FROM recipes WHERE id = ?', (recipe_id,))
        if not cursor.fetchone():
            return False
        
        # Actualizar (asumiendo que añadimos columna favorite)
        cursor.execute(
            'UPDATE recipes SET favorite = ? WHERE id = ?',
            (favorite, recipe_id)
        )
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        raise
    finally:
        self._close_connection(conn)
```

#### Paso 3: Migración de Base de Datos

```python
# En database.py, método init_database()
if self.is_postgres:
    cursor.execute('''
        ALTER TABLE recipes 
        ADD COLUMN IF NOT EXISTS favorite BOOLEAN DEFAULT FALSE
    ''')
else:
    # SQLite no soporta ALTER TABLE ADD COLUMN IF NOT EXISTS
    # Necesitamos verificar primero
    cursor.execute('PRAGMA table_info(recipes)')
    columns = [col[1] for col in cursor.fetchall()]
    if 'favorite' not in columns:
        cursor.execute('ALTER TABLE recipes ADD COLUMN favorite BOOLEAN DEFAULT 0')
```

#### Paso 4: Añadir Test

```python
def test_set_recipe_favorite(db):
    """Test de marcar receta como favorita"""
    # Añadir receta de prueba
    recipe_data = {
        'title': 'Test Recipe',
        'ingredients': '[]',
        'instructions': 'Test instructions'
    }
    recipe_id = db.add_recipe(recipe_data)
    
    # Marcar como favorita
    success = db.set_recipe_favorite(recipe_id, True)
    assert success == True
    
    # Verificar
    recipes = db.get_all_recipes()
    recipe = next(r for r in recipes if r['id'] == recipe_id)
    assert recipe['favorite'] == True
```

#### Paso 5: Actualizar Frontend

```javascript
// En static/js/app.js
async function toggleRecipeFavorite(recipeId, favorite) {
    try {
        const response = await fetchAPI('/api/recipes/favorite', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                recipe_id: recipeId,
                favorite: favorite
            })
        });
        
        if (response.success) {
            showSuccess('Receta actualizada');
            loadRecipes(); // Recargar lista
        } else {
            showError(response.error);
        }
    } catch (error) {
        showError('Error al actualizar receta');
    }
}
```

## 🐛 Debugging

### Logging

```python
import logging

# Configurar logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Usar en código
logger.debug('Detalle de debug')
logger.info('Información general')
logger.warning('Advertencia')
logger.error('Error')
logger.critical('Error crítico')
```

### Debug en Flask

```python
# En app.py, para desarrollo
if __name__ == '__main__':
    app.run(debug=True)  # Activa debug mode
```

### Debug en JavaScript

```javascript
// Usar console para debugging
console.log('Valor:', value);
console.error('Error:', error);
console.table(arrayData); // Para arrays/objetos

// Debugger (pausa ejecución)
debugger; // El navegador se detendrá aquí si DevTools está abierto
```

### Inspeccionar Base de Datos

```bash
# SQLite
sqlite3 family_kitchen.db
.tables
SELECT * FROM adults;
.schema adults

# PostgreSQL (Railway)
railway run psql $DATABASE_URL
\dt  # Listar tablas
SELECT * FROM adults;
\d adults  # Ver esquema
```

## 📦 Gestión de Dependencias

### Añadir Nueva Dependencia

```bash
# 1. Instalar
pip install nueva-dependencia

# 2. Actualizar requirements.txt
pip freeze > requirements.txt

# 3. Verificar versión específica
pip install nueva-dependencia==1.2.3
```

### Actualizar Dependencias

```bash
# Verificar versiones disponibles
pip list --outdated

# Actualizar una específica
pip install --upgrade nombre-paquete

# Actualizar todas (cuidado)
pip install --upgrade -r requirements.txt
```

## 🚢 Deployment

### Pre-Deployment Checklist

- [ ] Todas las variables de entorno configuradas
- [ ] Base de datos migrada (si hay cambios)
- [ ] Tests pasando
- [ ] Documentación actualizada
- [ ] Logs revisados
- [ ] Backup de base de datos (producción)

### Railway Deployment

```bash
# 1. Instalar Railway CLI
npm i -g @railway/cli

# 2. Login
railway login

# 3. Link proyecto
railway link

# 4. Deploy
railway up

# 5. Ver logs
railway logs

# 6. Ver variables de entorno
railway variables
```

## 📚 Recursos Útiles

### Documentación Externa

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Anthropic Claude API](https://docs.anthropic.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Pytest Documentation](https://docs.pytest.org/)

### Herramientas Recomendadas

- **Postman/Insomnia**: Para probar APIs
- **DB Browser for SQLite**: Para inspeccionar base de datos local
- **VS Code**: Editor recomendado con extensiones Python
- **Git**: Control de versiones

## ❓ Preguntas Frecuentes

### ¿Cómo añado un nuevo campo a un perfil?

1. Añadir columna en `database.py` → `init_database()`
2. Actualizar método `add_adult()` o `add_child()`
3. Actualizar formulario en `templates/index.html`
4. Actualizar JavaScript en `static/js/app.js`
5. Migrar datos existentes si es necesario

### ¿Cómo cambio el modelo de IA?

Editar `menu_generator.py`:
```python
# Cambiar modelo
response = self.client.messages.create(
    model="claude-sonnet-4-20250514",  # Cambiar aquí
    # ...
)
```

### ¿Cómo añado soporte para otro sitio de recetas?

Editar `recipe_extractor.py`:
```python
def _extract_from_nuevo_sitio(self, soup, url):
    """Extracción específica para nuevo sitio"""
    # Lógica de extracción
    pass
```

---

## 🤝 Contribuir

Ver [CONTRIBUTING.md](CONTRIBUTING.md) para guía completa de contribución.

---

**¡Feliz desarrollo! 🚀**
