import os
import json
import requests
import feedparser
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from google import genai

# ============================================================
# 1. FUENTES RSS (política + economía, por medio)
# ============================================================
FUENTES = {
    "El País": [
        "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/espana/portada",
        "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/economia/portada",
    ],
    "El Mundo": [
        "https://e00-elmundo.uecdn.es/elmundo/rss/espana.xml",
        "https://e00-elmundo.uecdn.es/elmundo/rss/economia.xml",
    ],
    "ABC": [
        "https://www.abc.es/rss/feeds/abc_EspanaEspana.xml",
        "https://www.abc.es/rss/feeds/abc_Economia.xml",
    ],
    "La Vanguardia": [
        "https://www.lavanguardia.com/rss/politica.xml",
        "https://www.lavanguardia.com/rss/economia.xml",
    ],
    "elDiario.es": [
        "https://www.eldiario.es/rss/politica/",
        "https://www.eldiario.es/rss/economia/",
    ],
}

ART = timezone(timedelta(hours=-3))
AHORA_ART = datetime.now(ART)
HACE_24H_ART = AHORA_ART - timedelta(hours=24)

# ============================================================
# 2. RECOLECTAR + FILTRAR POR FECHA (últimas 24h en ART)
# ============================================================
def recolectar():
    noticias = []
    urls_vistas = set()

    for medio, feeds in FUENTES.items():
        for url in feeds:
            try:
                respuesta = requests.get(
                    url, headers={"User-Agent": "Mozilla/5.0"}, timeout=20
                )
                respuesta.raise_for_status()
                contenido = respuesta.content
                if medio == "La Vanguardia":
                    contenido = contenido.decode("utf-8", errors="replace").encode("utf-8")
                feed = feedparser.parse(contenido)
            except Exception as error:
                print(f"⚠️  {medio}: error al leer {url} -> {error}")
                continue

            for entrada in feed.entries:
                fecha_texto = entrada.get("published")
                if not fecha_texto:
                    continue
                try:
                    fecha = parsedate_to_datetime(fecha_texto)
                    if fecha.tzinfo is None:
                        fecha = fecha.replace(tzinfo=timezone.utc)
                    fecha_art = fecha.astimezone(ART)
                except Exception:
                    continue

                if not (HACE_24H_ART <= fecha_art <= AHORA_ART):
                    continue

                link = entrada.get("link", "").strip()
                if not link or link in urls_vistas:
                    continue
                urls_vistas.add(link)

                noticias.append({
                    "medio": medio,
                    "titulo": entrada.get("title", "").strip(),
                    "url": link,
                    "fecha_art": fecha_art.isoformat(),
                })

    return noticias

# ============================================================
# 3. LIMPIEZA SIMPLE (solo basura evidente)
# ============================================================
BASURA_EVIDENTE = [
    "horoscopo", "loteria", "sorteo", "resultado del sorteo",
    "receta", "crucigrama", "el tiempo hoy", "previsión meteorológica",
]

def limpiar(noticias):
    limpio = []
    for n in noticias:
        titulo = n["titulo"].lower()
        if any(palabra in titulo for palabra in BASURA_EVIDENTE):
            continue
        limpio.append(n)
    return limpio

# ============================================================
# 4. GEMINI: CLASIFICA, AGRUPA Y PRIORIZA
# ============================================================
def preguntar_a_gemini(noticias):
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

    lista_texto = "\n".join(
        f"{i}) MEDIO: {n['medio']} | TITULO: {n['titulo']} | URL: {n['url']}"
        for i, n in enumerate(noticias)
    )

    prompt = f"""Sos un editor político especializado en España, escribiendo para consultores y políticos.

Te paso una lista numerada de noticias (medio, título, URL) publicadas en las últimas 24 horas.

Orden de prioridad de medios (usalo para decidir el "medio_principal" de cada acontecimiento): 1) El País, 2) El Mundo, 3) ABC, 4) La Vanguardia, 5) elDiario.es.

Tarea:
1. Descartá todo lo que NO sea política o economía de impacto real a nivel nacional o de comunidad autónoma (nada de deportes, sucesos, clima, cultura, tráfico, salud, sociedad general).
2. Agrupá las noticias que hablan del MISMO acontecimiento puntual (no un tema genérico ni una crisis en curso con muchas aristas: solo agrupá artículos que cubren el mismo hecho concreto, por ejemplo la misma declaración, el mismo anuncio, la misma votación).
3. Para cada acontecimiento, elegí como "medio_principal" el de mayor prioridad según el orden de arriba entre los que lo cubrieron, con su titular y URL exactos.
4. En "mismo_hecho_cubierto_por" incluí COMO MÁXIMO UN artículo por cada medio adicional (el más representativo de ese medio sobre ese mismo hecho puntual) — nunca dos URLs del mismo medio en la misma lista.
5. Si un medio publicó varias notas relacionadas con un tema amplio (por ejemplo una crisis en curso) pero cada nota cubre un ángulo o hecho distinto, tratalas como acontecimientos separados, no las agrupes todas juntas.
6. Ordená los acontecimientos por relevancia/impacto, de mayor a menor.
7. Quedate como máximo con 12 acontecimientos.

Noticias:
{lista_texto}

Devolvé EXCLUSIVAMENTE un JSON válido (sin texto adicional, sin markdown) con este formato exacto:
{{
  "acontecimientos": [
    {{
      "tema": "NOMBRE BREVE DEL TEMA EN MAYUSCULAS",
      "medio_principal": "Nombre del medio",
      "titular_principal": "Titular exacto tal cual fue publicado",
      "url_principal": "URL exacta de la lista",
      "mismo_hecho_cubierto_por": [
        {{"medio": "Nombre del medio", "url": "URL exacta de la lista"}}
      ]
    }}
  ]
}}

Importante: los títulos y URLs deben ser EXACTAMENTE los de la lista que te pasé, no inventes ni modifiques nada. Nunca repitas el mismo medio dos veces en el mismo acontecimiento (ni como principal ni en la lista de cobertura adicional)."""

    respuesta = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
    )

    texto = respuesta.text.strip()
    if texto.startswith("```"):
        texto = texto.strip("`")
        texto = texto.split("\n", 1)[1] if "\n" in texto else texto

    return json.loads(texto)

# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    print(f"Ahora (ART): {AHORA_ART.isoformat()}")
    print(f"Desde (ART): {HACE_24H_ART.isoformat()}")
    print()

    noticias = recolectar()
    print(f"Noticias recolectadas (últimas 24h): {len(noticias)}")

    noticias = limpiar(noticias)
    print(f"Noticias tras limpieza simple: {len(noticias)}")
    print()

    if not noticias:
        print("No hay noticias para procesar. Fin.")
    else:
        resultado = preguntar_a_gemini(noticias)
        print(json.dumps(resultado, ensure_ascii=False, indent=2))
