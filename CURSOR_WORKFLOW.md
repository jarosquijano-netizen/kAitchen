# 🎯 Workflow: Cursor + Github + Railway

Guía completa del flujo de trabajo para desarrollar y desplegar tu sistema de menús familiares usando Cursor, Github y Railway.

## 🌊 Flujo de Trabajo Completo

```
┌──────────┐      ┌──────────┐      ┌──────────┐
│  Cursor  │ ───► │  Github  │ ───► │ Railway  │
│   (Dev)  │      │  (Code)  │      │ (Deploy) │
└──────────┘      └──────────┘      └──────────┘
     │                  │                  │
     │                  │                  │
  Editas            Guardas            Auto-
  código            cambios           deploya
```

## 🚀 Setup Inicial (Una Vez)

### 1. Instalar Herramientas

```bash
# Cursor (Editor con IA)
# Descarga desde: https://cursor.sh/
# O si tienes VS Code, Cursor es compatible

# Git (si no lo tienes)
# Windows: https://git-scm.com/
# Mac: brew install git
# Linux: sudo apt install git

# Railway CLI
npm install -g @railway/cli
# O: brew install railway
```

### 2. Configurar Proyecto

```bash
# 1. Abrir proyecto en Cursor
# File → Open Folder → [tu carpeta]

# 2. Ejecutar setup
python setup.py

# 3. Verificar .cursorrules está presente
# Cursor lo leerá automáticamente
```

### 3. Crear Repositorio en Github

```bash
# Opción A: Desde Github.com
# 1. Ve a: https://github.com/new
# 2. Nombre: family-kitchen-menu
# 3. Privado o Público (tu elección)
# 4. NO añadas README (ya tienes)
# 5. Create repository

# Opción B: Desde Cursor Terminal
gh repo create family-kitchen-menu --private --source=. --remote=origin --push
```

### 4. Conectar Github → Railway

```bash
# Opción A: Desde Railway Dashboard
# 1. https://railway.app/new
# 2. Deploy from GitHub repo
# 3. Selecciona: family-kitchen-menu
# 4. Add PostgreSQL
# 5. Set variables (ver abajo)
# 6. Deploy!

# Opción B: Desde Railway CLI
railway login
railway init
railway add  # Añadir PostgreSQL
railway variables set ANTHROPIC_API_KEY=sk-ant-...
railway variables set SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
railway up
```

## 💻 Desarrollo Diario con Cursor

### Usar Cursor AI Efectivamente

Cursor tiene integración con IA. Aquí está cómo usarla mejor:

#### 1. **Cmd/Ctrl + K** - AI Edit

```
# Selecciona código y presiona Cmd+K
Prompt: "Añade validación de email a este formulario"
Prompt: "Optimiza esta query de base de datos"
Prompt: "Añade manejo de errores aquí"
```

#### 2. **Cmd/Ctrl + L** - AI Chat

```
# Abre panel de chat con IA
"¿Cómo puedo añadir autenticación con Clerk?"
"Explica esta función de extracción de recetas"
"¿Cuál es la mejor forma de cachear las recetas?"
```

#### 3. **Cursor Composer** - Multi-file Edits

```
# Para cambios que afectan múltiples archivos
Cmd+Shift+I

"Añade un nuevo campo 'dietary_notes' a los perfiles de adultos,
actualiza la base de datos, el formulario HTML y el API"

Cursor editará:
- database.py
- templates/index.html
- app.py
- static/js/app.js
```

### Ejemplos de Prompts Efectivos para Cursor

**Para Añadir Features:**
```
"Añade una función en menu_generator.py que permita 
excluir ingredientes específicos del menú generado.
Debe considerar los perfiles existentes."
```

**Para Debugging:**
```
"Este código en recipe_extractor.py está fallando
para sitios sin JSON-LD. ¿Cómo puedo mejorar el
fallback a extracción manual?"
```

**Para Refactoring:**
```
"Refactoriza database.py para usar un patrón singleton
y añade connection pooling para PostgreSQL"
```

**Para Testing:**
```
"Crea tests unitarios para las funciones principales
de menu_generator.py usando pytest"
```

### Workflow Típico de Desarrollo

```bash
# 1. Abrir Cursor
cursor .

# 2. Checkout nueva rama
git checkout -b feature/nueva-funcionalidad

# 3. Usar Cursor AI para desarrollar
# - Cmd+K para editar código
# - Cmd+L para preguntas
# - .cursorrules guía automáticamente

# 4. Probar localmente
python app.py
# Abrir: http://localhost:5000

# 5. Commit cambios
git add .
git commit -m "feat: añadida nueva funcionalidad"

# 6. Push a Github
git push origin feature/nueva-funcionalidad

# 7. Crear Pull Request en Github
# 8. Merge a main
# 9. Railway auto-deploya 🎉
```

## 🔄 CI/CD Automático

### Cómo Funciona

```
┌─────────────┐
│ Git Commit  │
│   & Push    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Github    │  Almacena código
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Railway    │  Detecta cambio
│  Webhook    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Auto Build  │  Instala deps
│ & Deploy    │  Corre tests
└──────┬──────┘  Deploya
       │
       ▼
┌─────────────┐
│  Live App   │  Actualizado!
└─────────────┘
```

### Configurar Github Actions (Opcional)

Para tests automáticos antes de deploy:

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest
      
      - name: Run tests
        run: pytest tests/
```

## 🎨 Personalización con Cursor

### Cambiar Estilos de la UI

```python
# 1. Abre templates/tv_display.html en Cursor
# 2. Selecciona el CSS
# 3. Cmd+K:

"Cambia el esquema de colores a tonos verdes y azules
que sean relajantes para una cocina. Mantén la legibilidad."

# Cursor modificará automáticamente todos los colores
```

### Añadir Nueva Funcionalidad

```python
# 1. Cmd+L en Cursor (Chat)
# 2. Pregunta:

"Quiero añadir un sistema de favoritos para recetas.
¿Qué archivos necesito modificar y cómo?"

# 3. Cursor te dará un plan
# 4. Usa Cursor Composer (Cmd+Shift+I):

"Implementa el sistema de favoritos que acabas de describir.
Añade:
- Campo en base de datos
- Botón en la UI
- API endpoint
- Lógica frontend"

# 5. Cursor editará múltiples archivos automáticamente
```

## 🐛 Debugging con Cursor

### Usar Cursor para Encontrar Bugs

```python
# Scenario: Menu generation está fallando

# 1. Abre menu_generator.py
# 2. Cmd+L (Chat):

"El método generate_weekly_menu está fallando para familias
sin recetas guardadas. ¿Cuál es el problema y cómo lo arreglo?"

# Cursor analizará el código y sugerirá:
# - Posibles causas
# - Líneas específicas problemáticas
# - Solución con código

# 3. Aplica la solución con Cmd+K
```

### Usar Railway Logs

```bash
# Ver logs en tiempo real
railway logs --follow

# O desde Cursor Terminal:
railway logs | grep ERROR

# Para bugs de producción:
# 1. Copia el error de Railway
# 2. Pégalo en Cursor Chat (Cmd+L)
# 3. Pregunta: "¿Por qué está ocurriendo esto?"
```

## 🚀 Deploy desde Cursor

### Push Rápido

```bash
# Terminal en Cursor (Cmd+J)

# Si trabajaste en rama feature:
git checkout main
git merge feature/mi-feature
git push

# Railway auto-deploya en ~2 minutos
```

### Preview Deployments (Avanzado)

Para probar antes de deployar a producción:

```bash
# Crear preview environment en Railway
railway environment

# Deploy a preview
railway up --environment preview

# Probar
railway open --environment preview

# Si funciona, merge a main
git checkout main
git merge feature/mi-feature
git push  # Deploy a producción
```

## 📊 Monitoreo en Cursor

### Ver Status de Railway

```bash
# Terminal en Cursor
railway status

# Ver deployments recientes
railway deployments

# Ver logs de producción
railway logs --environment production

# Ver variables
railway variables
```

### Setup Notificaciones

En Railway dashboard → Settings → Webhooks:

```
Deployment Started: POST https://tu-webhook.com/started
Deployment Success: POST https://tu-webhook.com/success
Deployment Failed: POST https://tu-webhook.com/failed
```

Puedes conectar a Slack, Discord, o email.

## 💡 Tips Pro

### 1. Usar .cursorrules Efectivamente

El archivo `.cursorrules` guía a Cursor. Personalizalo:

```markdown
# En .cursorrules, añade:

## Project-Specific Rules
- Always use Spanish for user-facing strings
- Prioritize food allergies in all menu logic
- Use PostgreSQL for production queries
- Test recipe extraction on 3+ sites before PR
```

### 2. Cursor Symbols

```
@filename  - Referencia un archivo
#function  - Referencia una función
@docs      - Busca en documentación
@web       - Busca en internet
```

Ejemplo:
```
"En @database.py, modifica #get_all_adults para incluir
campo de preferencias de desayuno"
```

### 3. Shortcuts de Cursor

```
Cmd/Ctrl + K       AI Edit (editar selección)
Cmd/Ctrl + L       AI Chat (preguntas)
Cmd/Ctrl + Shift+I  Composer (ediciones multi-archivo)
Cmd/Ctrl + /       Comentar línea
Cmd/Ctrl + D       Seleccionar siguiente ocurrencia
Cmd/Ctrl + P       Quick open de archivos
Cmd/Ctrl + `       Toggle terminal
```

### 4. Workflow de Pull Requests

```bash
# Desarrollo con Cursor
git checkout -b feature/menu-improvements
# ... hacer cambios con Cursor AI ...
git commit -m "Mejoras en generación de menús"
git push origin feature/menu-improvements

# En Github.com:
# 1. Create Pull Request
# 2. Añade descripción (Cursor puede generarla)
# 3. Request review (si trabajas en equipo)
# 4. Merge cuando esté aprobado

# Railway deploya automáticamente cuando merges a main
```

## 🎓 Recursos de Aprendizaje

### Cursor
- Docs: https://cursor.sh/docs
- Shortcuts: Cmd+Shift+P → "Cursor: Shortcuts"
- Discord: https://discord.gg/cursor

### Railway
- Docs: https://docs.railway.app/
- Templates: https://railway.app/templates
- Community: https://discord.gg/railway

### Github
- Actions: https://github.com/features/actions
- CLI: https://cli.github.com/
- Desktop: https://desktop.github.com/

## ✅ Checklist de Setup Completo

- [ ] Cursor instalado y configurado
- [ ] .cursorrules presente en proyecto
- [ ] Git inicializado (`git init`)
- [ ] Repositorio creado en Github
- [ ] Código pusheado a Github
- [ ] Railway conectado a Github
- [ ] PostgreSQL añadido en Railway
- [ ] Variables de entorno configuradas
- [ ] Primer deployment exitoso
- [ ] App accesible en Railway URL
- [ ] Auto-deployment funciona (test con commit)

## 🎉 ¡Listo para Desarrollar!

Ahora tienes:
- ✅ Editor con IA (Cursor)
- ✅ Control de versiones (Github)
- ✅ Auto-deployment (Railway)
- ✅ Base de datos en la nube (PostgreSQL)
- ✅ HTTPS automático
- ✅ Workflow profesional

**Próximo paso**: ¡Empieza a desarrollar! Usa Cursor AI para todo:
- Añadir features
- Refactorizar código
- Resolver bugs
- Mejorar UI/UX
- Optimizar performance

---

**Recuerda**: 
- Cursor AI conoce tu proyecto por `.cursorrules`
- Github guarda tu código
- Railway deploya automáticamente
- Tú te enfocas en crear features 🚀
