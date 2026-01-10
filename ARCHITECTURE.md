# 🏗️ Arquitectura del Sistema

Documentación técnica detallada de la arquitectura de k[AI]tchen.

## 📐 Visión General

k[AI]tchen es una aplicación web full-stack construida con Flask (backend) y JavaScript vanilla (frontend), diseñada para generar menús semanales personalizados usando inteligencia artificial.

```
┌─────────────────────────────────────────────────────────────┐
│                        CLIENTE                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Navegador   │  │   TV/Tablet  │  │   Móvil      │      │
│  │ (Admin UI)   │  │  (TV View)   │  │  (Mobile)    │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
└─────────┼─────────────────┼─────────────────┼──────────────┘
          │                 │                 │
          └─────────────────┼─────────────────┘
                            │
          ┌─────────────────▼─────────────────┐
          │      FLASK SERVER (app.py)         │
          │  ┌──────────────────────────────┐ │
          │  │   REST API Endpoints         │ │
          │  │   - /api/adults              │ │
          │  │   - /api/children            │ │
          │  │   - /api/recipes             │ │
          │  │   - /api/menu/generate       │ │
          │  └──────────────────────────────┘ │
          └─────────────────┬─────────────────┘
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
    ┌─────▼─────┐   ┌──────▼──────┐   ┌─────▼─────┐
    │ Database  │   │   Claude    │   │  Recipe   │
    │  Layer    │   │     AI      │   │ Extractor │
    │(database.py)│   │(menu_gen.py)│   │(extractor)│
    └─────┬─────┘   └──────┬──────┘   └─────┬─────┘
          │                 │                 │
    ┌─────▼─────────────────▼─────────────────▼─────┐
    │           SQLite (Local) / PostgreSQL          │
    │              (Production - Railway)             │
    └────────────────────────────────────────────────┘
```

## 🔧 Componentes Principales

### 1. Backend (Flask)

#### `app.py` - Servidor Principal

**Responsabilidades**:
- Configuración de Flask y CORS
- Definición de rutas web y API
- Manejo de errores HTTP
- Inicialización de componentes

**Estructura**:
```python
app.py
├── Configuración
│   ├── Flask app initialization
│   ├── CORS configuration
│   └── Error handlers
├── Rutas Web
│   ├── / (admin interface)
│   ├── /tv (TV display)
│   └── /menu/visualizer
├── API Endpoints
│   ├── /api/adults (CRUD)
│   ├── /api/children (CRUD)
│   ├── /api/recipes (CRUD + extract)
│   ├── /api/menu/* (generate, get, rate)
│   └── /api/settings
└── Inicialización
    └── Server startup
```

**Características clave**:
- Lazy loading del `MenuGenerator` (solo se inicializa cuando se necesita)
- Manejo de errores JSON para rutas API
- Soporte para múltiples orígenes CORS
- Variables de entorno para configuración

#### `database.py` - Capa de Datos

**Responsabilidades**:
- Abstracción de base de datos (SQLite/PostgreSQL)
- CRUD operations para todas las entidades
- Gestión de conexiones y pools
- Migraciones automáticas de esquema

**Arquitectura**:
```python
Database
├── __init__()
│   ├── Detect database type (SQLite/PostgreSQL)
│   ├── Initialize connection pool
│   └── Create tables if not exist
├── Adults Management
│   ├── add_adult()
│   ├── get_all_adults()
│   └── delete_adult()
├── Children Management
│   ├── add_child()
│   ├── get_all_children()
│   └── delete_child()
├── Recipes Management
│   ├── add_recipe()
│   ├── get_all_recipes()
│   ├── delete_recipe()
│   └── _find_recipe_by_title()
├── Menus Management
│   ├── save_weekly_menu()
│   ├── get_latest_menu()
│   ├── get_menu_by_week_start()
│   ├── get_all_menus()
│   └── extract_and_save_recipes_from_menu()
└── Ratings & Preferences
    ├── rate_menu_day()
    ├── get_menu_day_rating()
    ├── get_all_menu_ratings()
    ├── save_menu_preferences()
    └── get_menu_preferences()
```

**Patrón de Diseño**: Repository Pattern

**Ventajas**:
- Cambio fácil entre SQLite y PostgreSQL
- Código de negocio desacoplado de la base de datos
- Fácil testing con mocks

#### `menu_generator.py` - Generador de Menús con IA

**Responsabilidades**:
- Comunicación con API de Anthropic Claude
- Construcción de prompts personalizados
- Parsing de respuestas JSON
- Manejo de errores y timeouts

**Flujo de Generación**:
```
1. Recibir perfiles familiares
   ↓
2. Construir prompt detallado
   ├── Preferencias de adultos
   ├── Preferencias de niños
   ├── Recetas disponibles
   ├── Configuración de días
   └── Ratings históricos
   ↓
3. Llamar a Claude API
   ├── Timeout: 5 minutos
   ├── Model: claude-sonnet-4-20250514
   └── Max tokens: 8000
   ↓
4. Parsear respuesta JSON
   ├── Validar estructura
   ├── Reparar JSON si es necesario
   └── Extraer datos del menú
   ↓
5. Retornar menú estructurado
```

**Características**:
- Prompts dinámicos basados en perfiles
- Aprendizaje de ratings históricos
- Manejo robusto de errores JSON
- Soporte para regeneración de días individuales

#### `recipe_extractor.py` - Extractor de Recetas

**Responsabilidades**:
- Web scraping de URLs de recetas
- Extracción de datos estructurados
- Manejo de múltiples formatos
- Soporte para Pinterest y otros sitios

**Estrategia de Extracción**:
```
1. Detectar tipo de URL
   ├── Pinterest → Seguir redirects
   └── Directa → Continuar
   ↓
2. Intentar extracción estructurada
   ├── JSON-LD (Schema.org)
   ├── Microdata
   └── Open Graph
   ↓
3. Si falla, extracción manual
   ├── BeautifulSoup parsing
   ├── Buscar patrones comunes
   └── Trafilatura para texto
   ↓
4. Normalizar datos
   ├── Limpiar ingredientes
   ├── Formatear instrucciones
   └── Extraer metadatos
   ↓
5. Retornar datos estructurados
```

**Características**:
- Soporte para múltiples sitios web
- Manejo de errores robusto
- Extracción por lotes
- Cache de resultados (futuro)

### 2. Frontend (Vanilla JavaScript)

#### `static/js/app.js` - Lógica del Cliente

**Estructura**:
```javascript
app.js
├── State Management
│   ├── Global state object
│   └── State update functions
├── API Client
│   ├── fetchAPI() - Generic fetch wrapper
│   ├── CRUD operations
│   └── Error handling
├── UI Components
│   ├── Profile forms
│   ├── Recipe extractor
│   ├── Menu display
│   └── Settings panel
├── Event Handlers
│   ├── Form submissions
│   ├── Button clicks
│   └── Tab navigation
└── Utilities
    ├── Date formatting
    ├── Data validation
    └── DOM manipulation
```

**Patrón**: MVC (Model-View-Controller) simplificado

**Características**:
- Sin dependencias externas (vanilla JS)
- Manejo de estado centralizado
- Actualización reactiva de UI
- Manejo de errores user-friendly

#### Templates HTML

**`templates/index.html`** - Interfaz de Administración
- 4 pestañas principales: Familia, Recetas, Menú, Vista TV
- Formularios dinámicos para perfiles
- Visualización de datos en tablas
- Configuración de preferencias

**`templates/tv_display.html`** - Vista para TV
- Diseño optimizado para pantallas grandes
- Auto-refresh cada 5 minutos
- Navegación por días
- Estilos grandes y legibles

**`templates/menu_visualizer.html`** - Visualizador de Menús
- Vista detallada de menús
- Navegación semanal
- Ratings y feedback

## 🗄️ Base de Datos

### Esquema de Datos

#### Tabla: `adults`
```sql
CREATE TABLE adults (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    edad INTEGER,
    objetivo_alimentario TEXT,
    estilo_alimentacion TEXT,
    cocinas_favoritas TEXT,
    nivel_picante TEXT,
    ingredientes_favoritos TEXT,
    ingredientes_no_gustan TEXT,
    alergias TEXT,
    intolerancias TEXT,
    restricciones_religiosas TEXT,
    flexibilidad_comer TEXT,
    preocupacion_principal TEXT,
    tiempo_max_cocinar INTEGER,
    nivel_cocina TEXT,
    tipo_desayuno TEXT,
    le_gustan_snacks BOOLEAN,
    plato_favorito TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Tabla: `children`
```sql
CREATE TABLE children (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    edad INTEGER,
    nivel_exigencia TEXT,
    ingredientes_acepta TEXT,
    ingredientes_rechaza TEXT,
    texturas_no_gusta TEXT,
    alergias TEXT,
    intolerancias TEXT,
    preferencias_comida TEXT,
    comida_favorita TEXT,
    comida_rechaza TEXT,
    nivel_actividad TEXT,
    apetito TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Tabla: `recipes`
```sql
CREATE TABLE recipes (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    url TEXT,
    ingredients TEXT,  -- JSON array
    instructions TEXT,
    prep_time INTEGER,
    cook_time INTEGER,
    servings INTEGER,
    cuisine_type TEXT,
    meal_type TEXT,
    difficulty TEXT,
    image_url TEXT,
    extracted_data TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Tabla: `weekly_menus`
```sql
CREATE TABLE weekly_menus (
    id INTEGER PRIMARY KEY,
    week_start_date DATE NOT NULL UNIQUE,
    menu_data TEXT NOT NULL,  -- JSON
    metadata TEXT,  -- JSON
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Tabla: `menu_ratings`
```sql
CREATE TABLE menu_ratings (
    id INTEGER PRIMARY KEY,
    menu_id INTEGER,
    week_start_date DATE,
    day_name TEXT,
    menu_type TEXT,  -- 'adultos' or 'ninos'
    rating INTEGER CHECK(rating >= 1 AND rating <= 5),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (menu_id) REFERENCES weekly_menus(id)
);
```

#### Tabla: `menu_preferences`
```sql
CREATE TABLE menu_preferences (
    id INTEGER PRIMARY KEY,
    preferences TEXT NOT NULL,  -- JSON
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Relaciones

```
weekly_menus (1) ──< (N) menu_ratings
```

## 🔄 Flujos de Datos

### Flujo 1: Generación de Menú

```
Usuario → Frontend → POST /api/menu/generate
                        ↓
                    app.py (endpoint handler)
                        ↓
                    Database.get_all_adults()
                    Database.get_all_children()
                    Database.get_all_recipes()
                        ↓
                    MenuGenerator.generate_weekly_menu()
                        ↓
                    Claude API (HTTP Request)
                        ↓
                    Parse JSON Response
                        ↓
                    Database.save_weekly_menu()
                        ↓
                    Return JSON to Frontend
                        ↓
                    Update UI
```

### Flujo 2: Extracción de Receta

```
Usuario → Frontend → POST /api/recipes/extract
                        ↓
                    app.py (endpoint handler)
                        ↓
                    RecipeExtractor.extract_from_url()
                        ↓
                    HTTP GET to recipe URL
                        ↓
                    BeautifulSoup + Trafilatura parsing
                        ↓
                    Database.add_recipe()
                        ↓
                    Return JSON to Frontend
                        ↓
                    Display recipe in UI
```

### Flujo 3: Visualización en TV

```
TV Browser → GET /tv
                ↓
            Render tv_display.html
                ↓
            JavaScript loads menu
                ↓
            GET /api/menu/current-week
                ↓
            Display menu in large format
                ↓
            Auto-refresh every 5 minutes
```

## 🔐 Seguridad

### Variables de Entorno

Todas las configuraciones sensibles están en `.env`:
- `ANTHROPIC_API_KEY`: API key de Anthropic (nunca commitear)
- `SECRET_KEY`: Clave secreta para sesiones Flask
- `DATABASE_URL`: URL de base de datos (con credenciales)
- `CORS_ORIGINS`: Orígenes permitidos para CORS

### Validación de Datos

- Validación en backend de todos los inputs
- Sanitización de URLs antes de scraping
- Validación de tipos de datos
- Límites en tamaños de datos

### Endpoints Protegidos

Algunos endpoints solo están disponibles desde localhost:
- `/api/temp/get-api-key`
- `/api/temp/save-api-key-to-env`
- `/recover-api-key`

## 🚀 Deployment

### Desarrollo Local

```bash
python app.py
# Servidor en http://localhost:7000
```

### Producción (Railway)

```
Railway Platform
├── Build: pip install -r requirements.txt
├── Start: gunicorn app:app
├── Database: PostgreSQL (proporcionado por Railway)
└── Environment: Variables desde Railway dashboard
```

**Configuración**:
- `FLASK_ENV=production`
- `PORT`: Automático desde Railway
- `DATABASE_URL`: PostgreSQL de Railway
- Workers: 2 (configurado en Procfile)

## 📊 Escalabilidad

### Limitaciones Actuales

- **Base de datos**: SQLite en desarrollo (no escalable)
- **Servidor**: Single-threaded Flask en desarrollo
- **API**: Sin rate limiting
- **Cache**: Sin sistema de cache

### Mejoras Futuras

1. **Base de datos**: Ya soporta PostgreSQL (usar en producción)
2. **Cache**: Implementar Redis para:
   - Cache de recetas extraídas
   - Cache de menús generados
   - Session storage
3. **Rate Limiting**: Implementar límites de API
4. **CDN**: Para assets estáticos
5. **Queue System**: Para procesamiento asíncrono de:
   - Extracción de recetas
   - Generación de menús

## 🧪 Testing

### Estructura de Tests

```
tests/
├── test_database.py      # Tests de base de datos
├── test_api.py           # Tests de endpoints API
├── test_menu_generator.py # Tests de generación de menús
└── test_recipe_extractor.py # Tests de extracción
```

### Cobertura

- Backend: 18 tests
- Frontend: 7 tests (mocks)
- Total: 25 tests automáticos

## 📈 Monitoreo

### Logs

El sistema genera logs en:
- Console (desarrollo)
- Railway logs (producción)

### Métricas Recomendadas

- Tiempo de respuesta de API
- Tasa de éxito de extracción de recetas
- Tiempo de generación de menús
- Uso de memoria y CPU
- Errores de base de datos

## 🔄 Mantenimiento

### Tareas Regulares

1. **Backup de base de datos**: Diario (en producción)
2. **Limpieza de menús antiguos**: Mensual (opcional)
3. **Actualización de dependencias**: Mensual
4. **Revisión de logs**: Semanal

### Migraciones

Las migraciones de esquema se hacen automáticamente en `database.py` usando `CREATE TABLE IF NOT EXISTS`. Para cambios de esquema:

1. Modificar `init_database()` en `database.py`
2. Añadir lógica de migración si es necesario
3. Probar en desarrollo antes de producción

---

## 📚 Referencias

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Anthropic Claude API](https://docs.anthropic.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Railway Documentation](https://docs.railway.app/)
