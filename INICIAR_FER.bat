@echo off
chcp 65001 >nul
title FER AI
color 0A

echo.
echo ================================================
echo    FER AI - INICIANDO...
echo ================================================
echo.

:: ── VERIFICAR QUE EXISTE EL PROYECTO ──
if not exist "%~dp0backend\main.py" (
    echo ERROR: No encontré los archivos de FER.
    echo Asegurate de ejecutar este archivo desde la carpeta FER-AI.
    pause
    exit
)

:: ── INICIAR OLLAMA EN SEGUNDO PLANO ──
echo Iniciando el cerebro de FER...
start /min "" ollama serve

:: Esperar 3 segundos a que Ollama arranque
timeout /t 3 /nobreak >nul

:: ── ACTIVAR ENTORNO VIRTUAL E INICIAR FER ──
echo Iniciando FER...
echo.
cd /d "%~dp0backend"
call venv\Scripts\activate.bat
python main.py

:: Si FER se cierra, mostrar mensaje
echo.
echo FER se cerró.
pause
