# 🔍 Cómo Verificar y Configurar PostgreSQL en Railway

## Paso 1: Verificar si tienes PostgreSQL

1. Ve a: https://railway.app/
2. Selecciona tu proyecto (`stunning-luck`)
3. Mira en la **Architecture** (vista de arquitectura)

### ✅ Si VES PostgreSQL:
- Verás un servicio llamado **"PostgreSQL"** o **"Database"**
- Tiene un ícono de base de datos
- Está conectado a tu servicio "web"

### ❌ Si NO VES PostgreSQL:
- Solo verás el servicio "web"
- Necesitas añadirlo (ver Paso 2)

---

## Paso 2: Añadir PostgreSQL (si no lo tienes)

1. En Railway → Tu proyecto
2. Click en **"+ New"** (botón en la parte superior o lateral)
3. Selecciona **"Database"**
4. Selecciona **"Add PostgreSQL"**
5. Railway creará automáticamente:
   - Una base de datos PostgreSQL
   - La variable `DATABASE_URL` en tu servicio "web"
   - La conexión entre "web" y PostgreSQL

---

## Paso 3: Obtener la URL de PostgreSQL

Una vez que tengas PostgreSQL:

1. Click en el servicio **PostgreSQL** (no en "web")
2. Ve a la pestaña **"Variables"**
3. Busca `DATABASE_URL` o `POSTGRES_URL`
4. Copia el valor completo

La URL se ve así:
```
postgresql://postgres:password@containers-us-west-xxx.railway.app:5432/railway
```

---

## Paso 4: Verificar Variables en el Servicio "web"

1. Click en el servicio **"web"**
2. Ve a la pestaña **"Variables"**
3. Verifica que existe `DATABASE_URL`

Si existe, Railway ya configuró todo automáticamente ✅

---

## Paso 5: Sincronizar Datos

Una vez que tengas la URL de PostgreSQL:

```powershell
# En PowerShell, reemplaza TU_URL con la URL que copiaste
$env:RAILWAY_DATABASE_URL="postgresql://postgres:password@host:port/railway"
python sync_databases.py
```

---

## 🔧 Troubleshooting

### No veo PostgreSQL en Architecture
- Click en **"+ New"** → **"Database"** → **"Add PostgreSQL"**
- Espera 1-2 minutos a que se cree

### No veo DATABASE_URL en Variables del servicio "web"
- Railway debería añadirlo automáticamente
- Si no aparece, puedes añadirlo manualmente:
  1. Ve a PostgreSQL → Variables → Copia `DATABASE_URL`
  2. Ve a "web" → Variables → Click **"+ New Variable"**
  3. Nombre: `DATABASE_URL`
  4. Valor: Pega la URL que copiaste

### Error de conexión
- Verifica que PostgreSQL esté "Online" (debería tener un punto verde)
- Verifica que la URL sea correcta (sin espacios al inicio/final)
