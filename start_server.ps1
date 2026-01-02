# Script para iniciar el servidor Flask en PowerShell
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Iniciando servidor Flask en puerto 7000..." -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Cambiar al directorio del script
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

# Iniciar el servidor
python app.py

Write-Host ""
Write-Host "Presiona cualquier tecla para salir..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")


