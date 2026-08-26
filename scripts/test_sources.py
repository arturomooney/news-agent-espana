import requests
import feedparser


FUENTES = {
    "El País": [
        "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/espana/portada",
        "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/economia/portada"
    ],

    "El Mundo": [
        "https://e00-elmundo.uecdn.es/elmundo/rss/espana.xml",
        "https://e00-elmundo.uecdn.es/elmundo/rss/economia.xml"
    ],

    "ABC": [
        "https://www.abc.es/rss/feeds/abc_EspanaEspana.xml",
        "https://www.abc.es/rss/feeds/abc_Economia.xml"
    ],

    "La Vanguardia": [
        "https://www.lavanguardia.com/rss/politica.xml",
        "https://www.lavanguardia.com/rss/economia.xml"
    ],

    "elDiario.es": [
        "https://www.eldiario.es/rss/politica/",
        "https://www.eldiario.es/rss/economia/"
    ]
}


for medio, urls in FUENTES.items():

    print("=" * 60)
    print(medio)
    print("=" * 60)

    total = 0

    for url in urls:
        print(f"RSS: {url}")

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
            contenido = contenido.decode("utf-8", errors="replace").encode("utf-8")

        feed = feedparser.parse(contenido)

        if feed.bozo:
            print("❌ Error al leer el RSS")
            print(feed.bozo_exception)
            continue

        cantidad = len(feed.entries)

        print("✅ RSS funcionando")
        print(f"Noticias encontradas: {cantidad}")

        if cantidad > 0:
            print()
            print("Primeras 3 noticias:")

            for noticia in feed.entries[:3]:
                print("-", noticia.title)
                print(" ", noticia.link)

    except Exception as error:
        print("❌ Error al acceder al RSS")
        print(error)

    print()
