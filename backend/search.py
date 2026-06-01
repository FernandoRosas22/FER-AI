"""
FER AI - Módulo de Búsqueda Web
"""

import requests
from datetime import datetime
import pytz

def buscar_web(query: str) -> str:
    try:
        r = requests.get(
            "https://api.duckduckgo.com/",
            params={"q": query, "format": "json", "no_html": 1, "skip_disambig": 1},
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=4
        )
        if r.status_code != 200:
            return ""
        data = r.json()
        # Solo el resultado más relevante, máximo 200 caracteres
        if data.get("Answer"):
            return data["Answer"][:200]
        if data.get("AbstractText"):
            return data["AbstractText"][:200]
        return ""
    except Exception:
        return ""


# Palabras que realmente necesitan búsqueda web (no la hora)
KEYWORDS_BUSQUEDA = [
    "partido", "resultado", "ganó", "gano", "perdió", "perdio",
    "tabla", "posiciones", "torneo", "fichó", "ficho", "contrató",
    "dólar", "dolar", "precio", "inflación", "inflacion", "cotización",
    "noticia", "último", "ultimo", "reciente",
    "clima", "temperatura", "lluvia",
    "presidente", "gobierno",
]

KEYWORDS_HORA = ["hora", "día", "fecha", "hoy es", "qué día", "que dia"]

def necesita_busqueda(texto: str) -> bool:
    texto_lower = texto.lower()
    # Si solo pregunta la hora/fecha, NO buscar en web
    if any(kw in texto_lower for kw in KEYWORDS_HORA):
        if not any(kw in texto_lower for kw in KEYWORDS_BUSQUEDA):
            return False
    return any(kw in texto_lower for kw in KEYWORDS_BUSQUEDA)


def obtener_contexto_completo(texto_usuario: str) -> str:
    partes = []

    # Hora real siempre (formato corto)
    try:
        tz = pytz.timezone("America/Argentina/Buenos_Aires")
        ahora = datetime.now(tz)
        partes.append(f"Hora actual: {ahora.strftime('%H:%M')} del {ahora.strftime('%d/%m/%Y')} (Argentina).")
    except Exception:
        pass

    # Búsqueda web solo si realmente hace falta
    if necesita_busqueda(texto_usuario):
        print("🌐 Buscando...")
        resultado = buscar_web(texto_usuario)
        if resultado:
            partes.append(f"Dato encontrado: {resultado}")
        else:
            partes.append("Sin datos actualizados. Si no sabés algo, decíselo honestamente a Fernando.")

    return "[CONTEXTO]\n" + "\n".join(partes) + "\n[/CONTEXTO]" if partes else ""