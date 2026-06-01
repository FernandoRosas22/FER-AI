"""
FER AI - Módulo de Voz (ElevenLabs + pyttsx3 respaldo)
"""

import os, requests, tempfile, subprocess, pyttsx3, re
from dotenv import load_dotenv

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")
ELEVENLABS_URL = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"

engine_respaldo = None

def inicializar_engine():
    global engine_respaldo
    try:
        engine_respaldo = pyttsx3.init()
        voces = engine_respaldo.getProperty("voices")
        voz_elegida = None
        for voz in voces:
            if any(lang in voz.id.lower() for lang in ["es", "spa"]):
                voz_elegida = voz.id
                break
        if not voz_elegida and voces:
            voz_elegida = voces[0].id
        if voz_elegida:
            engine_respaldo.setProperty("voice", voz_elegida)
        engine_respaldo.setProperty("rate", 165)
        engine_respaldo.setProperty("volume", 1.0)
        print("🔊 TTS inicializado. Voz principal: ElevenLabs | Respaldo: pyttsx3")
    except Exception as e:
        print(f"⚠️ Error pyttsx3: {e}")


def limpiar_para_tts(texto: str) -> str:
    emoji_pattern = re.compile(
        "[" "\U0001F600-\U0001F64F" "\U0001F300-\U0001F5FF"
        "\U0001F680-\U0001F6FF" "\U0001F1E0-\U0001F1FF"
        "\U00002702-\U000027B0" "\U000024C2-\U0001F251" "]+",
        flags=re.UNICODE
    )
    texto = emoji_pattern.sub("", texto)
    texto = texto.replace("*","").replace("_","").replace("#","")
    return " ".join(texto.split())


def calcular_duracion(texto: str) -> int:
    """Calcula duración aproximada del audio en segundos según largo del texto."""
    palabras = len(texto.split())
    # ~2.5 palabras por segundo + 2 segundos de margen
    return max(5, int(palabras / 2.5) + 2)


def speak_elevenlabs(texto: str) -> bool:
    try:
        headers = {
            "xi-api-key": ELEVENLABS_API_KEY,
            "Content-Type": "application/json"
        }
        payload = {
            "text": texto,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.85,
                "style": 0.3,
                "use_speaker_boost": True
            }
        }
        respuesta = requests.post(ELEVENLABS_URL, json=payload, headers=headers, timeout=15)

        if respuesta.status_code == 200:
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
                tmp.write(respuesta.content)
                tmp_path = tmp.name

            # Calcular duración real según el texto
            duracion = calcular_duracion(texto)

            subprocess.run(
                ["powershell", "-c",
                 f'Add-Type -AssemblyName presentationCore; '
                 f'$player = New-Object System.Windows.Media.MediaPlayer; '
                 f'$player.Open([uri]"{tmp_path}"); '
                 f'$player.Play(); '
                 f'Start-Sleep -Seconds {duracion}; '
                 f'$player.Stop(); '
                 f'$player.Close()'],
                capture_output=True,
                timeout=duracion + 5
            )
            try:
                os.unlink(tmp_path)
            except Exception:
                pass
            return True
        else:
            print(f"⚠️ ElevenLabs {respuesta.status_code}: {respuesta.text[:80]}")
            return False

    except Exception as e:
        print(f"⚠️ ElevenLabs falló: {e}")
        return False


def speak_respaldo(texto: str):
    global engine_respaldo
    try:
        if engine_respaldo is None:
            inicializar_engine()
        engine_respaldo.say(texto)
        engine_respaldo.runAndWait()
    except Exception as e:
        print(f"❌ Error TTS respaldo: {e}")
        engine_respaldo = None


def speak(texto: str):
    print(f"🔊 FER: {texto}")
    texto_limpio = limpiar_para_tts(texto)
    if ELEVENLABS_API_KEY and ELEVENLABS_VOICE_ID:
        if speak_elevenlabs(texto_limpio):
            return
    print("🔄 Usando voz de respaldo...")
    speak_respaldo(texto_limpio)


if __name__ == "__main__":
    inicializar_engine()
    speak("Son las 19:45, Fernando.")