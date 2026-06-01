@echo off
chcp 65001 >nul
title FER AI - Instalador
color 0A

echo.
echo ================================================
echo    FER AI - INSTALADOR AUTOMATICO
echo ================================================
echo.
echo Hola! Este instalador va a configurar FER en tu PC.
echo Por favor no cierres esta ventana.
echo.
pause

:: ── VERIFICAR PYTHON ──
echo.
echo [1/5] Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Python no esta instalado.
    echo.
    echo Por favor:
    echo   1. Abri el navegador
    echo   2. Entrá a https://www.python.org/downloads/
    echo   3. Descargá e instalá Python
    echo   4. IMPORTANTE: tildá "Add Python to PATH" al instalar
    echo   5. Volvé a ejecutar este archivo
    echo.
    pause
    exit
)
echo Python OK!

:: ── VERIFICAR OLLAMA ──
echo.
echo [2/5] Verificando Ollama...
ollama --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Ollama no esta instalado.
    echo.
    echo Por favor:
    echo   1. Abri el navegador
    echo   2. Entrá a https://ollama.com
    echo   3. Descargá e instalá Ollama para Windows
    echo   4. Volvé a ejecutar este archivo
    echo.
    pause
    exit
)
echo Ollama OK!

:: ── DESCARGAR MODELO ──
echo.
echo [3/5] Descargando el cerebro de FER (Mistral ~4GB)...
echo Esto puede tardar varios minutos segun tu internet.
echo No cierres esta ventana.
echo.
ollama pull mistral
if %errorlevel% neq 0 (
    echo ERROR descargando Mistral. Verificá tu conexion a internet.
    pause
    exit
)
echo Modelo descargado!

:: ── INSTALAR DEPENDENCIAS PYTHON ──
echo.
echo [4/5] Instalando dependencias de Python...
cd /d "%~dp0backend"

:: Crear entorno virtual
python -m venv venv
call venv\Scripts\activate.bat

:: Instalar dependencias
pip install --upgrade pip >nul
pip install SpeechRecognition PyAudio pyttsx3 requests python-dotenv pytz elevenlabs

:: Si PyAudio falla, intentar con pipwin
pip show PyAudio >nul 2>&1
if %errorlevel% neq 0 (
    echo Intentando instalar PyAudio de otra forma...
    pip install pipwin
    pipwin install pyaudio
)

echo Dependencias instaladas!

:: ── CREAR ACCESO DIRECTO EN ESCRITORIO ──
echo.
echo [5/5] Creando acceso directo en el escritorio...

:: Copiar INICIAR_FER.bat al escritorio
copy /Y "%~dp0INICIAR_FER.bat" "%USERPROFILE%\Desktop\INICIAR FER.bat" >nul
echo Acceso directo creado en el escritorio!

:: ── LISTO ──
echo.
echo ================================================
echo    INSTALACION COMPLETADA
echo ================================================
echo.
echo FER esta listo para usar!
echo.
echo Para iniciar FER:
echo   - Hacé doble click en "INICIAR FER" en el escritorio
echo   - O ejecutá INICIAR_FER.bat desde esta carpeta
echo.
echo IMPORTANTE: FER necesita internet para escuchar tu voz.
echo El cerebro de FER funciona sin internet.
echo.
pause
