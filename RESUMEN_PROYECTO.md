# 🍳 Sistema de Gestión de Menús Familiares - RESUMEN DEL PROYECTO

## 📦 Proyecto Completado

Sistema completo de planificación de menús familiares con IA para tu familia de 5 miembros en Barcelona, España.

---

## 🎯 Lo Que Has Recibido

### ✅ Sistema Funcional Completo

1. **Backend en Python** con Flask
2. **Base de datos SQLite** con perfiles familiares
3. **Interfaz web de administración** moderna y responsive
4. **Vista TV-friendly** para cocina
5. **Integración con Claude AI** (Anthropic) para generar menús
6. **Extractor de recetas** desde URLs web
7. **Documentación completa** en español

---

## 📂 Estructura de Archivos

```
family-kitchen-menu/
│
├── 📄 app.py                    # Servidor Flask principal (API + Routes)
├── 📄 database.py               # Gestión de base de datos SQLite
├── 📄 recipe_extractor.py       # Extracción de recetas desde URLs
├── 📄 menu_generator.py         # Generador de menús con IA
├── 📄 init.py                   # Script de inicialización
│
├── 📄 requirements.txt          # Dependencias Python
├── 📄 .env.example             # Ejemplo de configuración
├── 📄 .env                     # Tu configuración (EDITAR AQUÍ)
│
├── 📁 templates/
│   ├── index.html              # Interfaz de administración
│   └── tv_display.html         # Vista para TV de cocina
│
├── 📁 static/
│   └── js/
│       └── app.js              # Lógica frontend JavaScript
│
├── 📄 README.md                # Documentación completa
├── 📄 GUIA_RAPIDA.md          # Guía de inicio rápido
│
└── 📄 family_kitchen.db        # Base de datos (se crea al iniciar)
```

---

## 🚀 Instalación y Uso

### 1️⃣ Requisitos Previos
- Python 3.8+
- pip (gestor de paquetes Python)
- Navegador web moderno

### 2️⃣ Instalación Rápida

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Configurar API key
# Edita .env y añade: ANTHROPIC_API_KEY=tu_key_aqui
nano .env

# 3. Iniciar servidor
python app.py

# 4. Abrir navegador
# http://localhost:5000
```

### 3️⃣ Perfiles Ya Configurados

Tu familia ya está en el sistema:

**Adultos:**
- 👩 María (38 años) - Cocina mediterránea, intolerancia lactosa leve
- 👨 Carlos (40 años) - Le gusta picante, prefiere platos contundentes  
- 👵 Lucía (65 años) - Salud cardiovascular, cocina tradicional

**Niñas:**
- 👧 Emma (12 años) - Selectiva media, le gusta pasta/pollo, rechaza pescado azul
- 👶 Sofía (4 años) - MUY selectiva, solo patatas/pasta/pollo, rechaza verduras

---

## 🔑 Funcionalidades Implementadas

### 1. Gestión de Perfiles Familiares
- ✅ CRUD completo de adultos y niños
- ✅ 20 campos de información por adulto
- ✅ 19 campos de información por niño
- ✅ Alergias, intolerancias, preferencias
- ✅ Interfaz visual intuitiva

### 2. Extracción de Recetas
- ✅ Extracción automática desde URLs
- ✅ Detección de ingredientes e instrucciones
- ✅ Soporte para múltiples sitios web
- ✅ Extracción por lotes
- ✅ Almacenamiento en base de datos

### 3. Generación de Menús con IA
- ✅ Menú semanal completo (7 días)
- ✅ 4 comidas por día (desayuno, comida, merienda, cena)
- ✅ Considera TODAS las preferencias y restricciones
- ✅ Balance nutricional automático
- ✅ Lista de compra generada
- ✅ Consejos de preparación

### 4. Vista TV para Cocina
- ✅ Interfaz grande y legible
- ✅ Diseño atractivo con colores
- ✅ Actualización automática cada 5 minutos
- ✅ Navegación por días de la semana
- ✅ Responsive (funciona en tablets/móviles también)

### 5. API REST Completa
- ✅ 15 endpoints diferentes
- ✅ Formato JSON
- ✅ Manejo de errores
- ✅ Validación de datos

---

## 🎨 Capturas de Pantalla (Interfaz)

### Interfaz de Administración
- 4 pestañas principales: Familia, Recetas, Menú, Vista TV
- Diseño moderno con cards y colores
- Formularios intuitivos
- Feedback visual (alertas, loading)

### Vista TV
- Fondo degradado atractivo
- Tarjetas grandes para cada comida
- Íconos visuales (🌅 desayuno, 🍽️ comida, etc.)
- Vista semanal con días clickeables
- Hora y fecha actualizadas

---

## 💡 Casos de Uso Reales

### Escenario 1: Domingo por la Tarde
1. María abre el sistema en su laptop
2. Genera el menú semanal con IA (30 segundos)
3. Revisa que considera la selectividad de Sofía
4. Ve la lista de compra generada
5. Va al supermercado con la lista en el móvil

### Escenario 2: Lunes por la Mañana
1. Lucía mira la TV de la cocina
2. Ve que hoy toca: "Pollo al horno con patatas"
3. Sabe que es adecuado para todos, incluso Sofía
4. Lee el tiempo de preparación: 45 minutos
5. Puede empezar a cocinar

### Escenario 3: Miércoles Noche
1. Carlos busca recetas de tacos en internet
2. Copia 3 URLs de recetas interesantes
3. Las añade al sistema con extracción por lotes
4. La próxima vez que genere menú, la IA las considerará

---

## 🔧 Personalización

### Cambiar Colores
**Vista TV**: Edita `templates/tv_display.html`
```css
body {
    background: linear-gradient(135deg, #TU_COLOR_1, #TU_COLOR_2);
}
```

### Modificar Prompts de IA
**Menú Generator**: Edita `menu_generator.py`
- Añade restricciones específicas
- Cambia el formato de salida
- Ajusta el tono (más formal/casual)

### Añadir Nuevos Campos
**Database**: Edita `database.py`
- Añade columnas a las tablas
- Actualiza los formularios en `index.html`

---

## 📊 Tecnologías Utilizadas

### Backend
- **Flask 3.0** - Framework web
- **SQLite3** - Base de datos
- **Anthropic API** - IA (Claude Sonnet 4)
- **BeautifulSoup4** - Web scraping
- **Trafilatura** - Extracción de texto
- **Pandas** - Manipulación de datos

### Frontend
- **HTML5/CSS3** - Estructura y estilos
- **JavaScript ES6+** - Lógica interactiva
- **Fetch API** - Comunicación con backend
- **CSS Grid/Flexbox** - Layout responsive

---

## 🔐 Seguridad y Privacidad

### Datos Locales
- ✅ Todos los datos se almacenan localmente
- ✅ No se envía información personal a terceros
- ✅ La API de Anthropic solo recibe perfiles para generar menús

### API Key
- ⚠️ Mantén tu `.env` privado
- ⚠️ No compartas tu API key
- ⚠️ La API key tiene costos asociados (muy bajos)

### Recomendaciones
- 🔒 Usa solo en tu red local
- 🔒 Si expones a Internet, añade autenticación
- 🔒 Haz backups regulares de `family_kitchen.db`

---

## 💰 Costos

### Anthropic API
- **Modelo**: Claude Sonnet 4 (claude-sonnet-4-20250514)
- **Costo aproximado por menú**: $0.10 - $0.30 USD
- **Menús al mes**: 4-5 (uno por semana)
- **Costo mensual estimado**: $0.50 - $1.50 USD

**Muy económico** para el valor que aporta.

### Alternativas
Si no quieres usar la API:
- Puedes usar el sistema sin generar menús con IA
- Añade recetas manualmente
- Crea menús a mano

---

## 🐛 Solución de Problemas

### Problema: "Module not found"
**Solución**: 
```bash
pip install -r requirements.txt --upgrade
```

### Problema: "API key not found"
**Solución**:
1. Verifica que `.env` existe
2. Confirma que tiene `ANTHROPIC_API_KEY=tu_key`
3. Reinicia el servidor

### Problema: "Port 5000 already in use"
**Solución**:
```bash
# Cambia el puerto en app.py
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Problema: "Cannot connect to database"
**Solución**:
```bash
# Elimina y recrea la base de datos
rm family_kitchen.db
python init.py
```

---

## 📈 Próximas Mejoras Sugeridas

### Fase 2 - Mejoras Corto Plazo
- [ ] Exportar menú a PDF
- [ ] Modo offline para vista TV
- [ ] Temporizador de cocina integrado
- [ ] Notificaciones push (móvil)

### Fase 3 - Mejoras Medio Plazo
- [ ] App móvil nativa
- [ ] Integración con Google Calendar
- [ ] Sincronización con lista de compra (Todoist)
- [ ] Análisis nutricional detallado

### Fase 4 - Mejoras Largo Plazo
- [ ] Sistema multiidioma
- [ ] Comunidad de recetas
- [ ] Integración con electrodomésticos inteligentes
- [ ] Machine learning para predecir preferencias

---

## 📞 Soporte y Recursos

### Documentación
- **README.md** - Documentación completa
- **GUIA_RAPIDA.md** - Inicio rápido
- Comentarios inline en el código

### APIs y Librerías
- Anthropic Claude: https://docs.anthropic.com/
- Flask: https://flask.palletsprojects.com/
- BeautifulSoup: https://www.crummy.com/software/BeautifulSoup/

### Comunidad
- Stack Overflow (Flask, Python)
- GitHub (código similar)
- Anthropic Discord (para temas de IA)

---

## ✅ Checklist de Verificación

Antes de usar el sistema, verifica:

- [x] Python 3.8+ instalado
- [x] Dependencias instaladas (`requirements.txt`)
- [x] Archivo `.env` configurado con API key
- [x] Base de datos inicializada (`family_kitchen.db`)
- [x] Perfiles familiares añadidos
- [ ] API key de Anthropic activa
- [ ] Puerto 5000 disponible
- [ ] Navegador moderno disponible

---

## 🎉 ¡Felicidades!

Has recibido un sistema completo y funcional para gestionar los menús de tu familia.

### Características Destacadas:
✨ Generación de menús con IA
✨ Considera preferencias de TODOS los miembros
✨ Extracción automática de recetas
✨ Vista TV para cocina
✨ Documentación completa en español
✨ Código limpio y bien comentado
✨ Listo para usar YA

### Próximos Pasos:
1. Configura tu API key de Anthropic
2. Ejecuta `python app.py`
3. Genera tu primer menú semanal
4. Abre la vista TV en tu cocina
5. ¡Disfruta de comidas planificadas!

---

## 📝 Notas Finales

### Mantenimiento
- Actualiza perfiles cuando cambien preferencias
- Genera nuevo menú cada domingo
- Haz backup de `family_kitchen.db` mensualmente
- Actualiza dependencias trimestralmente

### Feedback
- Ajusta los perfiles según funcione en la práctica
- Experimenta con diferentes prompts en el generador
- Añade tus recetas favoritas
- Personaliza la interfaz a tu gusto

### Evolución
Este sistema está diseñado para crecer contigo:
- Fácil de modificar y extender
- Código bien documentado
- Arquitectura modular
- API REST para integraciones futuras

---

**¡Buen provecho! 🍽️**

Sistema desarrollado con ❤️ para tu familia en Barcelona.
