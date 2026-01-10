# 📡 Documentación de la API

Documentación completa de todos los endpoints disponibles en k[AI]tchen.

## 🔗 Base URL

- **Desarrollo**: `http://localhost:7000`
- **Producción**: `https://tu-dominio.com`

## 📋 Formato de Respuesta

Todas las respuestas siguen este formato:

```json
{
  "success": true|false,
  "data": {...},
  "error": "mensaje de error si success es false",
  "message": "mensaje opcional"
}
```

## 🔐 Autenticación

Actualmente, la API no requiere autenticación para uso local. En producción, se recomienda implementar autenticación mediante Clerk o similar.

---

## 👥 Perfiles de Adultos

### GET /api/adults

Obtiene todos los perfiles de adultos registrados.

**Respuesta exitosa (200)**:
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "nombre": "María",
      "edad": 38,
      "objetivo_alimentario": "Salud y bienestar",
      "estilo_alimentacion": "Mediterránea",
      "cocinas_favoritas": "Española, Italiana",
      "nivel_picante": "Medio",
      "ingredientes_favoritos": "Aceite de oliva, ajo, tomate",
      "ingredientes_no_gustan": "Pepino",
      "alergias": "",
      "intolerancias": "Lactosa leve",
      "restricciones_religiosas": "",
      "flexibilidad_comer": "Flexible",
      "preocupacion_principal": "Nutrición equilibrada",
      "tiempo_max_cocinar": 60,
      "nivel_cocina": "Intermedio",
      "tipo_desayuno": "Ligero",
      "le_gustan_snacks": true,
      "plato_favorito": "Paella",
      "created_at": "2024-01-15T10:30:00"
    }
  ],
  "count": 1
}
```

### POST /api/adults

Añade un nuevo perfil de adulto.

**Body (JSON)**:
```json
{
  "nombre": "María",
  "edad": 38,
  "objetivo_alimentario": "Salud y bienestar",
  "estilo_alimentacion": "Mediterránea",
  "cocinas_favoritas": "Española, Italiana",
  "nivel_picante": "Medio",
  "ingredientes_favoritos": "Aceite de oliva, ajo, tomate",
  "ingredientes_no_gustan": "Pepino",
  "alergias": "",
  "intolerancias": "Lactosa leve",
  "restricciones_religiosas": "",
  "flexibilidad_comer": "Flexible",
  "preocupacion_principal": "Nutrición equilibrada",
  "tiempo_max_cocinar": 60,
  "nivel_cocina": "Intermedio",
  "tipo_desayuno": "Ligero",
  "le_gustan_snacks": true,
  "plato_favorito": "Paella"
}
```

**Respuesta exitosa (201)**:
```json
{
  "success": true,
  "message": "Perfil de adulto añadido correctamente",
  "id": 1
}
```

**Errores posibles**:
- `400`: Datos inválidos o campos requeridos faltantes

### DELETE /api/adults/{id}

Elimina un perfil de adulto.

**Parámetros**:
- `id` (path): ID del adulto a eliminar

**Respuesta exitosa (200)**:
```json
{
  "success": true,
  "message": "Perfil eliminado correctamente"
}
```

**Errores posibles**:
- `404`: Perfil no encontrado

---

## 👶 Perfiles de Niños

### GET /api/children

Obtiene todos los perfiles de niños registrados.

**Respuesta exitosa (200)**:
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "nombre": "Emma",
      "edad": 12,
      "nivel_exigencia": "Media",
      "ingredientes_acepta": "Pasta, pollo, patatas",
      "ingredientes_rechaza": "Pescado azul, brócoli",
      "texturas_no_gusta": "Muy cremoso",
      "alergias": "",
      "intolerancias": "",
      "preferencias_comida": "Platos simples",
      "comida_favorita": "Espaguetis con tomate",
      "comida_rechaza": "Pescado",
      "nivel_actividad": "Alta",
      "apetito": "Normal",
      "created_at": "2024-01-15T10:30:00"
    }
  ],
  "count": 1
}
```

### POST /api/children

Añade un nuevo perfil de niño.

**Body (JSON)**:
```json
{
  "nombre": "Emma",
  "edad": 12,
  "nivel_exigencia": "Media",
  "ingredientes_acepta": "Pasta, pollo, patatas",
  "ingredientes_rechaza": "Pescado azul, brócoli",
  "texturas_no_gusta": "Muy cremoso",
  "alergias": "",
  "intolerancias": "",
  "preferencias_comida": "Platos simples",
  "comida_favorita": "Espaguetis con tomate",
  "comida_rechaza": "Pescado",
  "nivel_actividad": "Alta",
  "apetito": "Normal"
}
```

**Respuesta exitosa (201)**:
```json
{
  "success": true,
  "message": "Perfil de niño añadido correctamente",
  "id": 1
}
```

### DELETE /api/children/{id}

Elimina un perfil de niño.

**Parámetros**:
- `id` (path): ID del niño a eliminar

**Respuesta exitosa (200)**:
```json
{
  "success": true,
  "message": "Perfil eliminado correctamente"
}
```

---

## 🍳 Recetas

### GET /api/recipes

Obtiene todas las recetas almacenadas.

**Respuesta exitosa (200)**:
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "title": "Paella Valenciana",
      "url": "https://ejemplo.com/paella",
      "ingredients": ["arroz", "pollo", "azafrán"],
      "instructions": "1. Calentar aceite...",
      "prep_time": 30,
      "cook_time": 45,
      "servings": 4,
      "cuisine_type": "Española",
      "meal_type": "Comida",
      "difficulty": "Media",
      "image_url": "https://ejemplo.com/imagen.jpg",
      "created_at": "2024-01-15T10:30:00"
    }
  ],
  "count": 1
}
```

### POST /api/recipes/extract

Extrae una receta desde una URL.

**Body (JSON)**:
```json
{
  "url": "https://ejemplo.com/receta"
}
```

**Respuesta exitosa (200)**:
```json
{
  "success": true,
  "message": "Receta extraída y guardada correctamente",
  "data": {
    "id": 1,
    "title": "Paella Valenciana",
    "url": "https://ejemplo.com/receta",
    "ingredients": ["arroz", "pollo", "azafrán"],
    "instructions": "1. Calentar aceite...",
    "prep_time": 30,
    "cook_time": 45,
    "servings": 4
  }
}
```

**Errores posibles**:
- `400`: URL inválida o no se pudo extraer la receta
- `500`: Error al guardar en base de datos

### POST /api/recipes/batch

Extrae múltiples recetas desde URLs.

**Body (JSON)**:
```json
{
  "urls": [
    "https://ejemplo.com/receta1",
    "https://ejemplo.com/receta2",
    "https://ejemplo.com/receta3"
  ]
}
```

**Respuesta exitosa (200)**:
```json
{
  "success": true,
  "message": "2/3 recetas extraídas correctamente",
  "data": [
    {
      "id": 1,
      "title": "Receta 1",
      "success": true
    },
    {
      "error": "No se pudo extraer la receta",
      "url": "https://ejemplo.com/receta2",
      "success": false
    },
    {
      "id": 2,
      "title": "Receta 3",
      "success": true
    }
  ]
}
```

### GET /api/recipes/search

Busca una receta por título (case-insensitive).

**Query Parameters**:
- `title` (required): Título de la receta a buscar

**Ejemplo**: `GET /api/recipes/search?title=paella`

**Respuesta exitosa (200)**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "title": "Paella Valenciana",
    "url": "https://ejemplo.com/paella",
    "instructions": "1. Calentar aceite..."
  }
}
```

**Si no se encuentra**:
```json
{
  "success": false,
  "data": null
}
```

### DELETE /api/recipes/{id}

Elimina una receta.

**Parámetros**:
- `id` (path): ID de la receta a eliminar

**Respuesta exitosa (200)**:
```json
{
  "success": true,
  "message": "Receta eliminada correctamente"
}
```

---

## 📅 Menús

### POST /api/menu/generate

Genera un menú semanal usando IA (Claude).

**Body (JSON)**:
```json
{
  "preferences": {
    "include_weekend": true,
    "include_breakfast": true,
    "include_lunch": true,
    "include_dinner": true,
    "excluded_days": []
  },
  "day_settings": {
    "lunes": {
      "meals": ["desayuno", "comida", "cena"],
      "no_cooking": false
    },
    "martes": {
      "meals": ["desayuno", "comida"],
      "no_cooking": false
    }
  },
  "week_start_date": "2024-01-15"
}
```

**Parámetros opcionales**:
- `preferences`: Preferencias adicionales del menú
- `day_settings`: Configuración específica por día
- `week_start_date`: Fecha de inicio de semana (YYYY-MM-DD). Si no se proporciona, usa la semana actual.

**Respuesta exitosa (200)**:
```json
{
  "success": true,
  "message": "Menú generado correctamente",
  "menu": {
    "menu_adultos": {
      "dias": {
        "lunes": {
          "desayuno": "Tostadas con tomate y aceite",
          "comida": "Paella de pollo y verduras",
          "merienda": "Fruta",
          "cena": "Ensalada mediterránea"
        }
      }
    },
    "menu_ninos": {
      "dias": {
        "lunes": {
          "desayuno": "Cereales con leche",
          "comida": "Espaguetis con tomate",
          "merienda": "Yogur",
          "cena": "Pollo a la plancha con patatas"
        }
      }
    },
    "lista_compra": ["arroz", "pollo", "tomate", "aceite"],
    "consejos": "Preparar el pollo con antelación..."
  },
  "menu_id": 1,
  "week_start": "2024-01-15",
  "generated_at": "2024-01-15T10:30:00"
}
```

**Errores posibles**:
- `400`: No hay perfiles familiares configurados
- `400`: API key de Anthropic no configurada
- `400`: Error en la generación del menú

### GET /api/menu/latest

Obtiene el menú más reciente generado.

**Respuesta exitosa (200)**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "week_start_date": "2024-01-15",
    "menu_data": {
      "menu_adultos": {...},
      "menu_ninos": {...}
    },
    "metadata": {
      "generated_at": "2024-01-15T10:30:00"
    },
    "created_at": "2024-01-15T10:30:00"
  }
}
```

**Errores posibles**:
- `404`: No hay menús disponibles

### GET /api/menu/week/{week_start}

Obtiene el menú para una semana específica.

**Parámetros**:
- `week_start` (path): Fecha de inicio de semana en formato YYYY-MM-DD

**Ejemplo**: `GET /api/menu/week/2024-01-15`

**Respuesta exitosa (200)**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "week_start_date": "2024-01-15",
    "menu_data": {...}
  },
  "week_start": "2024-01-15"
}
```

**Errores posibles**:
- `404`: No hay menú disponible para esa semana

### GET /api/menu/current-week

Obtiene el menú de la semana actual (lunes de la semana actual).

**Respuesta exitosa (200)**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "week_start_date": "2024-01-15",
    "menu_data": {...}
  },
  "week_start": "2024-01-15",
  "is_fallback": false
}
```

**Nota**: Si no hay menú para la semana actual, devuelve el menú más reciente con `is_fallback: true`.

### GET /api/menu/next-week

Obtiene el menú de la próxima semana.

**Respuesta exitosa (200)**:
```json
{
  "success": true,
  "data": {
    "id": 2,
    "week_start_date": "2024-01-22",
    "menu_data": {...}
  },
  "week_start": "2024-01-22"
}
```

### GET /api/menu/all

Obtiene todos los menús disponibles.

**Respuesta exitosa (200)**:
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "week_start_date": "2024-01-15",
      "menu_data": {...}
    },
    {
      "id": 2,
      "week_start_date": "2024-01-22",
      "menu_data": {...}
    }
  ],
  "count": 2
}
```

### POST /api/menu/rate-day

Califica un día específico del menú (adultos o niños).

**Body (JSON)**:
```json
{
  "menu_id": 1,
  "week_start_date": "2024-01-15",
  "day_name": "lunes",
  "menu_type": "adultos",
  "rating": 4
}
```

**Parámetros**:
- `menu_id`: ID del menú
- `week_start_date`: Fecha de inicio de semana (YYYY-MM-DD)
- `day_name`: Nombre del día (lunes, martes, etc.)
- `menu_type`: Tipo de menú (`"adultos"` o `"ninos"`)
- `rating`: Calificación entre 1 y 5

**Respuesta exitosa (200)**:
```json
{
  "success": true,
  "message": "Rating guardado correctamente"
}
```

### GET /api/menu/get-day-rating

Obtiene la calificación de un día específico.

**Query Parameters**:
- `menu_id` (required): ID del menú
- `day_name` (required): Nombre del día
- `menu_type` (required): Tipo de menú (`"adultos"` o `"ninos"`)

**Ejemplo**: `GET /api/menu/get-day-rating?menu_id=1&day_name=lunes&menu_type=adultos`

**Respuesta exitosa (200)**:
```json
{
  "success": true,
  "data": {
    "rating": 4
  }
}
```

### POST /api/menu/regenerate-day

Regenera el menú de un día específico.

**Body (JSON)**:
```json
{
  "menu_id": 1,
  "week_start_date": "2024-01-15",
  "day_name": "lunes",
  "menu_type": "adultos"
}
```

**Respuesta exitosa (200)**:
```json
{
  "success": true,
  "message": "Menú regenerado para lunes (adultos)",
  "data": {
    "desayuno": "Nuevo desayuno",
    "comida": "Nueva comida",
    "merienda": "Nueva merienda",
    "cena": "Nueva cena"
  }
}
```

---

## ⚙️ Configuración

### GET /api/settings

Obtiene la configuración actual del sistema.

**Respuesta exitosa (200)**:
```json
{
  "success": true,
  "data": {
    "has_api_key": true,
    "api_key_preview": "sk-ant-api03-...",
    "port": 7000,
    "mode": "development",
    "menu_preferences": {
      "include_weekend": true,
      "include_breakfast": true,
      "include_lunch": true,
      "include_dinner": true,
      "excluded_days": []
    }
  }
}
```

### POST /api/settings

Guarda la configuración del sistema.

**Body (JSON)**:
```json
{
  "anthropic_api_key": "sk-ant-api03-...",
  "menu_preferences": {
    "include_weekend": true,
    "include_breakfast": true,
    "include_lunch": true,
    "include_dinner": true,
    "excluded_days": []
  }
}
```

**Nota**: Puedes enviar solo `anthropic_api_key` o solo `menu_preferences`, o ambos.

**Respuesta exitosa (200)**:
```json
{
  "success": true,
  "message": "Configuración guardada correctamente. El servidor necesita reiniciarse para aplicar cambios de API key."
}
```

### POST /api/settings/test

Prueba si una API key es válida.

**Body (JSON)**:
```json
{
  "anthropic_api_key": "sk-ant-api03-..."
}
```

**Respuesta exitosa (200)**:
```json
{
  "success": true,
  "message": "API key válida. El formato es correcto."
}
```

---

## 👨‍👩‍👧‍👦 Familia

### GET /api/family/summary

Obtiene un resumen de todos los miembros de la familia.

**Respuesta exitosa (200)**:
```json
{
  "success": true,
  "data": {
    "adults": [
      {
        "id": 1,
        "nombre": "María",
        "edad": 38
      }
    ],
    "children": [
      {
        "id": 1,
        "nombre": "Emma",
        "edad": 12
      }
    ],
    "total_members": 2
  }
}
```

---

## 🏥 Health Check

### GET /health

Endpoint de verificación de salud del servidor.

**Respuesta exitosa (200)**:
```json
{
  "status": "ok",
  "timestamp": "2024-01-15T10:30:00"
}
```

---

## 🌐 Rutas Web (No API)

### GET /

Interfaz de administración principal.

### GET /tv

Vista optimizada para TV de cocina.

### GET /menu/visualizer

Visualizador de menús.

### GET /recipe/view

Visualización de receta individual.

**Query Parameters**:
- `title` (required): Título de la receta

**Ejemplo**: `GET /recipe/view?title=Paella%20Valenciana`

---

## ⚠️ Códigos de Estado HTTP

- `200`: Éxito
- `201`: Creado exitosamente
- `400`: Solicitud inválida (datos faltantes o incorrectos)
- `403`: Prohibido (solo para endpoints locales)
- `404`: Recurso no encontrado
- `500`: Error interno del servidor

---

## 🔒 Seguridad

### Endpoints Locales

Los siguientes endpoints solo están disponibles desde localhost:
- `/api/temp/get-api-key`
- `/api/temp/save-api-key-to-env`
- `/recover-api-key`

### Variables de Entorno

Asegúrate de configurar las siguientes variables en producción:
- `ANTHROPIC_API_KEY`: API key de Anthropic
- `SECRET_KEY`: Clave secreta para sesiones Flask
- `DATABASE_URL`: URL de la base de datos (PostgreSQL en producción)
- `CORS_ORIGINS`: Orígenes permitidos para CORS (separados por comas)

---

## 📝 Notas Adicionales

### Formato de Fechas

Todas las fechas se manejan en formato ISO 8601: `YYYY-MM-DD` o `YYYY-MM-DDTHH:MM:SS`.

### Semanas

Las semanas siempre comienzan en lunes. El sistema calcula automáticamente el lunes de la semana actual si no se proporciona una fecha específica.

### Timeouts

- Extracción de recetas: 10 segundos
- Generación de menús: 5 minutos (300 segundos)

### Límites

- No hay límites específicos en el número de perfiles o recetas
- Se recomienda mantener menos de 1000 recetas para mejor rendimiento
- Los menús históricos se mantienen indefinidamente

---

## 🧪 Ejemplos de Uso

### Ejemplo completo: Generar menú semanal

```bash
# 1. Obtener perfiles familiares
curl http://localhost:7000/api/adults
curl http://localhost:7000/api/children

# 2. (Opcional) Añadir recetas
curl -X POST http://localhost:7000/api/recipes/extract \
  -H "Content-Type: application/json" \
  -d '{"url": "https://ejemplo.com/receta"}'

# 3. Generar menú
curl -X POST http://localhost:7000/api/menu/generate \
  -H "Content-Type: application/json" \
  -d '{
    "preferences": {
      "include_weekend": true,
      "include_breakfast": true,
      "include_lunch": true,
      "include_dinner": true
    }
  }'

# 4. Obtener menú generado
curl http://localhost:7000/api/menu/current-week
```

### Ejemplo: Calificar un día

```bash
curl -X POST http://localhost:7000/api/menu/rate-day \
  -H "Content-Type: application/json" \
  -d '{
    "menu_id": 1,
    "week_start_date": "2024-01-15",
    "day_name": "lunes",
    "menu_type": "adultos",
    "rating": 5
  }'
```

---

## 📚 Referencias

- [Documentación de Flask](https://flask.palletsprojects.com/)
- [Documentación de Anthropic Claude](https://docs.anthropic.com/)
- [Documentación de Railway](https://docs.railway.app/)
