# src/digest_generator.py

import os
import json
from datetime import datetime
from dotenv import load_dotenv
import requests

from summarizer import Summarizer

load_dotenv()

SERPAPI_KEY = os.getenv("SERPAPI_KEY")
SEARCH_QUERY = "machine learning OR artificial intelligence OR deep learning OR LLM OR large language model OR GPT OR NLP OR natural language " \
                "processing OR quantum computing OR generative AI OR ML algorithms OR reinforcement learning OR transformers"

SERPAPI_ENDPOINT = (
    f"https://serpapi.com/search.json?engine=google_news&q={SEARCH_QUERY}&hl=en&gl=us&api_key={SERPAPI_KEY}"
)

class DigestGenerator:
    def __init__(self):
        self.summarizer = Summarizer()

    def tag(self, summary: str):
        tags = []
        txt = summary.lower()
        if any(k in txt for k in ("paper", "research")):
            tags.append("research")
        if "job" in txt:
            tags.append("job advice")
        if any(k in txt for k in ("release", "update", "breaking")):
            tags.append("news")
        if any(k in txt for k in ("library", "tutorial")):
            tags.append("tools")
        return tags or ["other"]

    def run(self):
        ts = datetime.utcnow().strftime("%Y-%m-%d_%H-%M")
        os.makedirs("data", exist_ok=True)
        seen_path = "data/seen_ids.json"

        try:
            with open(seen_path, "r", encoding="utf-8") as f:
                seen_ids = set(json.load(f))
        except (FileNotFoundError, json.JSONDecodeError):
            seen_ids = set()

        md_lines, records = [], []

        try:
            r = requests.get(SERPAPI_ENDPOINT, timeout=10)
            r.raise_for_status()
            articles = r.json().get("news_results", [])
        except Exception as e:
            print(f"❌ Failed to fetch news from SerpAPI: {e}")
            return

        for article in articles:
            url = article.get("link")
            if url in seen_ids:
                print(f"Skipping seen article: {url}")
                continue

            title = article.get("title", "")
            content = article.get("snippet", "") or title
            if not content:
                continue

            summary = self.summarizer.summarize(content)
            tags = self.tag(summary)

            md_lines.append(
                f"## [{article.get('source', {}).get('name', 'Unknown')}] {title}\n\n"
                f"{summary}\n\n"
                f"[Read more]({url})\n\n"
                f"_Tags: {', '.join(tags)}_\n\n---\n"
            )
            records.append({
                "timestamp": ts,
                "source": article.get('source', {}).get('name', 'Unknown'),
                "title": title,
                "url": url,
                "summary": summary,
                "tags": tags
            })
            seen_ids.add(url)

        if not records:
            print("⚠️ No new articles to save.")
            return

        os.makedirs("digests", exist_ok=True)
        with open(f"digests/{ts}.md", "w", encoding="utf-8") as f:
            f.writelines(md_lines)

        with open(f"data/{ts}.json", "w", encoding="utf-8") as f:
            json.dump(records, f, indent=2, ensure_ascii=False)

        with open(seen_path, "w", encoding="utf-8") as f:
            json.dump(list(seen_ids), f)

if __name__ == "__main__":
    DigestGenerator().run()