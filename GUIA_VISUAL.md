# 📸 Guía Visual Paso a Paso

## 🎯 Tu Sistema en 10 Minutos

---

## PASO 1: Preparar el Entorno
```
┌─────────────────────────────────────┐
│   📁 Descargar Archivos             │
│                                     │
│   Descomprime en una carpeta:      │
│   C:\FamilyKitchen                 │
│   /Users/tu/FamilyKitchen          │
└─────────────────────────────────────┘
```

---

## PASO 2: Instalar Dependencias
```
┌─────────────────────────────────────────────┐
│  💻 Abrir Terminal/CMD                      │
│                                             │
│  cd /ruta/a/FamilyKitchen                  │
│  pip install -r requirements.txt            │
│                                             │
│  ⏱️ Tiempo: 2-3 minutos                     │
└─────────────────────────────────────────────┘
```

---

## PASO 3: Conseguir API Key de Anthropic
```
┌───────────────────────────────────────────────┐
│  🔑 https://console.anthropic.com/           │
│                                              │
│  1. Crear cuenta / Login                     │
│  2. Ir a "API Keys"                          │
│  3. "Create Key"                             │
│  4. Copiar la key:                           │
│     sk-ant-api03-xxxxx...                    │
│                                              │
│  💰 Costo: ~$1/mes para menús semanales      │
└───────────────────────────────────────────────┘
```

---

## PASO 4: Configurar .env
```
┌─────────────────────────────────────────────┐
│  📝 Editar archivo .env                     │
│                                             │
│  Cambiar:                                   │
│  ANTHROPIC_API_KEY=tu_key_aqui             │
│                                             │
│  Por:                                       │
│  ANTHROPIC_API_KEY=sk-ant-api03-xxxxx...   │
│                                             │
│  💾 Guardar archivo                         │
└─────────────────────────────────────────────┘
```

---

## PASO 5: Iniciar Servidor
```
┌─────────────────────────────────────────────┐
│  🚀 Terminal/CMD                            │
│                                             │
│  python app.py                              │
│                                             │
│  Verás:                                     │
│  🍳 SISTEMA DE MENÚS FAMILIARES            │
│  📱 http://localhost:5000                   │
│  📺 http://localhost:5000/tv                │
│                                             │
│  ✅ ¡Listo para usar!                       │
└─────────────────────────────────────────────┘
```

---

## PASO 6: Abrir en Navegador
```
┌─────────────────────────────────────────────┐
│  🌐 Navegador Web                           │
│                                             │
│  Abre: http://localhost:5000                │
│                                             │
│  Verás la interfaz con 4 pestañas:         │
│  ┌──────────────────────────────────┐      │
│  │ 👨‍👩‍👧‍👦 Familia │ 📖 Recetas │      │
│  │ 🗓️ Menú    │ 📺 Vista TV  │      │
│  └──────────────────────────────────┘      │
│                                             │
│  ✨ Tu familia ya está configurada          │
└─────────────────────────────────────────────┘
```

---

## PASO 7: Ver Perfiles Familiares
```
┌─────────────────────────────────────────────┐
│  Pestaña: 👨‍👩‍👧‍👦 Familia                   │
│                                             │
│  ADULTOS (3):                               │
│  ┌──────────────────────────────────┐      │
│  │ María (38)                        │      │
│  │ ⚠️ Intolerancias | Mediterránea  │      │
│  └──────────────────────────────────┘      │
│  ┌──────────────────────────────────┐      │
│  │ Carlos (40)                       │      │
│  │ Omnívoro | Picante Alto          │      │
│  └──────────────────────────────────┘      │
│  ┌──────────────────────────────────┐      │
│  │ Lucía (65)                        │      │
│  │ Salud cardiovascular             │      │
│  └──────────────────────────────────┘      │
│                                             │
│  NIÑAS (2):                                 │
│  ┌──────────────────────────────────┐      │
│  │ Emma (12)                         │      │
│  │ Selectiva Media | Rechaza pescado│      │
│  └──────────────────────────────────┘      │
│  ┌──────────────────────────────────┐      │
│  │ Sofía (4)                         │      │
│  │ MUY selectiva | Solo básicos     │      │
│  └──────────────────────────────────┘      │
└─────────────────────────────────────────────┘
```

---

## PASO 8: Generar Primer Menú
```
┌─────────────────────────────────────────────┐
│  Pestaña: 🗓️ Menú Semanal                  │
│                                             │
│  ┌────────────────────────────────┐        │
│  │                                 │        │
│  │   ✨ Generar Menú con IA        │        │
│  │                                 │        │
│  └────────────────────────────────┘        │
│                                             │
│  👆 Click aquí                              │
│                                             │
│  ⏳ Espera 15-30 segundos...                │
│                                             │
│  Resultado:                                 │
│  📅 Menú Semanal                            │
│  ├── Lunes                                  │
│  │   ├── 🌅 Desayuno: Tostadas...          │
│  │   ├── 🍽️ Comida: Lentejas...            │
│  │   ├── 🧁 Merienda: Fruta...             │
│  │   └── 🌙 Cena: Pollo al horno...        │
│  ├── Martes...                              │
│  └── ...Domingo                             │
│                                             │
│  🛒 Lista de Compra Incluida                │
└─────────────────────────────────────────────┘
```

---

## PASO 9: Abrir Vista TV
```
┌─────────────────────────────────────────────┐
│  🎯 Opción A: Desde el PC                   │
│                                             │
│  Abrir: http://localhost:5000/tv            │
│  Presionar F11 (pantalla completa)          │
│                                             │
│  ───────────────────────────────────────   │
│                                             │
│  🎯 Opción B: Desde la TV                   │
│                                             │
│  1. Encuentra la IP de tu PC:              │
│     Windows: ipconfig                       │
│     Mac/Linux: ifconfig                     │
│     Ejemplo: 192.168.1.100                  │
│                                             │
│  2. En la TV, abre el navegador:           │
│     http://192.168.1.100:5000/tv           │
│                                             │
│  3. Pantalla completa (F11 o botón TV)     │
│                                             │
│  ✅ ¡El menú se muestra en grande!          │
└─────────────────────────────────────────────┘
```

---

## PASO 10: Vista TV en Acción
```
┌─────────────────────────────────────────────┐
│                                             │
│       🍳 Menú Semanal                       │
│   Martes, 31 de Diciembre - 10:30         │
│                                             │
│  ╔════════════════════════════════════╗    │
│  ║         MARTES                     ║    │
│  ╚════════════════════════════════════╝    │
│                                             │
│  ┌──────────────┬──────────────────┐       │
│  │ 🌅 DESAYUNO  │  🍽️ COMIDA       │       │
│  │              │                  │       │
│  │ Tostadas con │  Pollo al horno  │       │
│  │ aguacate     │  con patatas     │       │
│  │              │                  │       │
│  │ ⏱️ 10 min    │  ⏱️ 45 min       │       │
│  │ 👥 Todos     │  👥 Todos        │       │
│  └──────────────┴──────────────────┘       │
│                                             │
│  ┌──────────────┬──────────────────┐       │
│  │ 🧁 MERIENDA  │  🌙 CENA         │       │
│  │              │                  │       │
│  │ Fruta fresca │  Macarrones con  │       │
│  │ y yogur      │  tomate          │       │
│  │              │                  │       │
│  │ ⏱️ 5 min     │  ⏱️ 20 min       │       │
│  │ 👥 Todos     │  👥 Todos        │       │
│  └──────────────┴──────────────────┘       │
│                                             │
│  📅 Esta Semana:                            │
│  [L] [M] [X] [J] [V] [S] [D]               │
│   •   🔵  •   •   •   •   •                │
│                                             │
│              🔄 Auto-actualiza              │
└─────────────────────────────────────────────┘
```

---

## 🎉 ¡SISTEMA LISTO!

### ✅ Lo que tienes ahora:
```
┌─────────────────────────────────────────────┐
│  ✨ Sistema funcionando                     │
│  ✨ Perfiles familiares configurados        │
│  ✨ Menú semanal generado                   │
│  ✨ Vista TV activa                         │
│  ✨ Base de datos creada                    │
└─────────────────────────────────────────────┘
```

---

## 💡 Uso Diario

### 🌅 Por la Mañana
```
1. Mirar la TV de cocina
2. Ver qué toca hoy
3. Preparar ingredientes
```

### 🌙 Por la Noche
```
1. Seguir receta en la TV
2. Cocinar en familia
3. Disfrutar comida saludable
```

### 🗓️ Domingo
```
1. Generar nuevo menú semanal
2. Ver lista de compra
3. Ir al supermercado
```

---

## 🔄 Flujo Semanal Ideal

```
Domingo
  ↓
Generar Menú → Ver Lista → Comprar
  ↓              ↓           ↓
Lunes         Martes     Miércoles
  ↓              ↓           ↓
Cocinar según TV durante toda la semana
  ↓
Domingo siguiente
  ↓
Repetir ♻️
```

---

## 🎨 Personalización Rápida

### Cambiar colores de la TV
```python
# templates/tv_display.html, línea ~25

body {
    background: linear-gradient(
        135deg, 
        #TU_COLOR_1 0%,    # ← Cambia aquí
        #TU_COLOR_2 100%   # ← Y aquí
    );
}

# Ejemplos de colores:
# Azul/Morado: #667eea, #764ba2 (actual)
# Rojo/Naranja: #f12711, #f5af19
# Verde/Azul: #11998e, #38ef7d
# Rosa/Naranja: #fa709a, #fee140
```

### Ajustar tamaños de texto
```python
# templates/tv_display.html

.meal-name {
    font-size: 2.5rem;  # ← Aumentar o disminuir
}

.meal-info {
    font-size: 1.6rem;  # ← Aumentar o disminuir
}
```

---

## 🐛 Soluciones Rápidas

### No funciona el menú con IA
```
Causa: API key incorrecta

Solución:
1. Abrir .env
2. Verificar ANTHROPIC_API_KEY=sk-ant-...
3. Guardar
4. Reiniciar servidor (Ctrl+C, luego python app.py)
```

### No veo la TV desde otro dispositivo
```
Causa: Usando localhost

Solución:
1. Encontrar IP del PC: ipconfig (Win) / ifconfig (Mac)
2. En TV usar: http://192.168.1.X:5000/tv
3. Verificar misma red WiFi
```

### Recetas no se extraen
```
Causa: Sitio no compatible

Solución:
1. Probar con otro sitio
2. Usar sitios populares:
   - RecetasGratis.net
   - DirectoAlPaladar.com
   - Recetas.com
```

---

## 📱 Configuración TV por Tipo

### Smart TV Samsung/LG
```
1. Abrir "Internet" o "Browser"
2. Navegar a: http://[IP-PC]:5000/tv
3. Añadir a favoritos
4. Modo pantalla completa
```

### Chromecast
```
1. Desde Chrome en PC:
2. Menú → Transmitir
3. Seleccionar Chromecast
4. Abrir: localhost:5000/tv
5. Transmitir pestaña
```

### Fire TV Stick
```
1. Instalar "Silk Browser"
2. Abrir navegador
3. Ir a: http://[IP-PC]:5000/tv
4. Añadir a inicio
```

### Apple TV
```
1. Instalar app "AirWeb"
2. Conectar teclado Bluetooth (opcional)
3. Navegar a URL
4. Pantalla completa
```

---

## 🎓 Tips Profesionales

### 🔥 Mejora la IA
```
En menu_generator.py:

Añadir restricciones:
"- Máximo 3 ingredientes nuevos por semana"
"- Incluir siempre un plato que le encante a Sofía"
"- Priorizar recetas de menos de 30 min"
```

### 📊 Analizar uso
```
python3 << 'EOF'
from database import Database
db = Database()

adults = db.get_all_adults()
children = db.get_all_children()
recipes = db.get_all_recipes()

print(f"Adultos: {len(adults)}")
print(f"Niños: {len(children)}")
print(f"Recetas: {len(recipes)}")
EOF
```

### 🔄 Automatizar generación
```bash
# Crear script: generate_menu.py

from menu_generator import MenuGenerator
from database import Database
import os

db = Database()
gen = MenuGenerator(os.getenv('ANTHROPIC_API_KEY'))

adults = db.get_all_adults()
children = db.get_all_children()

result = gen.generate_weekly_menu(adults, children)
print("Menú generado!")

# Ejecutar cada domingo con cron (Linux/Mac):
# 0 8 * * 0 cd /ruta && python generate_menu.py
```

---

## 📞 Ayuda Adicional

### Documentación
- 📖 README.md - Completa
- 🚀 GUIA_RAPIDA.md - Inicio rápido
- 📊 RESUMEN_PROYECTO.md - Visión general

### Online
- Anthropic Docs: https://docs.anthropic.com/
- Flask Docs: https://flask.palletsprojects.com/
- Stack Overflow: Etiquetas [python] [flask]

---

## ✨ ¡Disfruta tu Sistema!

```
┌─────────────────────────────────────────────┐
│                                             │
│  Ya no más:                                 │
│  ❌ "¿Qué hacemos de comer?"                │
│  ❌ Compras desorganizadas                  │
│  ❌ Comida repetitiva                       │
│  ❌ Niños sin comer bien                    │
│                                             │
│  Ahora tienes:                              │
│  ✅ Menús balanceados                       │
│  ✅ Lista de compra automática              │
│  ✅ Variedad garantizada                    │
│  ✅ Todos contentos                         │
│                                             │
│         🍳 ¡Buen provecho! 🍽️               │
│                                             │
└─────────────────────────────────────────────┘
```

---

**Sistema creado con ❤️ para tu familia en Barcelona**
