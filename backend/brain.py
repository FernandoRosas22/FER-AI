"""
FER AI - Módulo Cerebro (Ollama + Búsqueda Web)
=================================================
Timeout aumentado. Contexto reducido para respuestas más rápidas.
"""

import requests
from personality import SYSTEM_PROMPT, detectar_celos, frase_error
from memory import agregar_mensaje, obtener_historial_para_ollama
from search import obtener_contexto_completo

OLLAMA_URL = "http://localhost:11434/api/chat"
MODELO = "mistral"

def process_input(texto_usuario: str) -> str:

    # ── Celos ──
    if detectar_celos(texto_usuario):
        texto_usuario = f"{texto_usuario} [FER está celoso]"

    # ── Memoria ──
    agregar_mensaje("user", texto_usuario)

    # ── Contexto real (corto y preciso) ──
    contexto = obtener_contexto_completo(texto_usuario)
    system_final = f"{SYSTEM_PROMPT}\n\n{contexto}" if contexto else SYSTEM_PROMPT

    # ── Solo los últimos 6 mensajes del historial para no saturar ──
    historial = obtener_historial_para_ollama()
    historial_reciente = historial[-6:] if len(historial) > 6 else historial

    mensajes = [{"role": "system", "content": system_final}] + historial_reciente

    try:
        respuesta = requests.post(
            OLLAMA_URL,
            json={
                "model": MODELO,
                "messages": mensajes,
                "stream": False,
                "options": {
                    "temperature": 0.8,
                    "num_predict": 120,   # Respuestas más cortas = más rápido
                }
            },
            timeout=90   # 90 segundos de timeout
        )

        if respuesta.status_code == 200:
            texto_respuesta = respuesta.json()["message"]["content"].strip()
            agregar_mensaje("assistant", texto_respuesta)
            return texto_respuesta
        else:
            print(f"❌ Error Ollama: {respuesta.status_code}")
            return frase_error()

    except requests.exceptions.ConnectionError:
        return "No puedo pensar ahora. Asegurate de que Ollama esté corriendo."

    except requests.exceptions.Timeout:
        print("⏱️ Timeout")
        return "Tardé demasiado, probá de nuevo."

    except Exception as e:
        print(f"❌ Error: {e}")
        return frase_error()