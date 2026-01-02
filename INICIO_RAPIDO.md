# 🚀 INICIO RÁPIDO DEL SERVIDOR

## ⚡ Solución Rápida (RECOMENDADO)

**Haz doble clic en:** `keep_server_alive.bat`

Este script:
- ✅ Inicia el servidor automáticamente
- ✅ Se reinicia automáticamente si se cae
- ✅ Muestra todos los mensajes y errores
- ✅ Mantiene el servidor corriendo

## 📋 Pasos Detallados

1. **Busca el archivo `keep_server_alive.bat`** en la carpeta del proyecto
2. **Haz doble clic** en él
3. **Espera** a ver este mensaje:
   ```
   ============================================================
   SERVIDOR FLASK - SISTEMA DE MENUS FAMILIARES
   ============================================================
   ```
4. **Mantén la ventana abierta** mientras uses la aplicación
5. **Abre tu navegador** en: http://localhost:7000

## ⚠️ IMPORTANTE

- **NO CIERRES** la ventana del servidor mientras uses la app
- Si se cierra, el servidor se detiene
- Si el servidor se cae, se reiniciará automáticamente en 5 segundos

## 🔍 Verificar que Está Corriendo

Abre otra ventana de PowerShell y ejecuta:
```powershell
netstat -ano | findstr ":7000"
```

Si ves `LISTENING`, el servidor está activo.

## 🐛 Si No Funciona

1. Verifica que Python esté instalado: `python --version`
2. Verifica las dependencias: `pip install -r requirements.txt`
3. Revisa la ventana del servidor para ver errores específicos


