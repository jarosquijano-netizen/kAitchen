# Testing Guide - k[AI]tchen

Este documento describe el sistema de testing automático implementado para prevenir errores futuros.

## 📋 Resumen

Se ha implementado un sistema completo de testing automático que cubre:
- ✅ **Backend (Python/Flask)**: 18 tests pasando
- ✅ **Frontend (JavaScript)**: 7 tests pasando
- ✅ **CI/CD**: Configuración para GitHub Actions

## 🚀 Ejecutar Tests

### Todos los tests
```bash
python run_tests.py
```

### Solo backend
```bash
pytest tests/ -v
```

### Solo frontend
```bash
node tests/test_frontend.js
```

### Con cobertura
```bash
pytest tests/ --cov=. --cov-report=html
```

## 📁 Estructura de Tests

```
tests/
├── __init__.py
├── test_database.py      # Tests de base de datos
├── test_api.py          # Tests de endpoints Flask
├── test_menu_generator.py # Tests del generador de menús
├── test_frontend.js     # Tests del frontend
└── README.md            # Documentación de tests
```

## 🧪 Tests Implementados

### Backend Tests (18 tests)

#### Database Tests (`test_database.py`)
- ✅ Inicialización de base de datos
- ✅ Creación de todas las tablas
- ✅ Añadir perfiles de adultos
- ✅ Añadir perfiles de niños
- ✅ Eliminar perfiles
- ✅ Obtener preferencias de menú
- ✅ Guardar preferencias de menú

#### API Tests (`test_api.py`)
- ✅ GET /api/adults (vacío y con datos)
- ✅ POST /api/adults
- ✅ DELETE /api/adults
- ✅ GET /api/children (vacío y con datos)
- ✅ POST /api/children
- ✅ GET /api/settings
- ✅ GET /api/family/summary
- ✅ GET /health

#### Menu Generator Tests (`test_menu_generator.py`)
- ✅ Inicialización del generador
- ✅ Estructura del menú generado

### Frontend Tests (7 tests)

#### API Mock Tests (`test_frontend.js`)
- ✅ GET /api/adults retorna lista vacía
- ✅ POST /api/adults añade adulto
- ✅ DELETE /api/adults elimina adulto
- ✅ GET /api/family/summary retorna conteo correcto
- ✅ Tests de utilidades (assertEqual, assertTrue, assertFalse)

## 🔧 Configuración

### Dependencias de Testing

Las dependencias de testing están en `requirements.txt`:
- `pytest==7.4.3`
- `pytest-cov==4.1.0`
- `pytest-flask==1.3.0`

### Variables de Entorno

Para los tests del generador de menús, necesitas configurar:
```bash
export ANTHROPIC_API_KEY=tu-key-aqui
```

Los otros tests no requieren API key.

## 🔄 CI/CD

Los tests se ejecutan automáticamente en GitHub Actions cuando:
- Se hace push a `main`, `master`, o `develop`
- Se crea un pull request

Ver `.github/workflows/tests.yml` para la configuración.

## 📊 Cobertura de Tests

Para ver la cobertura de código:
```bash
pytest tests/ --cov=. --cov-report=html
```

Esto generará un reporte HTML en `htmlcov/index.html`.

## 🐛 Troubleshooting

### Error: "no such table"
- Los tests usan bases de datos temporales
- Si falla, verifica que `init_database()` se ejecute correctamente

### Error: "ANTHROPIC_API_KEY not configured"
- Los tests del generador de menús se saltan si no hay API key
- Esto es normal y no afecta otros tests

### Tests lentos
- El test del generador de menús puede tardar ~3 minutos (llamada real a API)
- Otros tests son rápidos (< 1 segundo)

## 📝 Añadir Nuevos Tests

### Para Backend

1. Crea un nuevo archivo `tests/test_nuevo_feature.py`
2. Usa el patrón:
```python
import pytest
from app import app

class TestNuevoFeature:
    def test_algo(self, client):
        response = client.get('/api/endpoint')
        assert response.status_code == 200
```

### Para Frontend

1. Añade tests en `tests/test_frontend.js`
2. Usa el patrón:
```javascript
test.test('Nuevo test', async () => {
    // Tu código de test aquí
    test.assertTrue(condicion);
});
```

## ✅ Checklist Pre-Commit

Antes de hacer commit, ejecuta:
```bash
python run_tests.py
```

Si todos los tests pasan, puedes hacer commit con confianza.

## 🎯 Mejores Prácticas

1. **Escribe tests antes de arreglar bugs** - Ayuda a prevenir regresiones
2. **Mantén los tests rápidos** - Los tests lentos desaniman su ejecución
3. **Tests independientes** - Cada test debe poder ejecutarse solo
4. **Nombres descriptivos** - `test_add_adult_with_all_fields` es mejor que `test1`
5. **Cobertura mínima** - Apunta a >80% de cobertura de código crítico

## 📚 Recursos

- [Pytest Documentation](https://docs.pytest.org/)
- [Flask Testing](https://flask.palletsprojects.com/en/latest/testing/)
- [JavaScript Testing Best Practices](https://github.com/goldbergyoni/javascript-testing-best-practices)

---

**Última actualización**: 2025-01-02
**Tests pasando**: ✅ 25/25 (18 backend + 7 frontend)
