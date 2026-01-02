@echo off
title Servidor Flask - Auto-Reinicio
color 0A
mode con: cols=80 lines=25

:start
cls
echo ============================================================
echo    SERVIDOR FLASK - SISTEMA DE MENUS FAMILIARES
echo    Modo Auto-Reinicio Activo
echo ============================================================
echo.
echo Puerto: 7000
echo URL: http://localhost:7000
echo.
echo IMPORTANTE:
echo - Esta ventana DEBE permanecer abierta
echo - Si el servidor se cae, se reiniciara automaticamente
echo - Presiona Ctrl+C para detener completamente
echo.
echo ============================================================
echo Iniciando servidor...
echo ============================================================
echo.

cd /d "%~dp0"

python app.py

echo.
echo ============================================================
echo El servidor se detuvo.
echo ============================================================
echo.
echo Reiniciando en 5 segundos...
echo Presiona Ctrl+C para cancelar
echo ============================================================

timeout /t 5 /nobreak >nul 2>&1

goto start


