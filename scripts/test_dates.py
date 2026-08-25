import requests
import feedparser


FUENTES = {
    "El País": "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/portada",
    "El Mundo": "https://e00-elmundo.uecdn.es/elmundo/rss/portada.xml",
    "elDiario.es": "https://www.eldiario.es/rss",
    "La Vanguardia": "https://www.lavanguardia.com/rss/politica.xml",
    "ABC": "https://www.abc.es/rss/2.0/portada",
}


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

        print(f"Noticias encontradas: {len(feed.entries)}")
        print()

        for noticia in feed.entries[:3]:

            print("TÍTULO:")
            print(noticia.get("title", "SIN TÍTULO"))

            print("URL:")
            print(noticia.get("link", "SIN URL"))

            print("FECHA:")
            print(noticia.get("published", "SIN FECHA"))

            print("FECHA ACTUALIZACIÓN:")
            print(noticia.get("updated", "SIN FECHA"))

            print("-" * 70)

    except Exception as error:

        print("❌ ERROR")
        print(error)

    print()
