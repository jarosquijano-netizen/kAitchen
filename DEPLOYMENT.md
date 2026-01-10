# 🚀 Guía de Deployment

Guía completa para desplegar k[AI]tchen en diferentes entornos.

## 📋 Tabla de Contenidos

1. [Requisitos Previos](#requisitos-previos)
2. [Deployment Local](#deployment-local)
3. [Deployment en Railway](#deployment-en-railway)
4. [Deployment en Otros Servicios](#deployment-en-otros-servicios)
5. [Configuración Post-Deployment](#configuración-post-deployment)
6. [Troubleshooting](#troubleshooting)

## ✅ Requisitos Previos

### Cuentas Necesarias

- **Anthropic**: Para API key de Claude ([console.anthropic.com](https://console.anthropic.com))
- **Railway** (opcional): Para hosting ([railway.app](https://railway.app))
- **GitHub** (opcional): Para control de versiones

### Herramientas

- Python 3.8+
- Git
- Railway CLI (si usas Railway)

## 🏠 Deployment Local

### Windows

#### Opción 1: Script Batch

```batch
# Usar start_server.bat
start_server.bat
```

#### Opción 2: Manual

```powershell
# 1. Activar entorno virtual (si existe)
.\venv\Scripts\activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar .env
# Editar .env y añadir ANTHROPIC_API_KEY

# 4. Inicializar base de datos
python init.py

# 5. Ejecutar servidor
python app.py
```

El servidor estará disponible en `http://localhost:7000`

### Linux/Mac

```bash
# 1. Activar entorno virtual
source venv/bin/activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar .env
nano .env  # Añadir ANTHROPIC_API_KEY

# 4. Inicializar base de datos
python init.py

# 5. Ejecutar servidor
python app.py
```

### Con Gunicorn (Producción Local)

```bash
# Instalar gunicorn
pip install gunicorn

# Ejecutar con gunicorn
gunicorn app:app --bind 0.0.0.0:7000 --workers 2 --timeout 120
```

## 🚂 Deployment en Railway

Railway es la plataforma recomendada para producción.

### Paso 1: Preparar el Proyecto

Asegúrate de tener estos archivos:

- `Procfile` (ya incluido)
- `railway.toml` (ya incluido)
- `requirements.txt` (ya incluido)
- `.env.example` (para referencia)

### Paso 2: Crear Proyecto en Railway

1. Ve a [railway.app](https://railway.app)
2. Inicia sesión o crea cuenta
3. Click en "New Project"
4. Selecciona "Deploy from GitHub repo" o "Empty Project"

### Paso 3: Conectar Repositorio (si usas GitHub)

1. En Railway, selecciona "Deploy from GitHub repo"
2. Autoriza Railway a acceder a tu repositorio
3. Selecciona el repositorio
4. Railway detectará automáticamente Python y Flask

### Paso 4: Configurar Variables de Entorno

En Railway dashboard, ve a "Variables" y añade:

```env
ANTHROPIC_API_KEY=sk-ant-api03-tu-key-aqui
SECRET_KEY=genera-una-clave-secreta-aleatoria
FLASK_ENV=production
DATABASE_URL=postgresql://... (Railway lo proporciona automáticamente)
CORS_ORIGINS=https://tu-dominio.com,https://www.tu-dominio.com
PORT=7000 (Railway lo establece automáticamente)
```

**Cómo generar SECRET_KEY**:
```python
import secrets
print(secrets.token_hex(32))
```

### Paso 5: Añadir Base de Datos PostgreSQL

1. En Railway dashboard, click "New"
2. Selecciona "Database" → "Add PostgreSQL"
3. Railway creará automáticamente la base de datos
4. La variable `DATABASE_URL` se añadirá automáticamente

### Paso 6: Deploy

Railway detectará automáticamente:
- `Procfile` para el comando de inicio
- `requirements.txt` para instalar dependencias
- Python como lenguaje

El deploy comenzará automáticamente. Puedes ver el progreso en "Deployments".

### Paso 7: Configurar Dominio

1. En Railway dashboard, ve a "Settings"
2. Click "Generate Domain" o añade tu dominio personalizado
3. Railway proporcionará una URL como `tu-proyecto.railway.app`

### Paso 8: Verificar Deployment

```bash
# Ver logs
railway logs

# Verificar que el servidor está corriendo
curl https://tu-proyecto.railway.app/health
```

Deberías recibir:
```json
{
  "status": "ok",
  "timestamp": "2024-01-15T10:30:00"
}
```

## 🌐 Deployment en Otros Servicios

### Heroku

#### 1. Crear `Procfile`

```
web: gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
```

#### 2. Crear `runtime.txt`

```
python-3.11.0
```

#### 3. Deploy

```bash
# Instalar Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login

# Crear app
heroku create tu-app-name

# Añadir PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Configurar variables
heroku config:set ANTHROPIC_API_KEY=tu-key
heroku config:set SECRET_KEY=tu-secret-key
heroku config:set FLASK_ENV=production

# Deploy
git push heroku main
```

### DigitalOcean App Platform

1. Conecta tu repositorio de GitHub
2. DigitalOcean detectará Flask automáticamente
3. Configura variables de entorno en el dashboard
4. Añade base de datos PostgreSQL
5. Deploy automático

### AWS Elastic Beanstalk

#### 1. Crear `.ebextensions/python.config`

```yaml
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: app:app
```

#### 2. Deploy

```bash
# Instalar EB CLI
pip install awsebcli

# Inicializar
eb init

# Crear entorno
eb create

# Deploy
eb deploy
```

### Docker

#### 1. Crear `Dockerfile`

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7000

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:7000", "--workers", "2", "--timeout", "120"]
```

#### 2. Crear `docker-compose.yml`

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "7000:7000"
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - SECRET_KEY=${SECRET_KEY}
      - DATABASE_URL=postgresql://user:pass@db:5432/kitchen
      - FLASK_ENV=production
    depends_on:
      - db
  
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=kitchen
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

#### 3. Ejecutar

```bash
docker-compose up -d
```

## ⚙️ Configuración Post-Deployment

### 1. Inicializar Base de Datos

Si es la primera vez que despliegas, necesitas inicializar las tablas:

```bash
# Opción 1: Via Railway CLI
railway run python init.py

# Opción 2: Via SSH/Shell del servicio
python init.py
```

### 2. Verificar Variables de Entorno

```bash
# Railway
railway variables

# Heroku
heroku config

# Verificar que todas están configuradas:
# - ANTHROPIC_API_KEY
# - SECRET_KEY
# - DATABASE_URL
# - FLASK_ENV
```

### 3. Probar Endpoints

```bash
# Health check
curl https://tu-dominio.com/health

# Obtener perfiles (debería devolver array vacío inicialmente)
curl https://tu-dominio.com/api/adults
```

### 4. Configurar CORS

Si vas a acceder desde un dominio diferente:

```env
CORS_ORIGINS=https://tu-frontend.com,https://www.tu-frontend.com
```

O para desarrollo:
```env
CORS_ORIGINS=*
```

⚠️ **Advertencia**: `CORS_ORIGINS=*` solo para desarrollo. En producción, especifica dominios exactos.

## 🔍 Troubleshooting

### Error: "ANTHROPIC_API_KEY no configurada"

**Solución**:
1. Verifica que la variable está en Railway/Heroku/etc.
2. Verifica que el nombre es exactamente `ANTHROPIC_API_KEY`
3. Reinicia el servicio después de añadir la variable

### Error: "Database connection failed"

**Solución**:
1. Verifica que `DATABASE_URL` está configurada
2. Verifica que la base de datos está corriendo (Railway/Heroku)
3. Verifica formato de URL: `postgresql://user:pass@host:port/db`

### Error: "Port already in use"

**Solución**:
- En producción, usa la variable `PORT` del servicio
- No hardcodees el puerto en el código
- Railway/Heroku establecen `PORT` automáticamente

### Error: "Module not found"

**Solución**:
1. Verifica que `requirements.txt` incluye todas las dependencias
2. Rebuild el proyecto
3. Verifica logs de build para errores de instalación

### La aplicación no responde

**Checklist**:
- [ ] ¿El servicio está corriendo? (ver logs)
- [ ] ¿Las variables de entorno están configuradas?
- [ ] ¿La base de datos está accesible?
- [ ] ¿El dominio está correctamente configurado?
- [ ] ¿Hay errores en los logs?

### Ver Logs

```bash
# Railway
railway logs

# Heroku
heroku logs --tail

# Docker
docker-compose logs -f web
```

## 📊 Monitoreo

### Health Check Endpoint

El endpoint `/health` está disponible para monitoreo:

```bash
curl https://tu-dominio.com/health
```

Respuesta esperada:
```json
{
  "status": "ok",
  "timestamp": "2024-01-15T10:30:00"
}
```

### Logs Recomendados

Monitorea estos eventos en los logs:
- Errores de API de Anthropic
- Errores de base de datos
- Timeouts en generación de menús
- Errores de extracción de recetas

### Métricas Importantes

- Tiempo de respuesta de API
- Tasa de éxito de generación de menús
- Uso de memoria y CPU
- Errores 500

## 🔄 Actualización de Deployment

### Proceso de Actualización

1. **Desarrollo Local**
   ```bash
   git checkout -b feature/nueva-funcionalidad
   # Hacer cambios
   git commit -m "Añadir nueva funcionalidad"
   ```

2. **Testing**
   ```bash
   python run_tests.py
   ```

3. **Push a Repositorio**
   ```bash
   git push origin feature/nueva-funcionalidad
   ```

4. **Merge a Main**
   - Crear Pull Request
   - Revisar cambios
   - Merge

5. **Deploy Automático**
   - Railway/Heroku detectará cambios
   - Deploy automático comenzará
   - Verificar logs

### Rollback

Si algo sale mal:

```bash
# Railway
railway rollback

# Heroku
heroku releases:rollback v123

# Docker
docker-compose down
git checkout previous-version
docker-compose up -d
```

## 🔐 Seguridad en Producción

### Checklist de Seguridad

- [ ] `SECRET_KEY` es aleatoria y segura
- [ ] `ANTHROPIC_API_KEY` no está en el código
- [ ] `DATABASE_URL` contiene credenciales seguras
- [ ] CORS está configurado correctamente (no `*` en producción)
- [ ] HTTPS está habilitado
- [ ] Variables de entorno no están en el repositorio
- [ ] `.env` está en `.gitignore`

### Variables Sensibles

**NUNCA** commitees:
- `.env`
- `ANTHROPIC_API_KEY`
- `SECRET_KEY`
- `DATABASE_URL` con credenciales

**SÍ** commitea:
- `.env.example` (sin valores reales)
- `requirements.txt`
- `Procfile`
- `railway.toml`

## 📚 Recursos Adicionales

- [Railway Documentation](https://docs.railway.app/)
- [Heroku Python Guide](https://devcenter.heroku.com/articles/getting-started-with-python)
- [Flask Deployment](https://flask.palletsprojects.com/en/latest/deploying/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)

---

## ✅ Checklist de Deployment

### Pre-Deployment

- [ ] Código probado localmente
- [ ] Tests pasando
- [ ] Variables de entorno documentadas
- [ ] `.env.example` actualizado
- [ ] `requirements.txt` actualizado
- [ ] Documentación actualizada

### Deployment

- [ ] Servicio creado (Railway/Heroku/etc.)
- [ ] Base de datos configurada
- [ ] Variables de entorno configuradas
- [ ] Deploy exitoso
- [ ] Health check funcionando

### Post-Deployment

- [ ] Base de datos inicializada
- [ ] Endpoints API funcionando
- [ ] Frontend accesible
- [ ] Logs sin errores críticos
- [ ] Dominio configurado (si aplica)

---

**¡Deployment exitoso! 🎉**
