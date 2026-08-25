import requests
import feedparser
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime


FUENTES = {
    "El País": "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/portada",
    "El Mundo": "https://e00-elmundo.uecdn.es/elmundo/rss/portada.xml",
    "elDiario.es": "https://www.eldiario.es/rss",
    "La Vanguardia": "https://www.lavanguardia.com/rss/politica.xml",
    "ABC": "https://www.abc.es/rss/2.0/portada",
}


PALABRAS_POLITICA = [
    "gobierno",
    "congreso",
    "senado",
    "moncloa",
    "ministro",
    "ministra",
    "presidente",
    "presidenta",
    "psoe",
    "pp",
    "vox",
    "sumar",
    "podemos",
    "feijóo",
    "feijoo",
    "sánchez",
    "sanchez",
    "ayuso",
    "elecciones",
    "electoral",
    "ley",
    "decreto",
    "diputados",
    "senadores",
    "parlamento",
    "cortes",
    "boe",
    "presupuestos",
    "moción de censura",
    "investidura",
]


PALABRAS_ECONOMIA = [
    "economía",
    "economia",
    "pib",
    "inflación",
    "inflacion",
    "ipc",
    "empleo",
    "paro",
    "desempleo",
    "salarios",
    "salario",
    "impuestos",
    "fiscal",
    "déficit",
    "deficit",
    "deuda",
    "banco de españa",
    "bancos",
    "empresa",
    "empresas",
    "energía",
    "energia",
    "vivienda",
    "hipotecas",
    "hipoteca",
    "pensiones",
    "pensión",
    "pension",
    "mercado laboral",
    "mercados",
    "inversión",
    "inversion",
    "industria",
]


PALABRAS_ESPANA = [
    "españa",
    "espana",
    "español",
    "española",
    "espanol",
    "espanola",
    "madrid",
    "barcelona",
    "cataluña",
    "cataluna",
    "andalucía",
    "andalucia",
    "valencia",
    "galicia",
    "país vasco",
    "pais vasco",
    "euskadi",
    "navarra",
    "aragón",
    "aragon",
    "castilla y león",
    "castilla-la mancha",
    "extremadura",
    "murcia",
    "asturias",
    "cantabria",
    "canarias",
    "baleares",
    "ceuta",
    "melilla",
    "generalitat",
    "parlament",
    "xunta",
]


AHORA = datetime.now(timezone.utc)
HACE_24_HORAS = AHORA - timedelta(hours=24)


def contiene_alguna(texto, palabras):
    return any(palabra in texto for palabra in palabras)


print("=" * 70)
print("FILTRO TEMÁTICO — POLÍTICA Y ECONOMÍA DE ESPAÑA")
print("=" * 70)
print()
print(f"Ahora (UTC): {AHORA.isoformat()}")
print(f"Desde (UTC): {HACE_24_HORAS.isoformat()}")
print()


for medio, url in FUENTES.items():

    print("=" * 70)
    print(medio)
    print("=" * 70)

    try:
        respuesta = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            timeout=20
        )
        respuesta.raise_for_status()

        contenido = respuesta.content

        if medio == "La Vanguardia":
            contenido = contenido.decode(
                "utf-8",
                errors="replace"
            ).encode("utf-8")

        feed = feedparser.parse(contenido)

        if feed.bozo and not feed.entries:
            print("❌ No se pudo leer el RSS")
            print(feed.bozo_exception)
            continue

        seleccionadas = []

        for noticia in feed.entries:

            fecha_texto = noticia.get("published")

            if not fecha_texto:
                continue

            try:
                fecha = parsedate_to_datetime(fecha_texto)

                if fecha.tzinfo is None:
                    fecha = fecha.replace(tzinfo=timezone.utc)

                fecha_utc = fecha.astimezone(timezone.utc)

            except Exception:
                continue

            if not (HACE_24_HORAS <= fecha_utc <= AHORA):
                continue

            titulo = noticia.get("title", "").strip()
            descripcion = noticia.get("summary", "").strip()

            texto = f"{titulo} {descripcion}".lower()

            es_politica = contiene_alguna(
                texto,
                PALABRAS_POLITICA
            )

            es_economia = contiene_alguna(
                texto,
                PALABRAS_ECONOMIA
            )

            es_espana = contiene_alguna(
                texto,
                PALABRAS_ESPANA
            )

            if (es_politica or es_economia) and es_espana:

                seleccionadas.append({
                    "titulo": titulo,
                    "url": noticia.get("link", ""),
                    "fecha": fecha_utc,
                    "politica": es_politica,
                    "economia": es_economia,
                })

        seleccionadas.sort(
            key=lambda noticia: noticia["fecha"],
            reverse=True
        )

        print(f"Noticias seleccionadas: {len(seleccionadas)}")
        print()

        for noticia in seleccionadas:

            categorias = []

            if noticia["politica"]:
                categorias.append("POLÍTICA")

            if noticia["economia"]:
                categorias.append("ECONOMÍA")

            categoria = " + ".join(categorias)

            print(f"[{categoria}]")
            print(noticia["fecha"].isoformat())
            print(noticia["titulo"])
            print(noticia["url"])
            print("-" * 70)

    except Exception as error:

        print("❌ ERROR")
        print(error)

    print()
