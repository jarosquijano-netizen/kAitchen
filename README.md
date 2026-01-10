# 🍳 k[AI]tchen - Sistema de Gestión de Menús Familiares

Sistema inteligente de planificación de comidas para familias, con generación automática de menús personalizados usando IA y visualización optimizada para TV de cocina.

## 🌟 Características

### ✨ Funcionalidades Principales

- **Perfiles Familiares Detallados**: Gestiona perfiles individuales para adultos y niños con:
  - Preferencias alimentarias
  - Alergias e intolerancias
  - Ingredientes favoritos y rechazados
  - Objetivos nutricionales
  - Nivel de exigencia (niños)

- **Extracción Automática de Recetas**: 
  - Extrae recetas desde cualquier URL web
  - Detecta automáticamente ingredientes e instrucciones
  - Soporta múltiples formatos y sitios web
  - Almacenamiento en base de datos local

- **Generación Inteligente de Menús con IA**:
  - Usa Claude (Anthropic) para generar menús semanales
  - Considera TODAS las preferencias y restricciones familiares
  - Balance nutricional automático
  - Adaptaciones para cada miembro de la familia
  - Lista de compra generada automáticamente

- **Vista TV-Friendly**:
  - Interfaz optimizada para pantallas grandes
  - Visualización clara desde la distancia
  - Actualización automática
  - Navegación semanal

## 📋 Requisitos

- Python 3.8+
- Cuenta de Anthropic (para generación de menús con IA)
- Navegador web moderno
- (Opcional) TV inteligente o dispositivo de streaming para la vista de cocina

## 🚀 Instalación

### 1. Clonar o descargar el proyecto

```bash
cd /home/claude
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# Editar .env y añadir tu API key de Anthropic
# ANTHROPIC_API_KEY=tu_api_key_aqui
```

Para obtener una API key de Anthropic:
1. Visita https://console.anthropic.com/
2. Crea una cuenta o inicia sesión
3. Ve a la sección "API Keys"
4. Crea una nueva API key
5. Copia la key al archivo .env

### 4. Inicializar la base de datos

```bash
python init.py
```

Este script:
- Crea la base de datos SQLite
- Opcionalmente añade perfiles de ejemplo
- Verifica la configuración de la API key

## 💻 Uso

### Iniciar el Servidor

```bash
python app.py
```

El servidor se iniciará en http://localhost:7000

### Interfaces Disponibles

#### 1. Panel de Administración
**URL**: http://localhost:7000

Funciones:
- ✅ Gestionar perfiles de adultos y niños
- ✅ Extraer recetas desde URLs
- ✅ Generar menús semanales con IA
- ✅ Ver y gestionar menús generados
- ✅ Calificar días del menú
- ✅ Regenerar días específicos

#### 2. Vista de TV
**URL**: http://localhost:7000/tv

Características:
- 📺 Diseño optimizado para pantallas grandes
- 🔄 Actualización automática cada 5 minutos
- 📅 Navegación por días de la semana
- 🎨 Interfaz atractiva y fácil de leer desde lejos

## 📱 Guía de Uso Rápido

### 1. Configurar Perfiles Familiares

1. Ve a la pestaña "Familia"
2. Añade perfiles para cada adulto:
   - Nombre, edad
   - Objetivo alimentario
   - Preferencias culinarias
   - Alergias e intolerancias
   - Ingredientes favoritos y rechazados

3. Añade perfiles para cada niño:
   - Nombre, edad
   - Nivel de exigencia
   - Ingredientes que acepta/rechaza
   - Texturas que no le gustan
   - Alergias e intolerancias

### 2. Añadir Recetas (Opcional)

1. Ve a la pestaña "Recetas"
2. Pega la URL de una receta
3. Haz clic en "Extraer Receta"
4. El sistema extraerá automáticamente:
   - Título
   - Ingredientes
   - Instrucciones
   - Tiempo de preparación

**Ejemplo de URLs compatibles**:
- Blogs de cocina españoles (Recetas de Rechupete, Anna Recetas)
- Sitios internacionales (AllRecipes, Food Network)
- Blogs personales con recetas estructuradas

### 3. Generar Menú Semanal

1. Ve a la pestaña "Menú Semanal"
2. Haz clic en "✨ Generar Menú con IA"
3. Espera 15-30 segundos
4. El sistema generará un menú que considera:
   - Todas las preferencias familiares
   - Alergias e intolerancias
   - Balance nutricional
   - Variedad de ingredientes
   - Facilidad de preparación

### 4. Ver en TV de Cocina

1. Ve a la pestaña "Vista TV"
2. Copia la URL mostrada
3. Abre esa URL en el navegador de tu TV
4. El menú se mostrará en formato grande y claro

**Tip**: Si tu TV tiene navegador web, simplemente accede desde ahí. Si no, usa un Chromecast, Fire TV Stick, o cualquier dispositivo de streaming.

## 🏗️ Arquitectura del Sistema

```
family-kitchen-menu/
├── app.py                 # Servidor Flask principal
├── database.py            # Gestión de base de datos SQLite
├── recipe_extractor.py    # Extracción de recetas desde URLs
├── menu_generator.py      # Generador de menús con IA (Claude)
├── init.py               # Script de inicialización
├── requirements.txt       # Dependencias Python
├── .env.example          # Ejemplo de configuración
├── templates/
│   ├── index.html        # Interfaz de administración
│   └── tv_display.html   # Vista para TV
├── static/
│   └── js/
│       └── app.js        # Lógica frontend
└── family_kitchen.db     # Base de datos SQLite (se crea automáticamente)
```

## 🔧 API Endpoints

La aplicación expone una API REST completa. Para documentación detallada, consulta **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)**.

### Endpoints Principales

**Perfiles de Adultos**
- `GET /api/adults` - Obtener todos los adultos
- `POST /api/adults` - Añadir adulto
- `DELETE /api/adults/<id>` - Eliminar adulto

**Perfiles de Niños**
- `GET /api/children` - Obtener todos los niños
- `POST /api/children` - Añadir niño
- `DELETE /api/children/<id>` - Eliminar niño

**Recetas**
- `GET /api/recipes` - Obtener todas las recetas
- `POST /api/recipes/extract` - Extraer receta desde URL
- `POST /api/recipes/batch` - Extraer múltiples recetas
- `GET /api/recipes/search` - Buscar receta por título
- `DELETE /api/recipes/<id>` - Eliminar receta

**Menús**
- `POST /api/menu/generate` - Generar menú semanal con IA
- `GET /api/menu/latest` - Obtener último menú generado
- `GET /api/menu/current-week` - Obtener menú de la semana actual
- `GET /api/menu/week/<date>` - Obtener menú de semana específica
- `GET /api/menu/all` - Obtener todos los menús
- `POST /api/menu/rate-day` - Calificar un día del menú
- `POST /api/menu/regenerate-day` - Regenerar un día específico

**Configuración**
- `GET /api/settings` - Obtener configuración actual
- `POST /api/settings` - Guardar configuración
- `POST /api/settings/test` - Probar API key

Ver **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** para documentación completa con ejemplos.

## 🎨 Personalización

### Modificar Estilos de la Vista TV

Edita `templates/tv_display.html`:
- Cambia los colores en las variables CSS
- Ajusta tamaños de fuente
- Modifica el layout de las tarjetas

### Añadir Nuevas Fuentes de Recetas

Edita `recipe_extractor.py`:
- Añade patrones de extracción específicos para nuevos sitios
- Mejora la detección de ingredientes
- Añade soporte para nuevos formatos

### Personalizar Prompts de IA

Edita `menu_generator.py`:
- Modifica el prompt base en `_build_menu_prompt()`
- Añade restricciones adicionales
- Ajusta el formato de salida

## 🐛 Solución de Problemas

### Error: "ANTHROPIC_API_KEY no configurada"
**Solución**: 
1. Verifica que el archivo `.env` existe
2. Asegúrate de que contiene `ANTHROPIC_API_KEY=tu_key_real`
3. Reinicia el servidor

### Las recetas no se extraen correctamente
**Solución**:
- Verifica que la URL es accesible
- Algunos sitios bloquean scraping - prueba con URLs diferentes
- Usa el modo de extracción por lotes para múltiples URLs

### El menú no se muestra en la TV
**Solución**:
1. Verifica que el servidor está corriendo
2. Usa la IP local de tu ordenador en lugar de localhost
   - Ejemplo: `http://192.168.1.100:7000/tv`
3. Asegúrate de que la TV y el ordenador están en la misma red
4. Verifica la configuración de CORS si accedes desde otro dispositivo

### Error de conexión a la base de datos
**Solución**:
```bash
# Eliminar y recrear la base de datos
rm family_kitchen.db
python init.py
```

## 🔐 Seguridad

- ⚠️ **NO** compartas tu archivo `.env` con tu API key
- El sistema es para uso local/doméstico
- Si expones a Internet, añade autenticación
- La API key de Anthropic tiene costos asociados

## 💡 Consejos y Mejores Prácticas

### Para Mejores Resultados de IA:

1. **Perfiles Detallados**: Cuanto más detalle añadas a los perfiles, mejor será el menú generado
2. **Especifica Alergias**: Siempre marca claramente las alergias para evitar ingredientes peligrosos
3. **Sé Realista**: Indica tiempos de cocina realistas según tu disponibilidad
4. **Actualiza Regularmente**: Revisa y actualiza las preferencias de los niños (cambian con el tiempo)

### Para la Vista de TV:

1. **Full Screen**: Usa modo pantalla completa (F11 en la mayoría de navegadores)
2. **Evita Sleep**: Configura la TV para que no se apague automáticamente
3. **Bookmark**: Guarda la URL como favorito para acceso rápido

### Para Recetas:

1. **Fuentes Confiables**: Usa blogs y sitios de recetas conocidos
2. **Recetas Estructuradas**: Los sitios con Schema.org funcionan mejor
3. **Batch Extract**: Si tienes varias recetas de un sitio, usa extracción por lotes

## 🧪 Testing

El proyecto incluye un sistema completo de testing automático para prevenir errores:

### Ejecutar Tests

```bash
# Todos los tests
python run_tests.py

# Solo backend
pytest tests/ -v

# Solo frontend
node tests/test_frontend.js

# Con cobertura
pytest tests/ --cov=. --cov-report=html
```

### Cobertura Actual

- ✅ **Backend**: 18 tests (base de datos, API, generador de menús)
- ✅ **Frontend**: 7 tests (API mocks, utilidades)
- ✅ **Total**: 25 tests automáticos

Ver [TESTING.md](TESTING.md) para documentación completa del sistema de testing.

## 🚀 Próximas Mejoras Sugeridas

- [ ] Integración con calendarios (Google Calendar, iCal)
- [ ] Modo offline para la vista TV
- [ ] Exportar menús a PDF
- [ ] Sistema de favoritos para recetas
- [ ] Historial de menús anteriores
- [ ] Integración con listas de compra (Todoist, etc.)
- [ ] App móvil
- [ ] Notificaciones de recordatorio
- [ ] Modo "meal prep" para cocinar por lotes
- [ ] Análisis nutricional detallado

## 📄 Licencia

Este proyecto está diseñado para uso personal y familiar.

## 🤝 Contribuciones

Este es un proyecto personalizado, pero si encuentras bugs o tienes sugerencias:
1. Documenta el problema claramente
2. Proporciona ejemplos de reproducción
3. Sugiere soluciones si es posible

Ver [CONTRIBUTING.md](CONTRIBUTING.md) para la guía completa de contribución.

## 📚 Documentación Completa

### Documentación Principal

- **[DOCS_INDEX.md](DOCS_INDEX.md)** - Índice completo de toda la documentación
- **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** - Documentación completa de la API REST
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Arquitectura técnica del sistema
- **[DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md)** - Guía para desarrolladores
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Guía completa de deployment

### Guías de Inicio

- **[START_HERE.md](START_HERE.md)** - Guía de inicio rápido paso a paso
- **[GUIA_RAPIDA.md](GUIA_RAPIDA.md)** - Guía rápida en español
- **[INICIO_RAPIDO.md](INICIO_RAPIDO.md)** - Inicio rápido alternativo

### Testing y Contribución

- **[TESTING.md](TESTING.md)** - Guía completa del sistema de testing
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Cómo contribuir al proyecto
- **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - Estructura detallada del proyecto

### Deployment

- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Guía completa de deployment (Railway, Heroku, Docker, etc.)
- **[RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md)** - Guía específica de Railway

## 📞 Soporte

Para problemas con:
- **Anthropic API**: https://docs.anthropic.com/
- **Flask**: https://flask.palletsprojects.com/
- **Python**: https://docs.python.org/

## 🙏 Agradecimientos

- Anthropic por Claude AI
- La comunidad de Python y Flask
- Todos los blogs de cocina que comparten sus recetas

---

**¡Disfruta de tu planificación de menús automatizada! 🍽️✨**

Para empezar:
```bash
python init.py   # Inicializar
python app.py    # Ejecutar
```

Luego abre http://localhost:7000 en tu navegador.

---

## 🗺️ Navegación Rápida

- **Nuevo usuario?** → Empieza con [START_HERE.md](START_HERE.md)
- **Quieres usar la API?** → Lee [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
- **Quieres desarrollar?** → Consulta [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md)
- **Quieres desplegar?** → Sigue [DEPLOYMENT.md](DEPLOYMENT.md)
- **Quieres entender el sistema?** → Revisa [ARCHITECTURE.md](ARCHITECTURE.md)

Ver **[DOCS_INDEX.md](DOCS_INDEX.md)** para el índice completo de documentación.
