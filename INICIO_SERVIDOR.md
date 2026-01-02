# 🚀 Cómo Iniciar el Servidor

## Problema: "No se puede acceder a este sitio web"

Si ves este error, el servidor no está corriendo. Sigue estos pasos:

## ✅ Solución Rápida

### Opción 1: Usar el archivo batch (MÁS FÁCIL)

1. **Haz doble clic en `start_server.bat`**
   - Se abrirá una ventana negra (CMD)
   - Verás los mensajes del servidor
   - **NO CIERRES ESA VENTANA** mientras uses la aplicación

2. **Espera a ver este mensaje:**
   ```
   🍳 SISTEMA DE GESTIÓN DE MENÚS FAMILIARES
   📱 Interfaz de administración: http://localhost:7000
   ```

3. **Abre tu navegador** en: http://localhost:7000

### Opción 2: Desde PowerShell/CMD

1. **Abre PowerShell o CMD**

2. **Navega a la carpeta:**
   ```powershell
   cd C:\Users\joe_freightos\Desktop\JAXOKITCHEN
   ```

3. **Ejecuta:**
   ```bash
   python app.py
   ```

4. **Verás algo como:**
   ```
   ============================================================
   🍳 SISTEMA DE GESTIÓN DE MENÚS FAMILIARES
   ============================================================
   
   💻 Running in DEVELOPMENT mode
   
   📱 Interfaz de administración: http://localhost:7000
   📺 Vista de TV: http://localhost:7000/tv
   ```

5. **Mantén la ventana abierta** y abre http://localhost:7000

## ⚠️ IMPORTANTE

- **El servidor debe estar corriendo** para acceder a la aplicación
- **Mantén la ventana de terminal abierta** mientras uses la app
- Si cierras la ventana, el servidor se detiene

## 🔍 Verificar si el Servidor Está Corriendo

Ejecuta esto en PowerShell:
```powershell
netstat -ano | findstr ":7000"
```

Si ves algo como `LISTENING`, el servidor está activo.

## 🐛 Si Sigue Sin Funcionar

1. **Verifica que Python esté instalado:**
   ```bash
   python --version
   ```

2. **Verifica las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Revisa los errores** en la ventana donde ejecutaste `python app.py`

4. **Prueba otro puerto** si el 7000 está ocupado:
   - Edita `app.py` línea 465
   - Cambia `port = int(os.getenv('PORT', 7000))` a `port = int(os.getenv('PORT', 8000))`
   - Reinicia el servidor

## 📞 Ayuda Adicional

Si ves errores específicos al iniciar el servidor, compártelos para ayudarte a solucionarlos.

