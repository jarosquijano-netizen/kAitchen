# Índice de Documentación - k[AI]tchen

Este documento sirve como índice centralizado de toda la documentación del proyecto.

## 📖 Documentación Principal

### Para Empezar
- **[README.md](README.md)** - Documentación principal del proyecto
- **[START_HERE.md](START_HERE.md)** - Guía de inicio rápido (5 minutos)
- **[README_GITHUB.md](README_GITHUB.md)** - README optimizado para GitHub

### Desarrollo y Testing
- **[TESTING.md](TESTING.md)** - Guía completa del sistema de testing automático
  - Cómo ejecutar tests
  - Estructura de tests
  - Añadir nuevos tests
  - CI/CD con GitHub Actions

- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Guía de contribución
  - Proceso de contribución
  - Convenciones de código
  - Checklist pre-pull request
  - Reportar bugs y sugerir mejoras

- **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - Estructura del proyecto
  - Descripción de archivos y directorios
  - Flujo de datos
  - Convenciones de nombres
  - Comandos útiles

### Deployment
- **[RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md)** - Guía de deploy en Railway
- **[CURSOR_WORKFLOW.md](CURSOR_WORKFLOW.md)** - Workflow con Cursor IDE

### Guías en Español
- **[GUIA_RAPIDA.md](GUIA_RAPIDA.md)** - Guía rápida en español
- **[GUIA_VISUAL.md](GUIA_VISUAL.md)** - Guía visual paso a paso
- **[INICIO_RAPIDO.md](INICIO_RAPIDO.md)** - Inicio rápido
- **[INICIO_SERVIDOR.md](INICIO_SERVIDOR.md)** - Cómo iniciar el servidor

### Resúmenes
- **[BUILD_SUMMARY.md](BUILD_SUMMARY.md)** - Resumen de construcción
- **[RESUMEN_PROYECTO.md](RESUMEN_PROYECTO.md)** - Resumen del proyecto

## 🧪 Testing

### Ejecutar Tests
```bash
# Todos los tests
python run_tests.py

# Solo backend
pytest tests/ -v

# Solo frontend
node tests/test_frontend.js
```

### Cobertura Actual
- ✅ **Backend**: 18 tests pasando
- ✅ **Frontend**: 7 tests pasando
- ✅ **Total**: 25 tests automáticos

Ver [TESTING.md](TESTING.md) para detalles completos.

## 📁 Estructura de Tests

```
tests/
├── test_database.py      # Tests de base de datos (7 tests)
├── test_api.py          # Tests de API endpoints (9 tests)
├── test_menu_generator.py # Tests del generador (2 tests)
└── test_frontend.js     # Tests del frontend (7 tests)
```

## 🚀 Quick Links

### Desarrollo
- [Inicio Rápido](START_HERE.md)
- [Estructura del Proyecto](PROJECT_STRUCTURE.md)
- [Testing](TESTING.md)

### Contribución
- [Guía de Contribución](CONTRIBUTING.md)
- [Workflow con Cursor](CURSOR_WORKFLOW.md)

### Deployment
- [Railway Deployment](RAILWAY_DEPLOYMENT.md)
- [README GitHub](README_GITHUB.md)

## 📝 Convenciones

### Commits
- `feat:` - Nueva funcionalidad
- `fix:` - Corrección de bug
- `docs:` - Cambios en documentación
- `test:` - Añadir o modificar tests
- `refactor:` - Refactorización

### Testing
- Ejecutar tests antes de cada commit
- Añadir tests para nueva funcionalidad
- Mantener >80% cobertura en código crítico

## 🔗 Enlaces Externos

- **Anthropic Console**: https://console.anthropic.com/
- **Railway**: https://railway.app/
- **Cursor IDE**: https://cursor.sh/
- **Flask Docs**: https://flask.palletsprojects.com/

---

**Última actualización**: 2025-01-02
