@echo off
title Servidor Flask - Sistema de Menus Familiares
color 0A

:start
cls
echo ============================================================
echo    SISTEMA DE GESTION DE MENUS FAMILIARES
echo ============================================================
echo.
echo Iniciando servidor Flask en puerto 7000...
echo.
echo IMPORTANTE:
echo - Manten esta ventana abierta mientras uses la aplicacion
echo - Si el servidor se cae, se reiniciara automaticamente
echo - Presiona Ctrl+C para detener completamente
echo.
echo ============================================================
echo.

python app.py

echo.
echo ============================================================
echo El servidor se detuvo.
echo.
echo Opciones:
echo 1. Se reiniciara automaticamente en 10 segundos
echo 2. Presiona Ctrl+C para cancelar y salir
echo ============================================================
echo.

timeout /t 10 /nobreak

goto start


