# 📦 Añadir PostgreSQL en Railway

## Pasos Detallados:

### 1. Añadir PostgreSQL

1. Ve a: https://railway.app/
2. Selecciona tu proyecto (`stunning-luck`)
3. En la vista **Architecture**, busca el botón **"+ New"** (arriba a la izquierda o en el sidebar)
4. Click en **"+ New"**
5. Selecciona **"Database"**
6. Selecciona **"Add PostgreSQL"**
7. Railway comenzará a crear PostgreSQL (tarda 1-2 minutos)

### 2. Esperar a que se cree

- Verás un nuevo servicio aparecer llamado **"PostgreSQL"** o **"Database"**
- Espera hasta que tenga un punto **verde** y diga **"Online"**

### 3. Verificar Variables Automáticas

Railway debería añadir automáticamente `DATABASE_URL` a tu servicio "web":

1. Click en el servicio **"web"**
2. Ve a la pestaña **"Variables"**
3. Busca `DATABASE_URL`
4. Si existe, Railway ya configuró todo ✅

### 4. Obtener la URL de PostgreSQL

1. Click en el servicio **PostgreSQL** (no en "web")
2. Ve a la pestaña **"Variables"**
3. Busca `DATABASE_URL` o `POSTGRES_URL`
4. Copia el valor completo (algo como: `postgresql://postgres:password@host:port/railway`)

### 5. Sincronizar Datos

Una vez que tengas la URL, ejecuta en PowerShell:

```powershell
# Reemplaza TU_URL con la URL que copiaste
$env:RAILWAY_DATABASE_URL="postgresql://postgres:password@host:port/railway"
python sync_databases.py
```

---

## ⚠️ Nota Importante

Después de añadir PostgreSQL, Railway puede tardar 1-2 minutos en:
- Crear la base de datos
- Configurar las variables automáticamente
- Conectar el servicio "web" con PostgreSQL

Espera hasta que veas el punto verde en PostgreSQL antes de continuar.
