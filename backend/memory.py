"""
FER AI - Módulo de Memoria
===========================
Mantiene el historial de conversación para que FER recuerde
lo que se habló durante la sesión actual.
"""

from datetime import datetime

# ──────────────────────────────────────────────
# MEMORIA DE SESIÓN (en RAM, dura mientras corre)
# ──────────────────────────────────────────────

historial = []          # Lista de mensajes de la conversación
MAX_HISTORIAL = 20      # Máximo de turnos a recordar (para no saturar el contexto)


def agregar_mensaje(rol: str, contenido: str):
    """
    Agrega un mensaje al historial.
    rol: "user" o "assistant"
    """
    historial.append({
        "role": rol,
        "content": contenido,
        "timestamp": datetime.now().strftime("%H:%M")
    })

    # Mantener solo los últimos MAX_HISTORIAL mensajes
    if len(historial) > MAX_HISTORIAL:
        historial.pop(0)


def obtener_historial_para_ollama() -> list:
    """
    Devuelve el historial en formato que entiende Ollama/OpenAI.
    Solo role y content, sin timestamp.
    """
    return [
        {"role": m["role"], "content": m["content"]}
        for m in historial
    ]


def limpiar_memoria():
    """Resetea la memoria (por si Fernando quiere empezar de cero)."""
    historial.clear()
    print("🧹 Memoria limpiada.")


def resumen_sesion() -> str:
    """Devuelve un resumen breve de cuántos turnos lleva la sesión."""
    turnos = len([m for m in historial if m["role"] == "user"])
    return f"Llevamos {turnos} intercambios en esta sesión."
