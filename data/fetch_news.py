import feedparser
from utils.text_cleaner import clean_text


def fetch_news(company, max_items=10):
    query = company.strip()
    if not query:
        return []
    rss_url = (
        "https://news.google.com/rss/search"
        f"?q={query}&hl=ko&gl=KR&ceid=KR:ko"
    )
    feed = feedparser.parse(rss_url)
    items = []
    for entry in feed.entries[:max_items]:
        items.append(
            {
                "title": clean_text(getattr(entry, "title", "")),
                "link": getattr(entry, "link", ""),
                "published": getattr(entry, "published", ""),
                "summary": clean_text(getattr(entry, "summary", "")),
            }
        )
    return items
