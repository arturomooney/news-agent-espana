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


AHORA = datetime.now(timezone.utc)
HACE_24_HORAS = AHORA - timedelta(hours=24)


print("=" * 70)
print("FILTRO DE ÚLTIMAS 24 HORAS")
print("=" * 70)
print()
print("Ahora (UTC):")
print(AHORA.isoformat())
print()
print("Desde (UTC):")
print(HACE_24_HORAS.isoformat())
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

        total = len(feed.entries)
        dentro_24h = []

        for noticia in feed.entries:

            fecha_texto = noticia.get("published")

            if not fecha_texto:
                fecha_texto = noticia.get("updated")

            if not fecha_texto:
                continue

            try:
                fecha = parsedate_to_datetime(fecha_texto)

                if fecha.tzinfo is None:
                    fecha = fecha.replace(tzinfo=timezone.utc)

                fecha_utc = fecha.astimezone(timezone.utc)

            except Exception:
                continue

            if HACE_24_HORAS <= fecha_utc <= AHORA:

                dentro_24h.append({
                    "titulo": noticia.get("title", "SIN TÍTULO"),
                    "url": noticia.get("link", "SIN URL"),
                    "fecha": fecha_utc,
                })

        print(f"Noticias totales: {total}")
        print(f"Noticias últimas 24 horas: {len(dentro_24h)}")
        print(f"Noticias descartadas: {total - len(dentro_24h)}")
        print()

        if dentro_24h:

            dentro_24h.sort(
                key=lambda noticia: noticia["fecha"],
                reverse=True
            )

            print("Más reciente incluida:")
            print(dentro_24h[0]["fecha"].isoformat())
            print(dentro_24h[0]["titulo"])
            print()

            print("Más antigua incluida:")
            print(dentro_24h[-1]["fecha"].isoformat())
            print(dentro_24h[-1]["titulo"])
            print()

    except Exception as error:

        print("❌ ERROR")
        print(error)

    print()
