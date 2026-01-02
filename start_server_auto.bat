@echo off
:start
echo ============================================================
echo Iniciando servidor Flask en puerto 7000...
echo ============================================================
echo.
echo Si el servidor se cae, se reiniciara automaticamente en 5 segundos
echo Presiona Ctrl+C para detener completamente
echo.
echo ============================================================
echo.

python app.py

echo.
echo ============================================================
echo El servidor se detuvo. Reiniciando en 5 segundos...
echo Presiona Ctrl+C para cancelar
echo ============================================================
timeout /t 5 /nobreak >nul

goto start


