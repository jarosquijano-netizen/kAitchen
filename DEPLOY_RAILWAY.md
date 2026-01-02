# 🚀 Guía Rápida: Desplegar en Railway

## Paso 1: Crear Repositorio en GitHub

1. Ve a: https://github.com/new
2. Nombre del repositorio: `jaxokitchen` (o el que prefieras)
3. **NO** marques "Initialize with README" (ya tenemos archivos)
4. Click **Create repository**

## Paso 2: Subir Código a GitHub

Ejecuta estos comandos en PowerShell (reemplaza TU_USUARIO con tu usuario de GitHub):

```powershell
# Conectar con GitHub
git remote add origin https://github.com/TU_USUARIO/jaxokitchen.git

# Cambiar a rama main
git branch -M main

# Subir código
git push -u origin main
```

**Si GitHub te pide autenticación**, usa un Personal Access Token:
- Ve a: https://github.com/settings/tokens
- Generate new token (classic)
- Selecciona permisos: `repo`
- Copia el token y úsalo como contraseña cuando git te lo pida

## Paso 3: Crear Proyecto en Railway

1. Ve a: https://railway.app/
2. Click **Login** → Selecciona **Login with GitHub**
3. Autoriza Railway a acceder a tu GitHub
4. Click **New Project**
5. Selecciona **Deploy from GitHub repo**
6. Busca y selecciona tu repositorio `jaxokitchen`
7. Railway comenzará a detectar y desplegar automáticamente

## Paso 4: Añadir Base de Datos PostgreSQL

1. En tu proyecto de Railway, click **+ New**
2. Selecciona **Database** → **Add PostgreSQL**
3. Railway configurará automáticamente `DATABASE_URL`

## Paso 5: Configurar Variables de Entorno

En Railway dashboard → Tu servicio → **Variables**:

Añade estas variables:

```
ANTHROPIC_API_KEY=sk-ant-api03-8il-WUVavmUJcjaUAtd8NkcLL-c-1MRrbaFRyCbMCkZ40tloL_GKQnfuCrBykGvan1LVYRqqdg5sm4tdRVL_Pbw-iwv-mAAA
```

Para generar SECRET_KEY, ejecuta en PowerShell:
```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

Luego añade:
```
SECRET_KEY=el-valor-generado-aqui
FLASK_ENV=production
```

**NOTA**: Railway configura automáticamente:
- `DATABASE_URL` (no necesitas añadirlo manualmente)
- `PORT` (no necesitas añadirlo manualmente)

## Paso 6: Esperar Deployment

1. Railway comenzará a construir automáticamente
2. Ve a **Deployments** → Click en el deployment activo
3. Verás los logs en tiempo real
4. Espera 2-3 minutos hasta que veas: ✅ **Deployment successful**

## Paso 7: Obtener URL de tu App

1. En Railway dashboard, click en tu servicio
2. Click **Settings** → **Generate Domain**
3. Railway te dará una URL como: `https://jaxokitchen-production.up.railway.app`
4. **Copia esta URL** - la necesitarás para acceder desde la TV

## Paso 8: Acceder desde tu TV

En tu Xiaomi TV dongle:

1. Abre el navegador
2. Ve a: `https://TU-URL-RAILWAY.up.railway.app/tv`
3. ¡Listo! Tu menú debería aparecer

## Paso 9: Inicializar Base de Datos (Primera vez)

La primera vez que accedas, necesitas inicializar la base de datos:

1. Ve a: `https://TU-URL-RAILWAY.up.railway.app`
2. Ve a la pestaña **Settings**
3. Configura tu API key (si no lo hiciste en variables de entorno)
4. Ve a la pestaña **Family** y añade perfiles
5. Ve a **Menu** y genera tu primer menú

## ✅ Verificación

Tu app está funcionando si:
- ✅ Puedes acceder a la URL de Railway
- ✅ Puedes ver la interfaz principal
- ✅ Puedes acceder a `/tv` y ver la vista de TV
- ✅ Los logs de Railway no muestran errores

## 🔧 Troubleshooting

### Error: "Build Failed"
- Verifica que `requirements.txt` tiene todas las dependencias
- Revisa los logs en Railway para ver el error específico

### Error: "Database Connection Failed"
- Verifica que añadiste PostgreSQL en Railway
- Verifica que `DATABASE_URL` está configurado (Railway lo hace automáticamente)

### La app no carga
- Verifica que todas las variables de entorno están configuradas
- Revisa los logs: Railway dashboard → Deployments → View Logs

## 📱 URLs Importantes

- **Interfaz Principal**: `https://TU-URL.up.railway.app`
- **Vista TV**: `https://TU-URL.up.railway.app/tv`
- **API**: `https://TU-URL.up.railway.app/api/...`

---

**¿Necesitas ayuda?** Revisa los logs en Railway o consulta `RAILWAY_DEPLOYMENT.md` para más detalles.
