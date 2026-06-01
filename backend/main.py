"""
FER AI - Main Loop Principal
==============================
Punto de entrada de FER.
Escucha → Procesa → Habla → Repite.
"""

import sys
import time
from brain import process_input
from voice import speak, inicializar_engine
from listen import listen
from personality import frase_activacion, frase_no_escucho
from memory import limpiar_memoria, resumen_sesion

# ──────────────────────────────────────────────
# COMANDOS ESPECIALES (sin pasar por la IA)
# ──────────────────────────────────────────────

COMANDOS_SALIDA = ["salir", "exit", "apagarte", "chau fer", "hasta luego fer", "cerrar"]
COMANDOS_MEMORIA = ["olvidá todo", "borrá la memoria", "empezá de cero"]
COMANDOS_RESUMEN = ["cuánto llevamos", "resumen de sesión", "qué hablamos"]


def manejar_comandos_especiales(texto: str) -> bool:
    """
    Detecta comandos especiales.
    Devuelve True si fue un comando especial (para no mandarlo a la IA).
    """
    texto_lower = texto.lower()

    # Salida
    if any(cmd in texto_lower for cmd in COMANDOS_SALIDA):
        speak("Nos vemos Fernando. Cuando me necesites, acá voy a estar.")
        print("\n👋 FER apagado por el usuario.")
        sys.exit(0)

    # Limpiar memoria
    if any(cmd in texto_lower for cmd in COMANDOS_MEMORIA):
        limpiar_memoria()
        speak("Memoria limpiada. Empezamos de cero, como si nunca nos hubiéramos conocido. Igual me vas a extrañar.")
        return True

    # Resumen de sesión
    if any(cmd in texto_lower for cmd in COMANDOS_RESUMEN):
        resumen = resumen_sesion()
        speak(resumen)
        return True

    return False


# ──────────────────────────────────────────────
# VERIFICAR OLLAMA ANTES DE ARRANCAR
# ──────────────────────────────────────────────

def verificar_ollama() -> bool:
    """Verifica que Ollama esté corriendo antes de arrancar."""
    import requests
    try:
        r = requests.get("http://localhost:11434/api/tags", timeout=3)
        if r.status_code == 200:
            modelos = r.json().get("models", [])
            nombres = [m["name"] for m in modelos]
            print(f"✅ Ollama activo. Modelos disponibles: {nombres}")
            return True
        return False
    except Exception:
        return False


# ──────────────────────────────────────────────
# INICIO DE FER
# ──────────────────────────────────────────────

def main():
    print("=" * 50)
    print("🔥  FER AI — INICIANDO  🔥")
    print("=" * 50)

    # Verificar Ollama
    print("\n🔍 Verificando Ollama...")
    if not verificar_ollama():
        print("❌ ERROR: Ollama no está corriendo.")
        print("   Abrí una terminal y ejecutá: ollama serve")
        print("   Luego volvé a correr main.py")
        input("\nPresioná Enter para salir...")
        sys.exit(1)

    # Inicializar TTS
    print("\n🔊 Inicializando voz...")
    inicializar_engine()

    # Saludo de activación
    saludo = frase_activacion()
    print(f"\n🤖 FER: {saludo}")
    speak(saludo)

    print("\n" + "─" * 50)
    print("💬 FER está escuchando. Hablá cuando quieras.")
    print("   Decí 'salir' o 'chau FER' para apagarlo.")
    print("─" * 50 + "\n")

    # ──────────────────────────────────────────
    # LOOP PRINCIPAL
    # ──────────────────────────────────────────

    intentos_vacios = 0  # Contador de veces sin escuchar nada

    while True:
        try:
            # 1. ESCUCHAR
            texto_usuario = listen()

            # Si no escuchó nada, seguir esperando
            if not texto_usuario:
                intentos_vacios += 1
                # Cada 10 intentos vacíos (~70 segundos), FER dice algo
                if intentos_vacios >= 10:
                    intentos_vacios = 0
                    # Solo a veces, no siempre (para no ser molesto)
                    import random
                    if random.random() < 0.3:  # 30% de probabilidad
                        frases_espera = [
                            "Che, ¿todo bien? Acá sigo esperando.",
                            "Seguís ahí Fernando?",
                        ]
                        frase = random.choice(frases_espera)
                        speak(frase)
                continue

            intentos_vacios = 0  # Resetear contador si escuchó algo

            # 2. COMANDOS ESPECIALES
            if manejar_comandos_especiales(texto_usuario):
                continue

            # 3. PROCESAR CON IA
            print("🧠 FER pensando...")
            respuesta = process_input(texto_usuario)

            # 4. HABLAR
            speak(respuesta)

            # Pausa pequeña entre turnos
            time.sleep(0.3)

        except KeyboardInterrupt:
            print("\n\n⚡ Ctrl+C detectado.")
            speak("Me cortaron. Hasta luego Fernando.")
            print("👋 FER apagado.")
            sys.exit(0)

        except Exception as e:
            print(f"❌ Error en loop principal: {e}")
            time.sleep(1)  # Pausa antes de reintentar
            continue


# ──────────────────────────────────────────────
# ENTRY POINT
# ──────────────────────────────────────────────

if __name__ == "__main__":
    main()
