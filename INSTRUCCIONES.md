# 🔥 FER AI — INSTRUCCIONES DE INSTALACIÓN

## ¿Qué necesitás?
- Windows 10/11
- Python 3.10 o superior
- Ollama instalado (ya lo tenés)
- Micrófono funcionando
- Parlantes o auriculares
- Conexión a internet (solo para el reconocimiento de voz)

---

## PASO 1 — Descargar el modelo de IA

Abrí PowerShell y ejecutá:

```powershell
ollama pull mistral
```

Esto descarga el modelo (~4GB). Tardará según tu internet.
Cuando termine, el modelo queda guardado en tu PC para siempre.

---

## PASO 2 — Instalar dependencias de Python

En PowerShell, navegá a la carpeta del proyecto:

```powershell
cd C:\Users\Clarii\Desktop\FER-AI\backend
```

Activá el entorno virtual:

```powershell
.\venv\Scripts\activate
```

Instalá las dependencias:

```powershell
pip install -r requirements.txt
```

> ⚠️ Si PyAudio falla, instalalo así:
> ```powershell
> pip install pipwin
> pipwin install pyaudio
> ```

---

## PASO 3 — Iniciar Ollama

**IMPORTANTE:** Ollama tiene que estar corriendo ANTES de iniciar FER.

Abrí una terminal nueva (no cierres la otra) y ejecutá:

```powershell
ollama serve
```

Dejá esa terminal abierta. Verás algo como:
```
Ollama is running on http://localhost:11434
```

---

## PASO 4 — Iniciar FER

En la terminal original (con venv activado):

```powershell
python main.py
```

FER va a:
1. Verificar que Ollama esté corriendo ✅
2. Inicializar la voz ✅
3. Decir su frase de activación 🔊
4. Ponerse a escuchar tu micrófono 🎤

---

## COMANDOS ESPECIALES QUE ENTIENDE FER

| Lo que decís | Qué hace FER |
|---|---|
| "salir" / "chau FER" | Se apaga correctamente |
| "olvidá todo" | Borra la memoria de la sesión |
| "cuánto llevamos" | Dice cuántos intercambios llevamos |

---

## SOLUCIÓN DE PROBLEMAS

### ❌ "Ollama no está corriendo"
→ Abrí una terminal y ejecutá `ollama serve`

### ❌ PyAudio no instala
→ Ejecutá: `pip install pipwin` y luego `pipwin install pyaudio`

### ❌ No reconoce la voz
→ Verificá que el micrófono esté seleccionado como predeterminado en Windows

### ❌ FER responde pero muy lento
→ Normal con CPU. El modelo Mistral en CPU tarda 3-8 segundos. 
→ Para más velocidad podés probar: `ollama pull phi3` (modelo más liviano)

### ❌ Error "model not found"
→ Ejecutá `ollama pull mistral` en PowerShell

---

## ARQUITECTURA ACTUAL

```
FER-AI/
├── backend/
│   ├── main.py         ← Punto de entrada, loop principal
│   ├── brain.py        ← Cerebro (Ollama/Mistral)
│   ├── listen.py       ← Escucha el micrófono (Google STT)
│   ├── voice.py        ← Habla (pyttsx3 TTS)
│   ├── personality.py  ← Personalidad, humor, celos
│   ├── memory.py       ← Memoria de conversación
│   └── requirements.txt
└── frontend/           ← React/Vite (en desarrollo, no conectado aún)
```

---

## PRÓXIMOS PASOS (roadmap)

- [ ] Conectar frontend React con backend via FastAPI
- [ ] Memoria persistente con archivo JSON o Supabase
- [ ] Sonido de activación al iniciar
- [ ] Detección de palabra clave ("Hey FER") sin botón
- [ ] Panel web para ver conversaciones
- [ ] ElevenLabs para voz más realista
