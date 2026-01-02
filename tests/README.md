# Tests

Este directorio contiene los tests automáticos para el proyecto k[AI]tchen.

## Estructura

- `test_database.py` - Tests para operaciones de base de datos
- `test_api.py` - Tests para endpoints de la API Flask
- `test_menu_generator.py` - Tests para el generador de menús (requiere API key)
- `test_frontend.js` - Tests para funcionalidad del frontend

## Ejecutar Tests

### Todos los tests
```bash
python run_tests.py
```

### Solo tests del backend
```bash
pytest tests/ -v
```

### Solo tests específicos
```bash
pytest tests/test_database.py -v
pytest tests/test_api.py -v
```

### Con cobertura
```bash
pytest tests/ --cov=. --cov-report=html
```

### Solo tests del frontend
```bash
node tests/test_frontend.js
```

## Configuración

Los tests usan bases de datos temporales para no afectar los datos de desarrollo.

Para los tests del generador de menús, necesitas configurar `ANTHROPIC_API_KEY` en el entorno:

```bash
export ANTHROPIC_API_KEY=tu-key-aqui
```

## CI/CD

Los tests se ejecutan automáticamente en GitHub Actions cuando se hace push o pull request.
