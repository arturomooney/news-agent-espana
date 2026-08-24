import feedparser

RSS_URL = "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/portada"

feed = feedparser.parse(RSS_URL)

print(f"Noticias encontradas: {len(feed.entries)}")
print()

for noticia in feed.entries[:10]:
    print("TÍTULO:", noticia.title)
    print("FECHA:", noticia.get("published", "Sin fecha"))
    print("URL:", noticia.link)
    print("-" * 60)
