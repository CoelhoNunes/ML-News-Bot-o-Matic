import os
import json
import time
from datetime import datetime
from dotenv import load_dotenv
import requests
import random
from summarizer import Summarizer

load_dotenv()

SERPAPI_KEY = os.getenv("SERPAPI_KEY")

BASE_QUERY = (
    "machine learning OR artificial intelligence OR AI OR deep learning OR neural networks OR transformers OR LLM OR "
    "large language model OR generative AI OR GPT OR BERT OR NLP OR natural language processing OR computer vision OR "
    "image recognition OR video understanding OR video captioning OR video classification OR speech recognition OR "
    "audio processing OR reinforcement learning OR RLHF OR supervised learning OR unsupervised learning OR self-supervised learning OR "
    "few-shot learning OR zero-shot learning OR transfer learning OR meta-learning OR continual learning OR online learning OR "
    "quantum AI OR quantum machine learning OR quantum computing OR tensor networks OR data structures OR algorithms OR "
    "DSA OR algorithm optimization OR sorting algorithms OR graph neural networks OR GNNs OR diffusion models OR stable diffusion OR "
    "model compression OR model quantization OR distillation OR pruning OR federated learning OR edge AI OR tinyML OR "
    "explainable AI OR XAI OR interpretable models OR AI safety OR alignment OR prompt engineering OR fine-tuning OR "
    "pretraining OR multimodal AI OR vision-language models OR autonomous agents OR autoGPT OR open-source AI OR "
    "open source models OR MLops OR AIops OR LangChain OR agentic workflows OR synthetic data OR adversarial examples OR "
    "novel architecture OR SOTA models OR training tricks OR scalability OR distributed training"
)


class DigestGenerator:
    def __init__(self):
        self.summarizer = Summarizer()
        self.timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M")
        self.seen_path = "data/seen_ids.json"
        self.records = []
        self.seen_ids = self.load_seen_ids()

    def load_seen_ids(self):
        try:
            with open(self.seen_path, "r", encoding="utf-8") as f:
                return set(json.load(f))
        except Exception:
            return set()

    def save_seen_ids(self):
        with open(self.seen_path, "w", encoding="utf-8") as f:
            json.dump(list(self.seen_ids), f, indent=2)

    def tag(self, summary: str):
        if not summary.strip():
            return ["untagged"]
        txt = summary.lower()
        tags = []
        if any(k in txt for k in ("paper", "research")):
            tags.append("research")
        if "job" in txt:
            tags.append("job advice")
        if any(k in txt for k in ("release", "update", "breaking")):
            tags.append("news")
        if any(k in txt for k in ("library", "tutorial")):
            tags.append("tools")
        return tags or ["other"]

    def query_serpapi(self, query, tbs=None):
        base_url = f"https://serpapi.com/search.json?engine=google_news&q={query}&hl=en&gl=us&api_key={SERPAPI_KEY}"
        if tbs:
            base_url += f"&tbs={tbs}"
        try:
            r = requests.get(base_url, timeout=10)
            r.raise_for_status()
            return r.json().get("news_results", [])
        except Exception as e:
            print(f"❌ Request failed: {e}")
            return []

    def get_unique_articles(self):
        tries = 0
        alternate_tbs = [None, "qdr:d", "qdr:w", "qdr:m"]
        queries = [BASE_QUERY, BASE_QUERY + " AND AI", BASE_QUERY + " AND ML"]

        while tries < 5:
            for query in queries:
                for tbs in alternate_tbs:
                    print(f"🔍 Trying query: {query[:50]}... | tbs={tbs}")
                    articles = self.query_serpapi(query, tbs)
                    for article in articles:
                        url = article.get("link")
                        title = article.get("title", "")
                        if not url or not title or url in self.seen_ids:
                            continue

                        snippet = article.get("snippet", "") or title
                        try:
                            summary = self.summarizer.summarize(snippet)
                        except Exception:
                            summary = snippet

                        tags = self.tag(summary)
                        self.records.append({
                            "timestamp": self.timestamp,
                            "source": article.get('source', {}).get('name', 'Unknown'),
                            "title": title,
                            "url": url,
                            "summary": summary,
                            "tags": tags
                        })
                        self.seen_ids.add(url)

                        if len(self.records) >= 5:
                            return

            tries += 1
            print("♻️ Retrying in 5 seconds for more results...")
            time.sleep(5)

    def get_huggingface_models(self, limit=5):
        print("🤖 Fetching Hugging Face trending models...")
        try:
            r = requests.get("https://huggingface.co/api/models?sort=likes", timeout=10)
            r.raise_for_status()
            models = r.json()[:limit]
        except Exception as e:
            print(f"❌ Failed to fetch Hugging Face models: {e}")
            return

        for model in models:
            model_id = model.get("id")
            model_url = f"https://huggingface.co/{model_id}"
            if model_url in self.seen_ids:
                continue

            pipeline_tag = model.get("pipeline_tag", "N/A")
            downloads = model.get("downloads", "Unknown")
            last_modified = model.get("lastModified", "Unknown")

            summary = (
                f"🔥 Pipeline: {pipeline_tag}\n"
                f"⬇️ Downloads: {downloads}\n"
                f"🕒 Last updated: {last_modified}"
            )

            self.records.append({
                "timestamp": self.timestamp,
                "source": "Hugging Face",
                "title": model_id,
                "url": model_url,
                "summary": summary,
                "tags": ["huggingface", "model", pipeline_tag]
            })
            self.seen_ids.add(model_url)

        print(f"✅ Added {len(models)} Hugging Face models to the digest.")

    def fallback_with_old_data(self, count=5):
        print("🔁 No new data. Re-using old unseen records.")
        all_data_files = [
            os.path.join("data", f) for f in os.listdir("data")
            if f.endswith(".json") and not f.startswith("dummy")
        ]
        past_items = []
        for file_path in all_data_files:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    items = json.load(f)
                    for item in items:
                        if not isinstance(item, dict):
                            continue  # skip malformed entries
                        if "url" not in item or item["url"] in self.seen_ids:
                            continue
                        past_items.append(item)
            except Exception as e:
                print(f"⚠️ Failed to read or parse {file_path}: {e}")

        if not past_items:
            print("⚠️ No past data available to re-use.")
            return

        sampled = random.sample(past_items, min(count, len(past_items)))
        for item in sampled:
            item["timestamp"] = self.timestamp
            self.records.append(item)
            self.seen_ids.add(item["url"])

        print(f"✅ Fallback reused {len(sampled)} past items.")

    def save_digest(self):
        os.makedirs("digests", exist_ok=True)
        os.makedirs("data", exist_ok=True)

        if not self.records:
            self.fallback_with_old_data()

        if not self.records:
            print("❌ Still no records after fallback. Exiting.")
            return

        md_path = f"digests/{self.timestamp}.md"
        with open(md_path, "w", encoding="utf-8") as f:
            for item in self.records:
                f.write(
                    f"## [{item['source']}] {item['title']}\n\n"
                    f"{item['summary']}\n\n"
                    f"[Read more]({item['url']})\n\n"
                    f"_Tags: {', '.join(item['tags'])}_\n\n---\n"
                )

        with open(f"data/{self.timestamp}.json", "w", encoding="utf-8") as f:
            json.dump(self.records, f, indent=2, ensure_ascii=False)

        self.save_seen_ids()
        print(f"✅ Saved {len(self.records)} item(s).")

    def run(self):
        self.get_unique_articles()
        self.get_huggingface_models(limit=5)
        self.save_digest()

if __name__ == "__main__":
    DigestGenerator().run()