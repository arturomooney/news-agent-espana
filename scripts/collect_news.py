import feedparser

# RSS oficiales de los cinco medios
FEEDS = {
    "El País": "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/espana/portada",
    "El Mundo": "https://e00-elmundo.uecdn.es/elmundo/rss/espana.xml",
    "ABC": "https://www.abc.es/rss/feeds/abc_EspanaEspana.xml",
    "La Vanguardia": "https://www.lavanguardia.com/rss/politica.xml",
    "elDiario.es": "https://www.eldiario.es/rss/politica/"
}

print("===== PRUEBA DE RSS =====\n")

for medio, rss in FEEDS.items():
    print(f"--- {medio} ---")

    feed = feedparser.parse(rss)

    print(f"Noticias encontradas: {len(feed.entries)}")

    # Mostrar solo las primeras 5 noticias de cada medio
    for noticia in feed.entries[:5]:
        print("•", noticia.title)

    print()
