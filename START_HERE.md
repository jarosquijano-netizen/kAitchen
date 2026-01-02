# ⚡ START HERE - Quick Start

## 🎯 Tu Sistema en 5 Minutos

### Opción 1: Desarrollo Local (Inmediato)

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Setup automático
python setup.py

# 3. Iniciar
python app.py

# 4. Abrir navegador
# http://localhost:7000
```

### Opción 2: Deploy en Railway (Producción)

```bash
# 1. Push a Github
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/TU_USUARIO/family-kitchen-menu.git
git push -u origin main

# 2. Railway (desde web o CLI)
# Web: https://railway.app/ → Deploy from GitHub
# CLI: railway init && railway up
```

## 📁 Documentación

Lee en este orden:

1. **CURSOR_WORKFLOW.md** - Workflow con Cursor + Github + Railway
2. **RAILWAY_DEPLOYMENT.md** - Deploy paso a paso
3. **README_GITHUB.md** - Documentación completa

## 🔑 Keys Necesarias

### Anthropic (Requerido)
1. https://console.anthropic.com/
2. Create key
3. Añade a `.env`: `ANTHROPIC_API_KEY=sk-ant-...`

### Railway (Para deploy)
1. https://railway.app/
2. Connect Github
3. Add PostgreSQL
4. Deploy

## 🎨 Usar con Cursor

```bash
# 1. Abrir en Cursor
cursor .

# 2. Cursor lee .cursorrules automáticamente
# 3. Usa Cmd+K para editar con IA
# 4. Usa Cmd+L para preguntas
```

## 📺 Vista TV

**URL local**: `http://localhost:7000/tv`
**URL producción**: `https://tu-app.up.railway.app/tv`

## 🏗️ Estructura del Proyecto

```
📦 family-kitchen-menu/
├── 📄 app.py              # Servidor Flask
├── 📄 database.py         # Base de datos
├── 📄 menu_generator.py   # IA para menús
├── 📄 recipe_extractor.py # Extrae recetas de URLs
├── 📄 setup.py            # Setup automático
├── 📁 templates/          # HTML
├── 📁 static/            # CSS/JS
└── 📚 Documentación/      # Guías y READMEs
```

## ⚙️ Configuración (.env)

```bash
# Copiar template
cp .env.example .env

# O usar setup automático
python setup.py
```

Mínimo requerido:
```
ANTHROPIC_API_KEY=sk-ant-...
SECRET_KEY=tu-secret-key-aleatorio-de-32-chars
```

## 🚀 Workflow Típico

```
1. Desarrollar en Cursor
   ├─ Cmd+K para editar con IA
   └─ Cmd+L para preguntas

2. Probar local
   └─ python app.py

3. Commit a Github
   ├─ git add .
   ├─ git commit -m "..."
   └─ git push

4. Railway auto-deploya
   └─ ¡Listo en 2 minutos!
```

## 🆘 Problemas Comunes

### "Module not found"
```bash
pip install -r requirements.txt
```

### "API key not found"
```bash
# Editar .env con tu key real
nano .env
```

### "Can't connect to Railway"
```bash
railway login
```

## 📱 Links Importantes

- **Cursor**: https://cursor.sh/
- **Railway**: https://railway.app/
- **Anthropic**: https://console.anthropic.com/
- **Documentación completa**: Ver README_GITHUB.md

## ✅ Checklist Rápido

- [ ] Python 3.8+ instalado
- [ ] Dependencies instaladas (`pip install -r requirements.txt`)
- [ ] `.env` configurado con API key
- [ ] Cursor instalado (opcional pero recomendado)
- [ ] Git inicializado
- [ ] Repositorio en Github (para deploy)

## 🧪 Testing

El proyecto incluye tests automáticos. Ejecuta antes de hacer commit:

```bash
python run_tests.py
```

Ver [TESTING.md](TESTING.md) para más detalles.

## 🎯 Siguiente Paso

**Para desarrollo local**:
```bash
python setup.py
python app.py
```

**Para producción**:
```bash
# Sigue: RAILWAY_DEPLOYMENT.md
```

**Para usar Cursor eficientemente**:
```bash
# Lee: CURSOR_WORKFLOW.md
```

**Para ejecutar tests**:
```bash
python run_tests.py
```

---

**¿Problemas?** Lee la documentación completa en los archivos .md incluidos.

**¿Todo listo?** ¡Abre Cursor y empieza a desarrollar! 🚀
