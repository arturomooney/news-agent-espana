import os
import json
import time
import html as html_lib
import requests
import feedparser
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from google import genai
from google.genai import errors as genai_errors

# ============================================================
# CONFIG
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

BASURA_EVIDENTE = [
    "horoscopo", "loteria", "sorteo", "resultado del sorteo",
    "receta", "crucigrama", "el tiempo hoy", "previsión meteorológica",
]

# ============================================================
# 1. RECOLECTAR + FILTRO 24H
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

                titulo = entrada.get("title", "").strip()
                if any(palabra in titulo.lower() for palabra in BASURA_EVIDENTE):
                    continue

                noticias.append({
                    "medio": medio,
                    "titulo": titulo,
                    "url": link,
                })

    return noticias

# ============================================================
# 2. GEMINI — devuelve ÍNDICES, no URLs (así nunca se rompen)
# ============================================================
def preguntar_a_gemini(noticias, intentos=4):
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

    lista_texto = "\n".join(
        f"{i}) MEDIO: {n['medio']} | TITULO: {n['titulo']}"
        for i, n in enumerate(noticias)
    )

    prompt = f"""Sos un editor político especializado en España, escribiendo para consultores y políticos.

Te paso una lista numerada de noticias (medio, título) publicadas en las últimas 24 horas. Vas a trabajar SOLO con los números de esa lista, nunca con URLs ni con texto reescrito.

Orden de prioridad de medios (usalo para decidir cuál es el "indice_principal" de cada acontecimiento): 1) El País, 2) El Mundo, 3) ABC, 4) La Vanguardia, 5) elDiario.es.

Tarea:
1. Descartá todo lo que NO sea política o economía de impacto real a nivel nacional o de comunidad autónoma (nada de deportes, sucesos, clima, cultura, tráfico, salud, sociedad general).
2. Agrupá las noticias que hablan del MISMO acontecimiento puntual (no un tema genérico ni una crisis en curso con muchas aristas: solo agrupá artículos que cubren el mismo hecho concreto).
3. Para cada acontecimiento, elegí como "indice_principal" el número, según la lista, del medio de mayor prioridad entre los que lo cubrieron.
4. En "indices_cobertura_adicional" incluí como máximo UN índice por cada medio adicional (nunca dos índices del mismo medio en el mismo acontecimiento, y nunca el mismo índice que ya usaste como principal).
5. Si un medio publicó varias notas relacionadas con un tema amplio pero cada nota cubre un ángulo distinto, tratalas como acontecimientos separados.
6. Ordená los acontecimientos por relevancia/impacto, de mayor a menor.
7. Quedate como máximo con 12 acontecimientos.

Noticias:
{lista_texto}

Devolvé EXCLUSIVAMENTE un JSON válido (sin texto adicional, sin markdown), con la clave exacta "acontecimientos", en este formato exacto:
{{
  "acontecimientos": [
    {{
      "tema": "NOMBRE BREVE DEL TEMA EN MAYUSCULAS",
      "indice_principal": 0,
      "indices_cobertura_adicional": [0, 0]
    }}
  ]
}}

Los números deben ser SIEMPRE los de la lista numerada de arriba. No repitas el mismo índice dos veces en un mismo acontecimiento."""

    respuesta = None
    for intento in range(1, intentos + 1):
        try:
            respuesta = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt,
            )
            break
        except genai_errors.ServerError as error:
            espera = 20 * intento
            print(f"⚠️  Gemini sobrecargado (intento {intento}/{intentos}): {error}. Esperando {espera}s...")
            time.sleep(espera)
        except Exception as error:
            espera = 20 * intento
            print(f"⚠️  Error llamando a Gemini (intento {intento}/{intentos}): {error}. Esperando {espera}s...")
            time.sleep(espera)

    if respuesta is None:
        raise RuntimeError("Gemini no respondió tras varios intentos. Se aborta esta corrida.")

    texto = respuesta.text.strip()
    if texto.startswith("```"):
        texto = texto.strip("`")
        texto = texto.split("\n", 1)[1] if "\n" in texto else texto

    datos = json.loads(texto)

    lista_acontecimientos = []
    for valor in datos.values():
        if isinstance(valor, list):
            lista_acontecimientos = valor
            break

    resultado = []
    for a in lista_acontecimientos:
        try:
            idx_principal = a["indice_principal"]
            principal = noticias[idx_principal]
        except (KeyError, IndexError, TypeError):
            continue

        cobertura = []
        medios_usados = {principal["medio"]}
        for idx in a.get("indices_cobertura_adicional", []):
            try:
                noticia = noticias[idx]
            except (IndexError, TypeError):
                continue
            if noticia["medio"] in medios_usados:
                continue
            medios_usados.add(noticia["medio"])
            cobertura.append(noticia)

        resultado.append({
            "tema": a.get("tema", "").strip(),
            "medio_principal": principal["medio"],
            "titular_principal": principal["titulo"],
            "url_principal": principal["url"],
            "mismo_hecho_cubierto_por": [
                {"medio": n["medio"], "url": n["url"]} for n in cobertura
            ],
        })

    return resultado

# ============================================================
# 3. ACORTAR URLS CON TinyURL
# ============================================================
def acortar(url, intentos=3):
    for intento in range(1, intentos + 1):
        try:
            respuesta = requests.get(
                "https://tinyurl.com/api-create.php",
                params={"url": url},
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=15,
            )
            texto = respuesta.text.strip()
            if respuesta.status_code == 200 and texto.startswith("http"):
                time.sleep(0.5)
                return texto
            print(f"⚠️  TinyURL intento {intento}/{intentos} falló para {url} -> respuesta: {texto!r}")
        except Exception as error:
            print(f"⚠️  TinyURL intento {intento}/{intentos} error para {url} -> {error}")
        time.sleep(2)

    print(f"⚠️  No se pudo acortar tras {intentos} intentos, uso URL completa: {url}")
    return url

# ============================================================
# 4. FORMATEAR PARA TELEGRAM (HTML, por bloques)
# ============================================================
def armar_bloques(acontecimientos):
    fecha_titulo = AHORA_ART.strftime("%d/%m")
    bloques = [f"<b>NOTICIAS ESPAÑA {fecha_titulo}</b>"]

    con_grupo = [a for a in acontecimientos if a["mismo_hecho_cubierto_por"]]
    sin_grupo = [a for a in acontecimientos if not a["mismo_hecho_cubierto_por"]]

    numero = 1
    for a in con_grupo:
        lineas = [f"<b>{numero}) {html_lib.escape(a['tema'].upper())}</b>"]
        lineas.append(f"Medio: {html_lib.escape(a['medio_principal'])}")
        lineas.append(f"Titular del medio: \"{html_lib.escape(a['titular_principal'])}\"")
        lineas.append(f"Fuente: {html_lib.escape(acortar(a['url_principal']))}")
        lineas.append("Mismo hecho cubierto por:")
        for cobertura in a["mismo_hecho_cubierto_por"]:
            medio = html_lib.escape(cobertura['medio'])
            link = html_lib.escape(acortar(cobertura['url']))
            lineas.append(f"- {medio} — {link}")
        bloques.append("\n".join(lineas))
        numero += 1

    if sin_grupo:
        lineas = [f"<b>{numero}) OTROS TEMAS</b>"]
        for a in sin_grupo:
            lineas.append(f"Medio: {html_lib.escape(a['medio_principal'])}")
            lineas.append(f"Titular del medio: \"{html_lib.escape(a['titular_principal'])}\"")
            lineas.append(f"Fuente: {html_lib.escape(acortar(a['url_principal']))}")
            lineas.append("")
        bloques.append("\n".join(lineas).strip())

    return bloques

def agrupar_en_mensajes(bloques, limite=3800):
    mensajes = []
    actual = ""
    for bloque in bloques:
        candidato = (actual + "\n\n" + bloque).strip() if actual else bloque
        if len(candidato) > limite and actual:
            mensajes.append(actual)
            actual = bloque
        else:
            actual = candidato
    if actual:
        mensajes.append(actual)
    return mensajes

# ============================================================
# 5. ENVIAR A TELEGRAM
# ============================================================
def enviar_telegram(mensajes):
    token = os.environ["TELEGRAM_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]
    url = f"https://api.telegram.org/bot{token}/sendMessage"

    for mensaje in mensajes:
        respuesta = requests.post(
            url,
            data={"chat_id": chat_id, "text": mensaje, "parse_mode": "HTML"},
            timeout=20,
        )
        if respuesta.status_code != 200:
            print("⚠️  Error enviando a Telegram:", respuesta.text)

# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    print(f"Ahora (ART): {AHORA_ART.isoformat()}")

    noticias = recolectar()
    print(f"Noticias últimas 24h (tras limpieza simple): {len(noticias)}")

    if not noticias:
        print("No hay noticias. No se envía nada.")
    else:
        acontecimientos = preguntar_a_gemini(noticias)
        print(f"Acontecimientos seleccionados por Gemini: {len(acontecimientos)}")

        bloques = armar_bloques(acontecimientos)
        mensajes = agrupar_en_mensajes(bloques)
        print(f"Se va a enviar en {len(mensajes)} mensaje(s) de Telegram.")

        for m in mensajes:
            print("=" * 70)
            print(m)
        print("=" * 70)

        enviar_telegram(mensajes)
        print("Enviado a Telegram.")
