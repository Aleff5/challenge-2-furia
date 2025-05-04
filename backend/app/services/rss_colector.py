# rss_collector.py
import feedparser
from typing import List, Dict

FEED_URLS = [
    "https://rss.app/feeds/Lp1i5ycfz93TQSw6.xml", #lol
    "https://rss.app/feeds/f1peIRY9y9cHf5Zl.xml", #cs news
    "https://rss.app/feeds/EXBkRpcSjLbUpos3.xml" ,#valorant
    "https://rss.app/feeds/RBToieE9mRPjBxTz.xml", #partidas cs
    "https://rss.app/feeds/74DhRLnSWttObl3P.xml", #twitter furia
]

def fetch_rss_feeds() -> List[Dict[str, str]]:
    entries = []
    for url in FEED_URLS:
        feed = feedparser.parse(url)
        for item in feed.entries:
            entries.append({
                "title": item.get("title", ""),
                "link": item.get("link", ""),
                "summary": item.get("summary", ""),
                "published": item.get("published", "")
            })
    return entries
