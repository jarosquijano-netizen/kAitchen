# Guía de Contribución - k[AI]tchen

Gracias por tu interés en contribuir a k[AI]tchen. Esta guía te ayudará a entender cómo contribuir de manera efectiva.

## 🚀 Antes de Contribuir

1. **Lee el código existente** - Entiende la estructura y convenciones
2. **Ejecuta los tests** - Asegúrate de que todos pasen antes de hacer cambios
3. **Revisa la documentación** - Lee README.md y TESTING.md

## 📝 Proceso de Contribución

### 1. Fork y Clone

```bash
git clone https://github.com/TU_USUARIO/k[AI]tchen.git
cd k[AI]tchen
```

### 2. Crear una Rama

```bash
git checkout -b feature/nueva-funcionalidad
# o
git checkout -b fix/correccion-bug
```

### 3. Hacer Cambios

- Sigue las convenciones de código del proyecto
- Añade comentarios cuando sea necesario
- Mantén el código en español para comentarios de usuario
- Usa inglés para nombres técnicos y código

### 4. Añadir Tests

**IMPORTANTE**: Cualquier nueva funcionalidad debe incluir tests.

#### Para Backend

Crea tests en `tests/test_nuevo_feature.py`:

```python
import pytest
from app import app

class TestNuevoFeature:
    def test_funcionalidad_basica(self, client):
        response = client.get('/api/nuevo-endpoint')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] == True
```

#### Para Frontend

Añade tests en `tests/test_frontend.js`:

```javascript
test.test('Nueva funcionalidad funciona', async () => {
    // Tu código de test
    test.assertTrue(condicion);
});
```

### 5. Ejecutar Tests

```bash
# Ejecutar todos los tests
python run_tests.py

# Solo backend
pytest tests/ -v

# Solo frontend
node tests/test_frontend.js
```

**Todos los tests deben pasar antes de hacer commit.**

### 6. Verificar Código

- Revisa que no haya errores de linting
- Verifica que el código sigue las convenciones
- Asegúrate de que la documentación esté actualizada

### 7. Commit

```bash
git add .
git commit -m "feat: añade nueva funcionalidad X"
# o
git commit -m "fix: corrige bug en Y"
```

**Convenciones de commits:**
- `feat:` - Nueva funcionalidad
- `fix:` - Corrección de bug
- `docs:` - Cambios en documentación
- `test:` - Añadir o modificar tests
- `refactor:` - Refactorización de código
- `style:` - Cambios de formato (sin afectar funcionalidad)

### 8. Push y Pull Request

```bash
git push origin feature/nueva-funcionalidad
```

Luego crea un Pull Request en GitHub con:
- Descripción clara de los cambios
- Referencia a issues relacionados (si aplica)
- Screenshots si es un cambio de UI
- Confirmación de que los tests pasan

## ✅ Checklist Pre-Pull Request

- [ ] Código sigue las convenciones del proyecto
- [ ] Todos los tests pasan (`python run_tests.py`)
- [ ] Se añadieron tests para nueva funcionalidad
- [ ] Documentación actualizada (README, comentarios)
- [ ] No hay errores de linting
- [ ] Código probado manualmente
- [ ] Commit message sigue las convenciones

## 🧪 Testing

### Estructura de Tests

```
tests/
├── test_database.py      # Tests de base de datos
├── test_api.py          # Tests de endpoints Flask
├── test_menu_generator.py # Tests del generador de menús
└── test_frontend.js     # Tests del frontend
```

### Escribir Tests Efectivos

1. **Tests independientes** - Cada test debe poder ejecutarse solo
2. **Nombres descriptivos** - `test_add_adult_with_all_fields` es mejor que `test1`
3. **Una aserción por concepto** - No mezcles múltiples verificaciones
4. **Tests rápidos** - Los tests lentos desaniman su ejecución
5. **Cobertura de casos edge** - Prueba casos límite y errores

### Ejemplo de Test Backend

```python
def test_add_adult_missing_required_field(self, client):
    """Test that adding adult without required field fails"""
    adult_data = {
        'nombre': 'Test',  # Falta 'edad' requerida
    }
    response = client.post('/api/adults',
                          data=json.dumps(adult_data),
                          content_type='application/json')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['success'] == False
```

## 📚 Convenciones de Código

### Python

- Usa type hints para todas las funciones
- Sigue PEP 8
- Docstrings en estilo Google
- Prefiere f-strings sobre .format()

### JavaScript

- Usa ES6+ (const/let, arrow functions, async/await)
- Template literals para strings
- JSDoc para funciones complejas

### Base de Datos

- Siempre usa queries parametrizadas
- Maneja errores apropiadamente
- Cierra conexiones explícitamente

## 🐛 Reportar Bugs

Si encuentras un bug:

1. Verifica que no esté ya reportado en Issues
2. Crea un nuevo issue con:
   - Descripción clara del problema
   - Pasos para reproducir
   - Comportamiento esperado vs actual
   - Screenshots si aplica
   - Información del entorno (OS, Python version, etc.)

## 💡 Sugerir Mejoras

Para sugerir nuevas funcionalidades:

1. Crea un issue con la etiqueta "enhancement"
2. Describe la funcionalidad propuesta
3. Explica el caso de uso
4. Si es posible, propón una implementación

## 📖 Documentación

Al añadir nueva funcionalidad:

1. Actualiza README.md si es una feature importante
2. Añade docstrings a funciones nuevas
3. Actualiza TESTING.md si añades nuevos tests
4. Añade ejemplos de uso si es relevante

## 🔒 Seguridad

- **NUNCA** commitees archivos `.env` con API keys reales
- Usa variables de entorno para secretos
- Valida y sanitiza toda entrada de usuario
- Usa queries parametrizadas para prevenir SQL injection

## ❓ Preguntas

Si tienes preguntas:

1. Revisa la documentación existente
2. Busca en Issues cerrados
3. Crea un nuevo issue con la etiqueta "question"

## 🙏 Agradecimientos

Gracias por contribuir a k[AI]tchen. Tu ayuda hace que el proyecto sea mejor para todos.

---

**Última actualización**: 2025-01-02
