# 🚀 Instrucciones para Iniciar el Servidor

## Problema: localhost no abre

Si localhost:7000 no abre, sigue estos pasos:

## Método 1: Usar el archivo batch (Más fácil)

1. **Doble clic en `start_server.bat`**
   - Se abrirá una ventana de terminal
   - Verás los mensajes del servidor
   - El servidor quedará corriendo en esa ventana

2. **Mantén la ventana abierta** mientras uses la aplicación

3. **Abre tu navegador** en: http://localhost:7000

## Método 2: Desde PowerShell/Terminal

1. **Abre PowerShell o CMD** en la carpeta del proyecto

2. **Ejecuta:**
   ```bash
   python app.py
   ```

3. **Verás algo como:**
   ```
   ============================================================
   🍳 SISTEMA DE GESTIÓN DE MENÚS FAMILIARES
   ============================================================
   
   💻 Running in DEVELOPMENT mode
   
   📱 Interfaz de administración: http://localhost:7000
   📺 Vista de TV: http://localhost:7000/tv
   ```

4. **Mantén la terminal abierta** y abre http://localhost:7000 en tu navegador

## Método 3: Verificar si el servidor está corriendo

Si crees que el servidor está corriendo pero no abre:

1. **Verifica el puerto:**
   ```powershell
   netstat -ano | findstr "7000"
   ```
   
   Si ves algo como `LISTENING`, el servidor está activo.

2. **Prueba diferentes URLs:**
   - http://localhost:7000
   - http://127.0.0.1:7000
   - http://0.0.0.0:7000

3. **Verifica el firewall:**
   - Windows puede estar bloqueando el puerto
   - Permite Python a través del firewall si te lo pide

## Solución de Problemas

### Error: "Port 7000 already in use"
- Otro programa está usando el puerto 7000
- Cierra otros programas o cambia el puerto en `app.py` (línea 339)

### Error: "Module not found"
- Instala las dependencias:
  ```bash
  pip install -r requirements.txt
  ```

### Error: "Cannot connect"
- Asegúrate de que el servidor esté corriendo
- Verifica que no haya errores en la terminal
- Prueba reiniciar el servidor

## Para Detener el Servidor

En la terminal donde está corriendo, presiona:
- **Ctrl + C**

O cierra la ventana de terminal.

## Verificación Rápida

Ejecuta esto para verificar que todo está bien:

```bash
python -c "from app import app; print('✅ Todo OK')"
```

Si ves "✅ Todo OK", el código está bien. Solo necesitas iniciar el servidor.

---

**¿Sigue sin funcionar?**
1. Verifica que Python esté instalado: `python --version`
2. Verifica que las dependencias estén instaladas
3. Revisa los mensajes de error en la terminal
4. Intenta usar otro puerto (cambia 7000 por 8000 en app.py)

