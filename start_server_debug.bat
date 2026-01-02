@echo off
title Servidor Flask - Debug Mode
color 0B

echo ============================================================
echo    INICIANDO SERVIDOR CON MODO DEBUG
echo ============================================================
echo.
echo Este script iniciara el servidor y mostrara todos los errores
echo NO CIERRES ESTA VENTANA mientras uses la aplicacion
echo.
echo ============================================================
echo.

cd /d "%~dp0"

echo Verificando Python...
python --version
if errorlevel 1 (
    echo ERROR: Python no encontrado. Instala Python primero.
    pause
    exit /b 1
)

echo.
echo Verificando dependencias...
python -c "import flask; print('Flask OK')" 2>nul
if errorlevel 1 (
    echo ERROR: Flask no instalado. Ejecuta: pip install -r requirements.txt
    pause
    exit /b 1
)

echo.
echo ============================================================
echo Iniciando servidor Flask...
echo ============================================================
echo.

python app.py

echo.
echo ============================================================
echo El servidor se detuvo.
echo ============================================================
pause


