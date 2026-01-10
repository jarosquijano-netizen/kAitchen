# 🔗 Cómo Obtener la URL Externa de PostgreSQL

La URL que tienes (`postgres.railway.internal`) es **interna** y solo funciona dentro de Railway.

## Opción 1: Buscar en Variables (Recomendado)

1. Ve a Railway → Tu proyecto
2. Click en el servicio **PostgreSQL**
3. Ve a la pestaña **"Variables"**
4. Busca variables que contengan:
   - `PGHOST` (host externo)
   - `PGPORT` (puerto)
   - `PGDATABASE` (nombre de base de datos)
   - `PGUSER` (usuario)
   - `PGPASSWORD` (contraseña)

Si encuentras estas variables, construye la URL así:
```
postgresql://PGUSER:PGPASSWORD@PGHOST:PGPORT/PGDATABASE
```

## Opción 2: Buscar en Settings/Connect

1. Ve a Railway → PostgreSQL
2. Ve a la pestaña **"Settings"** o **"Connect"**
3. Busca una sección que diga **"Connection String"** o **"External Connection"**
4. Debería mostrar una URL con `railway.app` (no `railway.internal`)

## Opción 3: Usar Railway CLI (Más fácil)

Si Railway CLI está instalado, puedes obtener la URL así:

```powershell
# 1. Login en Railway
railway login

# 2. Link a tu proyecto
railway link

# 3. Obtener variables de PostgreSQL
railway variables --service postgres
```

## Opción 4: Crear URL Manualmente

Si tienes estas variables en PostgreSQL:
- `PGHOST`: `containers-us-west-xxx.railway.app`
- `PGPORT`: `5432`
- `PGDATABASE`: `railway`
- `PGUSER`: `postgres`
- `PGPASSWORD`: `CEmXLtbgjXajotgOzxVyfvzFYfvbuxmd`

La URL sería:
```
postgresql://postgres:CEmXLtbgjXajotgOzxVyfvzFYfvbuxmd@containers-us-west-xxx.railway.app:5432/railway
```

---

## 🎯 Próximo Paso

Una vez que tengas la URL externa, ejecuta:

```powershell
$env:RAILWAY_DATABASE_URL="postgresql://postgres:password@host-externo.railway.app:5432/railway"
python sync_databases.py
```
