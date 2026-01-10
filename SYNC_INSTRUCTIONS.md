# 🔄 Instrucciones para Sincronizar Base de Datos Local → Railway

## 📋 Pasos

### 1. Obtener la URL de la Base de Datos de Railway

1. Ve a: https://railway.app/
2. Selecciona tu proyecto
3. Click en el servicio **PostgreSQL** (no en "web")
4. Ve a la pestaña **Variables**
5. Copia el valor de `DATABASE_URL` (algo como: `postgresql://postgres:password@host:port/railway`)

### 2. Configurar Variable de Entorno

En PowerShell, ejecuta:

```powershell
$env:RAILWAY_DATABASE_URL="postgresql://postgres:password@host:port/railway"
```

**⚠️ IMPORTANTE**: Reemplaza la URL completa con la que copiaste de Railway.

### 3. Ejecutar el Script de Sincronización

```powershell
python sync_databases.py
```

El script:
- ✅ Conectará a tu base de datos local (SQLite)
- ✅ Conectará a Railway (PostgreSQL)
- ✅ Sincronizará todos los datos:
  - Adultos
  - Niños
  - Recetas
  - Menús semanales
  - Preferencias de menú

### 4. Verificar en Railway

1. Ve a: `https://web-production-57291.up.railway.app`
2. Verifica que tus perfiles familiares aparezcan
3. Verifica que tus menús aparezcan
4. Ve a `/tv` y deberías ver el menú

## 🔍 Troubleshooting

### Error: "RAILWAY_DATABASE_URL no está configurada"
- Asegúrate de haber ejecutado el comando `$env:RAILWAY_DATABASE_URL=...` antes de ejecutar el script
- Verifica que la URL sea correcta

### Error: "No se encuentra family_kitchen.db"
- Asegúrate de ejecutar el script desde el directorio del proyecto
- Verifica que el archivo `family_kitchen.db` existe

### Error de conexión a PostgreSQL
- Verifica que la URL de Railway sea correcta
- Asegúrate de que Railway esté funcionando
- Verifica que no haya espacios extra en la URL

## ✅ Resultado Esperado

Después de ejecutar el script, deberías ver:

```
🚀 Sincronizador de Base de Datos: Local → Railway

📦 Conectando a Railway PostgreSQL...

🔄 Iniciando sincronización...

1️⃣  Sincronizando adultos...
   📊 Encontrados X adultos en local
   ✅ Añadido: Nombre (ID: X)
   ...

2️⃣  Sincronizando niños...
   ...

3️⃣  Sincronizando recetas...
   ...

4️⃣  Sincronizando menús semanales...
   ...

5️⃣  Sincronizando preferencias de menú...
   ✅ Preferencias sincronizadas

✅ Sincronización completada!

📊 Resumen:
   - Adultos: X
   - Niños: X
   - Recetas: X
   - Menús: X

🎉 ¡Datos sincronizados exitosamente!
   Ahora puedes ver tus datos en Railway
```
