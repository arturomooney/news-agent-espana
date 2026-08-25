import requests
import feedparser


FUENTES = {
    "El País": "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/portada",
    "El Mundo": "https://e00-elmundo.uecdn.es/elmundo/rss/portada.xml",
    "elDiario.es": "https://www.eldiario.es/rss",
}


for medio, url in FUENTES.items():

    print("=" * 60)
    print(medio)
    print(url)
    print("=" * 60)

    try:
        respuesta = requests.get(url, timeout=20)
        respuesta.raise_for_status()

        feed = feedparser.parse(respuesta.content)

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
