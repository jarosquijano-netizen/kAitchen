# 🚀 Guía de Inicio Rápido

## Tu Sistema Ya Está Listo

Ya se ha inicializado tu sistema con los perfiles de tu familia:
- **3 Adultos**: María (38), Carlos (40), Lucía (65)
- **2 Niñas**: Emma (12) y Sofía (4)

## 📝 Configuración en 3 Pasos

### Paso 1: Configura la API Key de Anthropic

```bash
# Edita el archivo .env
nano .env

# Cambia esta línea:
ANTHROPIC_API_KEY=sk-ant-api03-tu_key_aqui

# Por tu key real de: https://console.anthropic.com/
```

### Paso 2: Inicia el Servidor

```bash
python app.py
```

Verás algo como:
```
🍳 SISTEMA DE GESTIÓN DE MENÚS FAMILIARES
============================================================
📱 Interfaz de administración: http://localhost:7000
📺 Vista de TV: http://localhost:7000/tv
```

### Paso 3: Abre en tu Navegador

- **Administración**: http://localhost:7000
- **Vista TV**: http://localhost:7000/tv

## 🎯 Casos de Uso

### 1. Generar tu Primer Menú Semanal

1. Abre http://localhost:7000
2. Ve a la pestaña "Menú Semanal"
3. Haz clic en "✨ Generar Menú con IA"
4. Espera 15-30 segundos
5. ¡Listo! Verás un menú completo para toda la semana

El menú considerará:
- ✅ Alergias e intolerancias de todos
- ✅ Preferencias de adultos y niños
- ✅ Nivel de exigencia de las niñas (especialmente Sofía de 4 años)
- ✅ Balance nutricional
- ✅ Cocina mediterránea (Barcelona)

### 2. Ver el Menú en la TV de tu Cocina

**Opción A: TV con Navegador Web**
1. En la TV, abre el navegador
2. Ve a: `http://[IP-DE-TU-ORDENADOR]:7000/tv`
3. Pon en pantalla completa (F11)

**Opción B: Chromecast / Fire TV Stick**
1. Instala un navegador en el dispositivo
2. Accede a la misma URL
3. El menú se actualizará automáticamente cada 5 minutos

**Encontrar la IP de tu ordenador:**
- Windows: `ipconfig` (busca IPv4)
- Mac/Linux: `ifconfig` (busca inet)
- Ejemplo: 192.168.1.100

### 3. Añadir Recetas desde Internet

**Una receta:**
1. Copia la URL de tu blog de cocina favorito
2. Ve a "Recetas" en la app
3. Pega la URL
4. Haz clic en "Extraer Receta"

**Múltiples recetas:**
1. Haz clic en "Extraer Múltiples"
2. Pega una URL por línea
3. Haz clic en "Extraer Todas"

**Sitios compatibles:**
- Blogs españoles (Recetas de Rechupete, Anna Recetas Fáciles)
- AllRecipes
- Food Network
- La mayoría de blogs con recetas estructuradas

### 4. Modificar Perfiles Familiares

Para actualizar preferencias:
1. Ve a la pestaña "Familia"
2. Encuentra el perfil que quieres cambiar
3. Haz clic en "Eliminar"
4. Añade uno nuevo con los datos actualizados

**Ejemplo**: Sofía ahora acepta brócoli:
1. Elimina el perfil de Sofía
2. Añade uno nuevo con "Verduras aceptadas: patatas, guisantes, zanahoria, brócoli"

## 💡 Tips Pro

### Para Mejores Menús de IA

1. **Sé específico con las alergias** - La IA las prioriza siempre
2. **Actualiza preferencias** - Los niños cambian sus gustos rápidamente
3. **Indica tiempo real** - Si solo tienes 30 min, el menú se adaptará
4. **Usa los comentarios** - "Le gusta comida bonita" ayuda a la IA

### Para la Vista TV

1. **Usa modo oscuro** - Configura tu TV en modo oscuro por la noche
2. **Prueba distancias** - Ajusta el tamaño de fuente si es necesario
3. **Bookmark** - Guarda como favorito para acceso rápido
4. **Auto-start** - Configura tu TV para abrir el navegador al encender

### Para Recetas

1. **Prefiere fuentes originales** - Los blogs funcionan mejor que agregadores
2. **Verifica antes de guardar** - Revisa que la extracción fue correcta
3. **Organiza por tipo** - Usa el campo de tipo de cocina

## 🎨 Personalización

### Cambiar Colores de la Vista TV

Edita `templates/tv_display.html`:

```css
body {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    /* Cambia estos colores hex */
}
```

### Ajustar Tamaño de Texto en TV

En `templates/tv_display.html`, busca:

```css
.meal-name {
    font-size: 2.5rem; /* Aumenta o disminuye este valor */
}
```

## 🐛 Problemas Comunes

### "No se puede generar menú"
**Causa**: API key no configurada
**Solución**: Edita `.env` con tu key real

### "Error al extraer receta"
**Causa**: El sitio no soporta extracción o bloquea bots
**Solución**: Prueba con otro sitio o añade la receta manualmente

### "No veo el menú en la TV"
**Causa**: IP incorrecta o firewall
**Solución**: 
- Usa la IP local de tu ordenador (no localhost)
- Desactiva el firewall temporalmente
- Verifica que estén en la misma red WiFi

## 📊 Ejemplo de Uso Real

**Domingo por la tarde:**
1. Genera el menú para la semana
2. Revisa la lista de compra generada
3. Ve al supermercado con la lista
4. Abre la vista TV en la cocina

**Durante la semana:**
- Mira la TV cada mañana para ver qué toca
- Sigue las instrucciones de preparación
- Si algo no funciona, genera un nuevo menú

**Ventajas:**
- ✅ No más "¿qué hacemos de comer?"
- ✅ Compras más eficientes
- ✅ Mejor balance nutricional
- ✅ Menos desperdicio de comida
- ✅ Todos comen algo que les gusta

## 🔄 Actualizar el Sistema

```bash
# Hacer backup de la base de datos
cp family_kitchen.db family_kitchen.db.backup

# Actualizar dependencias
pip install -r requirements.txt --upgrade

# Reiniciar servidor
python app.py
```

## 📱 Acceso Remoto (Avanzado)

Si quieres acceder desde fuera de casa:

**NO RECOMENDADO para producción**, pero para uso personal:

1. Instala ngrok: https://ngrok.com/
2. Ejecuta: `ngrok http 5000`
3. Usa la URL que te da (ej: https://abc123.ngrok.io)

⚠️ **Advertencia**: Esto expone tu aplicación a Internet. Solo para uso temporal.

## 🎓 Recursos Adicionales

### Aprender Más Sobre IA
- https://docs.anthropic.com/claude/docs
- Experimenta con diferentes prompts en `menu_generator.py`

### Mejorar Extracción de Recetas
- https://beautiful-soup-4.readthedocs.io/
- Añade patrones para tus sitios favoritos

### Personalizar la Interfaz
- https://flask.palletsprojects.com/
- Los templates usan HTML/CSS/JavaScript estándar

## ✨ ¡Disfruta de tu Sistema!

Tu familia de Barcelona ahora tiene:
- Perfiles detallados configurados
- Sistema listo para generar menús
- Interfaz TV preparada
- Base de datos inicializada

**¿Siguiente paso?**
→ Configura tu API key y genera tu primer menú

---

**¿Preguntas?** Consulta el README.md completo o la documentación inline en el código.
