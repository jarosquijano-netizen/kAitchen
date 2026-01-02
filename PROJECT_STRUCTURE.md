# Estructura del Proyecto - k[AI]tchen

Este documento describe la estructura completa del proyecto y el propósito de cada componente.

## 📂 Estructura de Directorios

```
JAXOKITCHEN/
├── 📄 Archivos Principales
│   ├── app.py                    # Servidor Flask principal y rutas API
│   ├── database.py               # Gestión de base de datos (SQLite/PostgreSQL)
│   ├── menu_generator.py         # Generador de menús con IA (Claude)
│   ├── recipe_extractor.py       # Extracción de recetas desde URLs web
│   ├── init.py                   # Script de inicialización de BD
│   ├── setup.py                  # Script de configuración inicial
│   ├── run_tests.py              # Ejecutor de tests automáticos
│   └── pytest.ini                # Configuración de pytest
│
├── 📋 Configuración
│   ├── requirements.txt          # Dependencias Python
│   ├── Procfile                  # Configuración para Railway
│   ├── railway.toml              # Configuración de Railway
│   ├── .env                      # Variables de entorno (NO COMMIT)
│   └── .env.example              # Ejemplo de variables de entorno
│
├── 🧪 Tests
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_database.py      # Tests de operaciones de BD
│   │   ├── test_api.py           # Tests de endpoints Flask
│   │   ├── test_menu_generator.py # Tests del generador de menús
│   │   ├── test_frontend.js      # Tests del frontend
│   │   └── README.md             # Documentación de tests
│   └── .github/workflows/
│       └── tests.yml             # CI/CD para GitHub Actions
│
├── 🌐 Frontend
│   ├── templates/
│   │   ├── index.html            # Interfaz principal de administración
│   │   ├── tv_display.html       # Vista optimizada para TV
│   │   ├── menu_visualizer.html  # Visualizador de menús
│   │   └── recover_api_key.html  # Página de recuperación de API key
│   └── static/
│       ├── css/                  # Estilos CSS
│       └── js/
│           └── app.js            # Lógica JavaScript del frontend
│
├── 📚 Documentación
│   ├── README.md                 # Documentación principal
│   ├── README_GITHUB.md          # README para GitHub
│   ├── TESTING.md                # Guía de testing
│   ├── CONTRIBUTING.md           # Guía de contribución
│   ├── PROJECT_STRUCTURE.md      # Este archivo
│   ├── START_HERE.md             # Guía de inicio rápido
│   ├── RAILWAY_DEPLOYMENT.md     # Guía de deploy en Railway
│   ├── CURSOR_WORKFLOW.md        # Workflow con Cursor
│   ├── GUIA_RAPIDA.md            # Guía rápida en español
│   ├── GUIA_VISUAL.md            # Guía visual
│   └── BUILD_SUMMARY.md          # Resumen de construcción
│
└── 🗄️ Base de Datos
    └── family_kitchen.db         # Base de datos SQLite (se crea automáticamente)
```

## 📄 Descripción de Archivos Principales

### Backend

#### `app.py`
- **Propósito**: Servidor Flask principal
- **Contiene**:
  - Configuración de Flask y CORS
  - Rutas web (/, /tv, /menu/visualizer)
  - Endpoints API (/api/adults, /api/children, /api/menu/generate, etc.)
  - Manejo de errores
  - Inicialización del servidor

#### `database.py`
- **Propósito**: Capa de abstracción para base de datos
- **Contiene**:
  - Clase `Database` con soporte para SQLite y PostgreSQL
  - Métodos CRUD para adultos, niños, recetas y menús
  - Gestión de preferencias de menú
  - Inicialización automática de tablas

#### `menu_generator.py`
- **Propósito**: Generación de menús semanales usando Claude AI
- **Contiene**:
  - Clase `MenuGenerator`
  - Construcción de prompts personalizados
  - Parsing de respuestas JSON de Claude
  - Normalización de listas de compras

#### `recipe_extractor.py`
- **Propósito**: Extracción de recetas desde URLs web
- **Contiene**:
  - Scraping con BeautifulSoup y Trafilatura
  - Detección de ingredientes e instrucciones
  - Soporte para múltiples formatos de sitios web

### Frontend

#### `templates/index.html`
- **Propósito**: Interfaz principal de administración
- **Contiene**:
  - Gestión de perfiles familiares
  - Extracción de recetas
  - Generación de menús
  - Configuración del sistema

#### `static/js/app.js`
- **Propósito**: Lógica JavaScript del frontend
- **Contiene**:
  - Comunicación con API
  - Renderizado de perfiles y menús
  - Manejo de formularios
  - Utilidades de UI

### Testing

#### `tests/test_database.py`
- **Tests**: Operaciones de base de datos
- **Cubre**: CRUD de adultos, niños, preferencias

#### `tests/test_api.py`
- **Tests**: Endpoints de la API Flask
- **Cubre**: GET, POST, DELETE de todos los recursos

#### `tests/test_menu_generator.py`
- **Tests**: Generador de menús
- **Cubre**: Inicialización y estructura de menús generados

#### `tests/test_frontend.js`
- **Tests**: Funcionalidad del frontend
- **Cubre**: Mock API y utilidades

### Scripts

#### `run_tests.py`
- **Propósito**: Ejecutar todos los tests automáticamente
- **Uso**: `python run_tests.py`

#### `init_all_tables.py`
- **Propósito**: Crear todas las tablas necesarias en la BD
- **Uso**: `python init_all_tables.py`

#### `setup.py`
- **Propósito**: Configuración inicial del proyecto
- **Uso**: `python setup.py`

## 🔄 Flujo de Datos

```
Usuario (Frontend)
    ↓
API Endpoints (app.py)
    ↓
Database Layer (database.py)
    ↓
SQLite/PostgreSQL
```

```
Generación de Menú:
    Frontend → API → MenuGenerator → Claude API → Parse → Database → Frontend
```

## 🧪 Sistema de Testing

```
tests/
├── Backend (Python/pytest)
│   ├── test_database.py      # 7 tests
│   ├── test_api.py           # 9 tests
│   └── test_menu_generator.py # 2 tests
│
└── Frontend (JavaScript)
    └── test_frontend.js      # 7 tests

Total: 25 tests automáticos
```

## 📦 Dependencias Principales

### Backend
- `flask==3.0.0` - Framework web
- `anthropic>=0.40.0` - API de Claude
- `beautifulsoup4==4.12.3` - Web scraping
- `pytest==7.4.3` - Testing framework

### Frontend
- Vanilla JavaScript (sin frameworks)
- Fetch API para comunicación con backend

## 🔐 Archivos Sensibles

**NO COMMITEAR**:
- `.env` - Contiene API keys y secretos
- `family_kitchen.db` - Base de datos local (puede contener datos personales)
- `*.pyc`, `__pycache__/` - Archivos compilados de Python

## 📝 Convenciones de Nombres

- **Python**: snake_case para funciones y variables
- **JavaScript**: camelCase para funciones y variables
- **Archivos**: lowercase con guiones bajos
- **Clases**: PascalCase
- **Constantes**: UPPER_SNAKE_CASE

## 🚀 Comandos Útiles

```bash
# Desarrollo
python app.py                    # Iniciar servidor
python init_all_tables.py        # Crear tablas
python setup.py                 # Configuración inicial

# Testing
python run_tests.py              # Todos los tests
pytest tests/ -v                # Solo backend
node tests/test_frontend.js     # Solo frontend

# Base de datos
python -c "from database import Database; db = Database()"  # Inicializar BD
```

## 📚 Documentación Relacionada

- [README.md](README.md) - Documentación principal
- [TESTING.md](TESTING.md) - Guía de testing
- [CONTRIBUTING.md](CONTRIBUTING.md) - Guía de contribución
- [START_HERE.md](START_HERE.md) - Inicio rápido

---

**Última actualización**: 2025-01-02
