# 🚂 Guía de Deployment en Railway

Esta guía te llevará paso a paso para desplegar tu sistema de menús familiares en Railway.

## 🎯 Por Qué Railway

Railway es perfecto para este proyecto porque:
- ✅ **Deployment automático** desde Github
- ✅ **PostgreSQL incluido** y pre-configurado
- ✅ **HTTPS gratuito** y automático
- ✅ **Variables de entorno** fáciles de configurar
- ✅ **$5 gratis al mes** (suficiente para este proyecto)
- ✅ **Escalado automático** si crece tu uso

## 📋 Prerequisitos

1. **Cuenta de Github** - Para sincronizar el código
2. **Cuenta de Railway** - Regístrate en https://railway.app/
3. **API Key de Anthropic** - Para generar menús con IA

## 🚀 Método 1: Deploy Rápido (Recomendado)

### Paso 1: Preparar Github

```bash
# 1. Crear repositorio en Github
# Ve a: https://github.com/new

# 2. Clonar o subir tu código
git init
git add .
git commit -m "Initial commit - Family Kitchen Menu System"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/family-kitchen-menu.git
git push -u origin main
```

### Paso 2: Conectar con Railway

1. **Ir a Railway**: https://railway.app/
2. **Login** con tu cuenta de Github
3. **New Project** → **Deploy from GitHub repo**
4. **Seleccionar** tu repositorio `family-kitchen-menu`
5. Railway detectará automáticamente que es un proyecto Python

### Paso 3: Añadir PostgreSQL

1. En tu proyecto de Railway, click **+ New**
2. Selecciona **Database** → **Add PostgreSQL**
3. Railway configurará automáticamente `DATABASE_URL`

### Paso 4: Configurar Variables de Entorno

En Railway dashboard → **Variables**:

```bash
# REQUERIDO
ANTHROPIC_API_KEY=sk-ant-api03-TU-KEY-AQUI

# REQUERIDO (genera uno seguro)
SECRET_KEY=tu-secret-key-de-32-caracteres-minimo

# Automático (Railway lo configura)
DATABASE_URL=postgresql://... (auto-configurado)
PORT=... (auto-configurado)

# Configuración de producción
FLASK_ENV=production
```

**Generar SECRET_KEY**:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Paso 5: Deploy!

1. Railway deployará automáticamente
2. Espera 2-3 minutos
3. Click en **View Logs** para ver el progreso
4. Cuando termine, verás: ✅ **Deployment successful**

### Paso 6: Acceder a Tu App

1. En Railway dashboard, click **Generate Domain**
2. Railway te dará una URL: `https://tu-app.up.railway.app`
3. ¡Abre esa URL y tu sistema está listo! 🎉

## 🚀 Método 2: Deploy con Railway CLI

### Instalación

```bash
# Instalar Railway CLI
npm i -g @railway/cli

# O con Homebrew (Mac)
brew install railway
```

### Deployment

```bash
# 1. Login
railway login

# 2. Crear nuevo proyecto
railway init

# 3. Link con tu código
railway link

# 4. Añadir PostgreSQL
railway add

# Selecciona: PostgreSQL

# 5. Configurar variables
railway variables set ANTHROPIC_API_KEY=sk-ant-...
railway variables set SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
railway variables set FLASK_ENV=production

# 6. Deploy
railway up

# 7. Ver logs
railway logs

# 8. Abrir en navegador
railway open
```

## 🔧 Configuración Post-Deployment

### 1. Verificar Variables de Entorno

En Railway dashboard → **Variables**, deberías ver:

```
✅ ANTHROPIC_API_KEY
✅ SECRET_KEY
✅ FLASK_ENV=production
✅ DATABASE_URL (auto-configurado)
✅ PORT (auto-configurado)
```

### 2. Inicializar Base de Datos

La base de datos se crea automáticamente en el primer arranque, pero si necesitas añadir perfiles de ejemplo:

**Opción A: Desde Railway CLI**
```bash
railway run python init.py
```

**Opción B: Crear endpoint temporal**

Añade temporalmente en `app.py`:
```python
@app.route('/api/init-db')
def init_db():
    # Ejecuta tu código de inicialización
    return "Database initialized"
```

Luego accede: `https://tu-app.up.railway.app/api/init-db`

### 3. Configurar Dominio Personalizado (Opcional)

En Railway dashboard → **Settings** → **Domains**:

1. Click **Add Custom Domain**
2. Añade tu dominio (ej: `menu.tudominio.com`)
3. Railway te dará registros DNS para configurar
4. Añade esos registros en tu proveedor de dominios
5. Espera 5-30 minutos para propagación

## 📊 Monitoreo y Logs

### Ver Logs en Tiempo Real

**Desde CLI**:
```bash
railway logs --follow
```

**Desde Dashboard**:
1. Click en tu servicio
2. Tab **Deployments**
3. Click en el deployment activo
4. View Logs

### Métricas de Uso

Railway dashboard muestra:
- CPU usage
- Memory usage
- Network traffic
- Request count

## 🔄 Actualizaciones Automáticas

Railway re-deploya automáticamente cuando:
1. Haces `git push` a la rama main
2. Cambias variables de entorno
3. Actualizas dependencias

**Para forzar re-deploy**:
```bash
# Trigger nuevo build
git commit --allow-empty -m "Trigger rebuild"
git push
```

## 💰 Costos

### Plan Gratis (Trial)
- $5 de crédito mensual
- Suficiente para:
  - 1 app Flask pequeña
  - 1 base de datos PostgreSQL
  - ~500MB RAM
  - Ideal para uso personal/familiar

### Plan Starter ($5/mes)
- $5 de crédito mensual
- Para aplicaciones con más tráfico

### Estimación para Este Proyecto
- **Uso normal** (familia de 5): ~$2-3/mes
- **Includes**: Hosting + Base de datos + Bandwidth
- **No incluye**: API calls de Anthropic (~$1-2/mes adicional)

## 🐛 Troubleshooting

### Error: "Build Failed"

**Síntomas**: Deployment falla durante build

**Soluciones**:
```bash
# Verificar requirements.txt
# Asegúrate de que todas las dependencias están listadas

# Ver logs específicos
railway logs

# Probar build localmente
pip install -r requirements.txt
python app.py
```

### Error: "Database Connection Failed"

**Síntomas**: App arranca pero no conecta a PostgreSQL

**Soluciones**:
1. Verifica que PostgreSQL está añadido en Railway
2. Verifica `DATABASE_URL` en variables
3. Reinicia el servicio

```bash
# Desde CLI
railway restart
```

### Error: "Module Not Found"

**Síntomas**: `ImportError: No module named 'X'`

**Solución**:
```bash
# Añadir dependencia faltante a requirements.txt
echo "nombre-del-modulo==version" >> requirements.txt

# Commit y push
git add requirements.txt
git commit -m "Add missing dependency"
git push
```

### Error: "Port Already in Use"

**Síntomas**: Solo en desarrollo local

**Solución**:
```bash
# Railway usa $PORT automáticamente
# En local, cambia a otro puerto:
export PORT=3000
python app.py
```

## 🔐 Seguridad en Producción

### 1. Variables de Entorno Seguras

✅ **NUNCA** commitees `.env` a Github
✅ Usa secrets diferentes para dev/prod
✅ Rota API keys periódicamente

### 2. HTTPS

Railway proporciona HTTPS automáticamente para:
- Dominios `*.up.railway.app`
- Dominios personalizados (con SSL auto-renovable)

### 3. Rate Limiting (Opcional)

Para producción pública, añade rate limiting:

```python
# Instalar: pip install flask-limiter
from flask_limiter import Limiter

limiter = Limiter(
    app,
    key_func=lambda: request.remote_addr,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/menu/generate')
@limiter.limit("5 per hour")  # Max 5 menús por hora
def generate_menu():
    # ...
```

## 📈 Optimización

### 1. Reducir Cold Starts

Railway duerme apps inactivas. Para mantenerla activa:

```bash
# Añadir health check en app.py
@app.route('/health')
def health():
    return {'status': 'ok'}

# Usar servicio externo de ping (ej: UptimeRobot)
# Ping cada 5 minutos a: https://tu-app.up.railway.app/health
```

### 2. Caché de Recetas

Para evitar re-extraer recetas:

```python
# Verificar si receta ya existe por URL
existing = db.get_recipe_by_url(url)
if existing:
    return existing
```

### 3. Conexiones de Base de Datos

```python
# Usar connection pooling para PostgreSQL
from psycopg2 import pool

connection_pool = pool.SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    dsn=DATABASE_URL
)
```

## 🔄 Rollback

Si un deployment falla o tiene bugs:

**Desde Dashboard**:
1. Tab **Deployments**
2. Find previous working deployment
3. Click ⋮ (menu)
4. **Rollback to this version**

**Desde CLI**:
```bash
# Ver deployments
railway deployments

# Rollback al anterior
railway rollback
```

## 📱 Monitoreo con Webhook (Opcional)

Railway puede notificarte en cada deployment:

1. **Settings** → **Webhooks**
2. Añade URL de tu servicio (Slack, Discord, etc.)
3. Eventos: deployment.created, deployment.completed, deployment.failed

## ✅ Checklist de Deployment

Antes de considerar el deployment completo:

- [ ] PostgreSQL añadido y conectado
- [ ] Todas las variables de entorno configuradas
- [ ] Deployment exitoso (sin errores)
- [ ] App accesible en la URL de Railway
- [ ] Puedes añadir perfiles familiares
- [ ] Puedes generar menús con IA
- [ ] Vista TV funciona correctamente
- [ ] Logs no muestran errores críticos
- [ ] (Opcional) Dominio personalizado configurado

## 🎓 Recursos Adicionales

- **Railway Docs**: https://docs.railway.app/
- **Railway Discord**: https://discord.gg/railway
- **Railway Status**: https://status.railway.app/
- **Gunicorn Docs**: https://docs.gunicorn.org/

## 🎉 ¡Felicidades!

Tu sistema de menús familiares ahora está:
- ✅ En producción
- ✅ Accesible 24/7
- ✅ Con HTTPS
- ✅ Auto-escalable
- ✅ Con base de datos persistente

**URL de tu sistema**: `https://tu-app.up.railway.app`

**Para usar desde la TV**: Abre esa URL + `/tv`

---

**¿Problemas?** Revisa la sección de Troubleshooting o los logs de Railway.
