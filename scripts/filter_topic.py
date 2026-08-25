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


# ============================================================
# POLÍTICA
# ============================================================

PALABRAS_POLITICA = [
    "gobierno",
    "gobierno de españa",
    "moncloa",
    "congreso",
    "senado",
    "parlamento",
    "parlament",
    "cortes",
    "diputados",
    "senadores",
    "ministro",
    "ministra",
    "presidente del gobierno",
    "presidenta del gobierno",
    "presidente autonómico",
    "presidente autonomico",
    "presidenta autonómica",
    "presidenta autonomica",
    "psoe",
    "pp",
    "vox",
    "sumar",
    "podemos",
    "junts",
    "erc",
    "bildu",
    "pnv",
    "feijóo",
    "feijoo",
    "sánchez",
    "sanchez",
    "ayuso",
    "puigdemont",
    "yolanda díaz",
    "yolanda diaz",
    "elecciones",
    "electoral",
    "elección",
    "eleccion",
    "votación",
    "votacion",
    "investidura",
    "moción de censura",
    "mocion de censura",
    "coalición de gobierno",
    "coalicion de gobierno",
    "pacto de gobierno",
    "oposición",
    "oposicion",
    "presupuestos generales",
    "boe",
    "decreto ley",
    "decreto-ley",
    "reforma legal",
    "reforma de la ley",
    "ley de",
    "amnistía",
    "amnistia",
    "inmigración",
    "inmigracion",
    "migrantes",
    "migrantes",
    "frontera",
    "fronteras",
    "ceuta",
    "melilla",
    "guardia civil",
    "policía nacional",
    "policia nacional",
    "marlaska",
    "interior",
    "defensa",
    "sanidad",
    "justicia",
    "fiscal general",
    "tribunal constitucional",
    "tribunal supremo",
    "generalitat",
    "xunta",
]


# ============================================================
# ECONOMÍA
# ============================================================

PALABRAS_ECONOMIA = [
    "economía",
    "economia",
    "pib",
    "crecimiento económico",
    "crecimiento economico",
    "inflación",
    "inflacion",
    "ipc",
    "empleo",
    "empleados",
    "paro",
    "desempleo",
    "mercado laboral",
    "salario",
    "salarios",
    "sueldo",
    "sueldos",
    "impuestos",
    "fiscal",
    "déficit",
    "deficit",
    "deuda pública",
    "deuda publica",
    "deuda del estado",
    "presupuesto",
    "presupuestos",
    "banco de españa",
    "banco central",
    "bancos",
    "banca",
    "empresa",
    "empresas",
    "multinacional",
    "energía",
    "energia",
    "electricidad",
    "gas",
    "petróleo",
    "petroleo",
    "vivienda",
    "hipoteca",
    "hipotecas",
    "alquiler",
    "alquileres",
    "pensiones",
    "pensión",
    "pension",
    "inversión",
    "inversion",
    "inversiones",
    "mercados",
    "mercado",
    "industria",
    "exportaciones",
    "importaciones",
    "consumo",
    "producción",
    "produccion",
    "recesión",
    "recesion",
    "tipos de interés",
    "tipos de interes",
    "tipo de interés",
    "tipo de interes",
    "euríbor",
    "euribor",
    "finanzas",
    "opa",
    "cotización",
    "cotizacion",
    "acciones",
    "bolsa",
    "aranceles",
    "arancel",
    "comercio exterior",
    "licitaciones",
]


# ============================================================
# TÉRMINOS QUE INDICAN ESPAÑA
# ============================================================

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
    "catalunya",
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
    "castilla y leon",
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


# ============================================================
# SECCIONES CLARAMENTE EXCLUIDAS
# ============================================================

SECCIONES_EXCLUIDAS = [
    "/deportes/",
    "/futbol/",
    "/fútbol/",
    "/baloncesto/",
    "/tenis/",
    "/motor/",
    "/cultura/",
    "/television/",
    "/televisión/",
    "/cine/",
    "/series/",
    "/gastronomia/",
    "/gastronomía/",
    "/viajes/",
    "/viaje/",
    "/estilo/",
    "/familia/",
    "/salud/",
    "/ciencia/",
    "/medio-ambiente/",
    "/medio-ambiente",
    "/clima-y-medio-ambiente/",
    "/sociedad/",
    "/historia/",
    "/play/",
]


# ============================================================
# SECCIONES POLÍTICAS
# ============================================================

SECCIONES_POLITICA = [
    "/politica/",
    "/política/",
    "/espana/politica/",
    "/espana/política/",
    "/espana/",
    "/madrid/",
    "/cataluna/",
    "/catalunya/",
    "/andalucia/",
    "/galicia/",
    "/pais-vasco/",
    "/euskadi/",
    "/navarra/",
]


# ============================================================
# SECCIONES ECONÓMICAS
# ============================================================

SECCIONES_ECONOMIA = [
    "/economia/",
    "/economía/",
    "/empresas/",
    "/mercados/",
    "/finanzas/",
    "/banca/",
    "/vivienda/",
]


# ============================================================
# RUIDO: PALABRAS QUE SUELE SER MEJOR DESCARTAR
# ============================================================

PALABRAS_RUIDO = [
    "podcast",
    "horóscopo",
    "horoscopo",
    "receta",
    "recetas",
    "moda",
    "belleza",
    "restaurante",
    "restaurantes",
    "gastronomía",
    "gastronomia",
    "viaje",
    "viajes",
    "película",
    "pelicula",
    "serie",
    "series",
    "actor",
    "actriz",
    "fútbol",
    "futbol",
    "baloncesto",
    "tenis",
    "motor",
    "videojuego",
    "videojuegos",
    "libro",
    "novela",
    "música",
    "musica",
    "concierto",
    "arte",
    "artista",
    "historia",
    "arqueología",
    "arqueologia",
]


# ============================================================
# TÉRMINOS DEMASIADO GENÉRICOS
# No deben servir solos para clasificar una noticia.
# ============================================================

PALABRAS_DEBILES = [
    "ley",
    "presidente",
    "presidenta",
    "empresa",
    "empresas",
    "madrid",
    "barcelona",
    "españa",
    "espana",
    "español",
    "española",
    "espanol",
    "espanola",
    "mercado",
    "banco",
    "bancos",
    "gobierno",
]


AHORA = datetime.now(timezone.utc)
HACE_24_HORAS = AHORA - timedelta(hours=24)


def contiene_alguna(texto, palabras):
    return any(
        palabra in texto
        for palabra in palabras
    )


def contar_coincidencias(texto, palabras):
    return sum(
        1
        for palabra in palabras
        if palabra in texto
    )


def normalizar(texto):
    return texto.lower().strip()


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

            fecha_texto = noticia.get(
                "published"
            )

            if not fecha_texto:
                continue

            try:

                fecha = parsedate_to_datetime(
                    fecha_texto
                )

                if fecha.tzinfo is None:
                    fecha = fecha.replace(
                        tzinfo=timezone.utc
                    )

                fecha_utc = fecha.astimezone(
                    timezone.utc
                )

            except Exception:
                continue

            if not (
                HACE_24_HORAS
                <= fecha_utc
                <= AHORA
            ):
                continue

            titulo = noticia.get(
                "title",
                ""
            ).strip()

            descripcion = noticia.get(
                "summary",
                ""
            ).strip()

            url_noticia = noticia.get(
                "link",
                ""
            ).strip()

            titulo_normalizado = normalizar(
                titulo
            )

            descripcion_normalizada = normalizar(
                descripcion
            )

            url_normalizada = normalizar(
                url_noticia
            )

            texto = (
                f"{titulo_normalizado} "
                f"{descripcion_normalizada}"
            )

            # ------------------------------------------------
            # EXCLUSIONES
            # ------------------------------------------------

            if contiene_alguna(
                url_normalizada,
                SECCIONES_EXCLUIDAS
            ):
                continue

            if contiene_alguna(
                titulo_normalizado,
                PALABRAS_RUIDO
            ):
                continue

            # ------------------------------------------------
            # SECCIÓN DEL MEDIO
            # ------------------------------------------------

            politica_seccion = contiene_alguna(
                url_normalizada,
                SECCIONES_POLITICA
            )

            economia_seccion = contiene_alguna(
                url_normalizada,
                SECCIONES_ECONOMIA
            )

            # ------------------------------------------------
            # COINCIDENCIAS TEMÁTICAS
            # ------------------------------------------------

            coincidencias_politica = contar_coincidencias(
                texto,
                PALABRAS_POLITICA
            )

            coincidencias_economia = contar_coincidencias(
                texto,
                PALABRAS_ECONOMIA
            )

            coincidencias_espana = contar_coincidencias(
                texto,
                PALABRAS_ESPANA
            )

            coincidencias_debiles = contar_coincidencias(
                texto,
                PALABRAS_DEBILES
            )

            # ------------------------------------------------
            # POLÍTICA
            #
            # Si la URL está claramente en política,
            # aceptamos.
            #
            # Si no, necesitamos al menos dos señales
            # políticas, o una señal fuerte + España.
            # ------------------------------------------------

            es_politica = False

            if politica_seccion:
                es_politica = True

            elif coincidencias_politica >= 2:
                es_politica = True

            elif (
                coincidencias_politica >= 1
                and coincidencias_espana >= 1
                and coincidencias_debiles < 3
            ):
                es_politica = True

            # ------------------------------------------------
            # ECONOMÍA
            #
            # Una sección económica clara alcanza.
            #
            # Fuera de ella necesitamos señales económicas
            # suficientes.
            # ------------------------------------------------

            es_economia = False

            if economia_seccion:
                es_economia = True

            elif coincidencias_economia >= 2:
                es_economia = True

            elif (
                coincidencias_economia >= 1
                and coincidencias_espana >= 1
                and coincidencias_debiles < 3
            ):
                es_economia = True

            # ------------------------------------------------
            # FILTRO FINAL
            # ------------------------------------------------

            if not (
                es_politica
                or es_economia
            ):
                continue

            # Si la noticia NO pertenece a una sección
            # política/económica clara, exigimos además
            # alguna conexión explícita con España.

            if not (
                politica_seccion
                or economia_seccion
            ):

                if coincidencias_espana == 0:
                    continue

            seleccionadas.append({
                "titulo": titulo,
                "url": url_noticia,
                "fecha": fecha_utc,
                "politica": es_politica,
                "economia": es_economia,
            })

        # ----------------------------------------------------
        # ORDENAR POR FECHA
        # ----------------------------------------------------

        seleccionadas.sort(
            key=lambda noticia: noticia["fecha"],
            reverse=True
        )

        print(
            f"Noticias seleccionadas: "
            f"{len(seleccionadas)}"
        )

        print()

        for noticia in seleccionadas:

            categorias = []

            if noticia["politica"]:
                categorias.append(
                    "POLÍTICA"
                )

            if noticia["economia"]:
                categorias.append(
                    "ECONOMÍA"
                )

            categoria = " + ".join(
                categorias
            )

            print(
                f"[{categoria}]"
            )

            print(
                noticia["fecha"].isoformat()
            )

            print(
                noticia["titulo"]
            )

            print(
                noticia["url"]
            )

            print(
                "-" * 70
            )

    except Exception as error:

        print("❌ ERROR")
        print(error)

    print()
