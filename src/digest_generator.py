# src/digest_generator.py

import os
import json
from datetime import datetime
from dotenv import load_dotenv

from reddit_client import RedditClient
from summarizer import Summarizer

# ─── 1) load local .env into os.environ ───────────────────────────────────────
load_dotenv()

# ─── 2) defaults ──────────────────────────────────────────────────────────────
DEFAULT_QUERY = (
    "AI OR artificial intelligence OR machine learning OR deep learning OR reinforcement learning "
    "OR supervised learning OR unsupervised learning OR few-shot OR zero-shot OR transfer learning "
    "OR meta-learning OR neural network OR CNN OR RNN OR transformer OR GPT OR BERT OR diffusion OR GAN "
    "OR VAE OR clustering OR classification OR regression OR optimization OR anomaly detection "
    "OR feature engineering OR tutorial OR research OR quantum computing OR quantum ML OR neuromorphic "
    "OR hardware acceleration OR FPGA OR GPU OR TPU OR federated learning OR MLOps OR edge AI OR TinyML "
    "OR IoT OR robotics OR computer vision OR NLP OR speech OR audio OR recommender OR explainability "
    "OR fairness OR ethics OR synthetic data OR data pipeline OR algorithm OR challenge OR problem OR job "
    "OR career OR interview"
)
DEFAULT_TOP_COMMENTS = 5
DEFAULT_SEARCH_LIMIT  = 100

def getenv_or(name: str, default: str) -> str:
    """Return env[name] if non-blank, else default."""
    val = os.environ.get(name, "").strip()
    return val if val else default

def getenv_int(name: str, default: int) -> int:
    """Return int(env[name]) if non-blank, else default."""
    val = os.environ.get(name, "").strip()
    return int(val) if val else default

class DigestGenerator:
    def __init__(self):
        self.reddit      = RedditClient()
        self.summarizer  = Summarizer()
        # read ints (with fallback if blank)
        self.top_comments = getenv_int("TOP_COMMENTS", DEFAULT_TOP_COMMENTS)
        self.search_limit = getenv_int("SEARCH_LIMIT", DEFAULT_SEARCH_LIMIT)

    def tag(self, summary: str):
        tags = []
        txt = summary.lower()
        if any(k in txt for k in ("paper", "research")):
            tags.append("research")
        if "job" in txt:
            tags.append("job advice")
        if any(k in txt for k in ("release", "update")):
            tags.append("news")
        if any(k in txt for k in ("library", "tutorial")):
            tags.append("tools")
        return tags or ["other"]

    def run(self):
        # build query (fallback if blank)
        query = getenv_or("SEARCH_QUERY", DEFAULT_QUERY)
        limit = self.search_limit

        ts = datetime.utcnow().strftime("%Y-%m-%d_%H-%M")

        # prepare seen‐IDs persistence
        os.makedirs("data", exist_ok=True)
        seen_file = "data/seen_ids.json"
        try:
            with open(seen_file, "r", encoding="utf-8") as f:
                seen_ids = set(json.load(f))
        except (FileNotFoundError, json.JSONDecodeError):
            seen_ids = set()

        md_lines = []
        records  = []

        # fetch & process only new posts
        for post in self.reddit.fetch_ml_posts(query, limit=limit):
            pid = post["id"]
            if pid in seen_ids:
                continue

            comments = self.reddit.fetch_top_comments(pid, limit=self.top_comments)
            content  = f"{post['title']}\n\n" + "\n\n".join(comments)
            summary  = self.summarizer.summarize(content)
            tags     = self.tag(summary)

            md_lines.append(
                f"## [{post['subreddit']}] {post['title']}\n\n"
                f"{summary}\n\n"
                f"_Tags: {', '.join(tags)}_\n\n---\n"
            )
            records.append({
                "timestamp": ts,
                "subreddit": post["subreddit"],
                "post_id":   pid,
                "title":     post["title"],
                "comments":  comments,
                "summary":   summary,
                "tags":      tags
            })

            seen_ids.add(pid)

        # write new digest files
        os.makedirs("digests", exist_ok=True)
        with open(f"digests/{ts}.md", "w", encoding="utf-8") as f_md:
            f_md.writelines(md_lines)
        with open(f"data/{ts}.json", "w", encoding="utf-8") as f_json:
            json.dump(records, f_json, indent=2, ensure_ascii=False)

        # persist updated seen‐IDs
        with open(seen_file, "w", encoding="utf-8") as f_seen:
            json.dump(list(seen_ids), f_seen)

if __name__ == "__main__":
    DigestGenerator().run()
