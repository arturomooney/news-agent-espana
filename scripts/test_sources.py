import feedparser

FUENTES = {
    "El País": "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/portada",
}


for medio, url in FUENTES.items():

    print("=" * 60)
    print(medio)
    print(url)
    print("=" * 60)

    feed = feedparser.parse(url)

    if feed.bozo:
        print("❌ Error al leer el RSS")
        print(feed.bozo_exception)
        continue

    cantidad = len(feed.entries)

    print(f"✅ RSS funcionando")
    print(f"Noticias encontradas: {cantidad}")

    if cantidad > 0:
        print()
        print("Primeras 3 noticias:")

        for noticia in feed.entries[:3]:
            print("-", noticia.title)
            print(" ", noticia.link)

    print()
