"""
FER AI - Módulo de Escucha (STT)
===================================
Captura voz del micrófono y la convierte a texto.
Usa Google Speech Recognition (gratis, sin key).
Idioma: es-AR (español argentino).
"""

import speech_recognition as sr
from personality import frase_no_escucho

# ──────────────────────────────────────────────
# INICIALIZACIÓN
# ──────────────────────────────────────────────

recognizer = sr.Recognizer()

# Calibración de sensibilidad al ruido ambiente
recognizer.energy_threshold = 300          # Sensibilidad al sonido
recognizer.dynamic_energy_threshold = True # Se adapta al ruido del ambiente
recognizer.pause_threshold = 0.8           # Segundos de silencio para cortar frase


# ──────────────────────────────────────────────
# FUNCIÓN PRINCIPAL DE ESCUCHA
# ──────────────────────────────────────────────

def listen() -> str:
    """
    Escucha el micrófono y devuelve el texto reconocido.
    Devuelve "" si no escuchó nada o hubo error.
    """
    try:
        with sr.Microphone() as source:
            print("🎤 Escuchando...")

            # Calibrar ruido ambiente (0.5 seg)
            recognizer.adjust_for_ambient_noise(source, duration=0.5)

            # Escuchar
            audio = recognizer.listen(
                source,
                timeout=7,          # Esperar hasta 7 seg a que hables
                phrase_time_limit=12 # Máximo 12 seg de frase
            )

        # Reconocer con Google (gratis, sin API key)
        print("⚙️  Procesando...")
        texto = recognizer.recognize_google(
            audio,
            language="es-AR"   # Español argentino
        )

        print(f"👤 Vos dijiste: {texto}")
        return texto.lower().strip()

    except sr.WaitTimeoutError:
        # No habló nada en el tiempo de espera — no imprimir nada, seguir loop
        return ""

    except sr.UnknownValueError:
        # Habló pero no se entendió
        print("❓ No entendí lo que dijiste.")
        return ""

    except sr.RequestError as e:
        # Error de conexión con Google Speech (necesita internet)
        print(f"❌ Error de Speech Recognition: {e}")
        print("   ⚠️  El reconocimiento de voz necesita conexión a internet.")
        return ""

    except OSError as e:
        # Micrófono no encontrado
        print(f"❌ Error de micrófono: {e}")
        print("   ⚠️  Verificá que el micrófono esté conectado y habilitado.")
        return ""

    except Exception as e:
        print(f"❌ Error inesperado en listen.py: {e}")
        return ""


# ──────────────────────────────────────────────
# TEST RÁPIDO
# ──────────────────────────────────────────────

if __name__ == "__main__":
    print("🎤 Test de listen.py — Hablá algo:")
    resultado = listen()
    if resultado:
        print(f"✅ Reconocido: '{resultado}'")
    else:
        print("❌ No se reconoció nada.")
