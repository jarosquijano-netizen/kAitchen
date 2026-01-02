# 🚀 Instrucciones para Desplegar en Railway

## ⚡ Pasos Rápidos

### 1. Configurar Git (Solo primera vez)

Ejecuta en PowerShell (reemplaza con tu información):

```powershell
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"
```

### 2. Hacer Commit Inicial

```powershell
git commit -m "Initial commit - Family Kitchen Menu System"
```

### 3. Crear Repositorio en GitHub

1. Ve a: https://github.com/new
2. Nombre: `jaxokitchen`
3. **NO** marques "Initialize with README"
4. Click **Create repository**

### 4. Conectar y Subir a GitHub

```powershell
# Usando tu cuenta de GitHub: jarosquijano-netizen
git remote add origin https://github.com/jarosquijano-netizen/jaxokitchen.git
git branch -M main
git push -u origin main
```

**Si te pide autenticación:**
- Usa un Personal Access Token de GitHub
- Ve a: https://github.com/settings/tokens
- Generate new token (classic) → Selecciona `repo`
- Usa el token como contraseña

### 5. Desplegar en Railway

1. Ve a: https://railway.app/
2. **Login with GitHub**
3. **New Project** → **Deploy from GitHub repo**
4. Selecciona `jaxokitchen`
5. Railway comenzará a desplegar automáticamente

### 6. Añadir PostgreSQL

1. En Railway → **+ New** → **Database** → **Add PostgreSQL**
2. Railway configurará `DATABASE_URL` automáticamente

### 7. Configurar Variables de Entorno

En Railway → Tu servicio → **Variables**, añade:

```
ANTHROPIC_API_KEY=sk-ant-api03-8il-WUVavmUJcjaUAtd8NkcLL-c-1MRrbaFRyCbMCkZ40tloL_GKQnfuCrBykGvan1LVYRqqdg5sm4tdRVL_Pbw-iwv-mAAA
SECRET_KEY=753e0260bfbdb96ccfc12bdeb1a1607ab7e8e256cc0aca91a8c114ef3027c013
FLASK_ENV=production
```

### 8. Obtener URL

1. Railway → **Settings** → **Generate Domain**
2. Copia la URL (ej: `https://jaxokitchen-production.up.railway.app`)

### 9. Usar desde tu TV

En tu Xiaomi TV dongle:
- Abre navegador
- Ve a: `https://TU-URL.up.railway.app/tv`

---

## ✅ Listo!

Tu aplicación funcionará 24/7 sin necesidad de tu computadora.
