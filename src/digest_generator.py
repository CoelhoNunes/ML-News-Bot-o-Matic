# src/digest_generator.py

import os
import json
from datetime import datetime
from dotenv import load_dotenv

from reddit_client import RedditClient
from summarizer   import Summarizer

# 1) load .env (for local/testing; CI injects via workflow env)
load_dotenv()

# 2) sane defaults
DEFAULT_QUERY = (
    "AI OR artificial intelligence OR machine learning OR deep learning OR reinforcement learning "
    "OR neural network OR NLP OR computer vision OR robotics OR data science OR quantum computing "
    "OR tutorial OR research OR jobs OR career OR interview OR challenge OR problem"
)
DEFAULT_TOP_COMMENTS = 5
DEFAULT_SEARCH_LIMIT  = 100

def getenv_or(name: str, default: str) -> str:
    v = os.environ.get(name, "").strip()
    return v if v else default

def getenv_int(name: str, default: int) -> int:
    v = os.environ.get(name, "").strip()
    return int(v) if v else default

class DigestGenerator:
    def __init__(self):
        self.reddit       = RedditClient()
        self.summarizer   = Summarizer()
        self.top_comments = getenv_int("TOP_COMMENTS", DEFAULT_TOP_COMMENTS)
        self.search_limit = getenv_int("SEARCH_LIMIT", DEFAULT_SEARCH_LIMIT)

    def tag(self, summary: str):
        tags = []
        txt = summary.lower()
        if any(k in txt for k in ("paper", "research")):    tags.append("research")
        if "job" in txt:                                    tags.append("job advice")
        if any(k in txt for k in ("release", "update")):    tags.append("news")
        if any(k in txt for k in ("library", "tutorial")):  tags.append("tools")
        return tags or ["other"]

    def run(self):
        query = getenv_or("SEARCH_QUERY", DEFAULT_QUERY)
        limit = self.search_limit
        ts    = datetime.utcnow().strftime("%Y-%m-%d_%H-%M")

        # ensure data dir + load seen IDs
        os.makedirs("data", exist_ok=True)
        seen_path = "data/seen_ids.json"
        try:
            with open(seen_path, "r", encoding="utf-8") as f:
                seen_ids = set(json.load(f))
        except (FileNotFoundError, json.JSONDecodeError):
            seen_ids = set()

        md_lines, records = [], []

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

        # write digest + JSON
        os.makedirs("digests", exist_ok=True)
        with open(f"digests/{ts}.md", "w", encoding="utf-8") as f:
            f.writelines(md_lines)
        with open(f"data/{ts}.json", "w", encoding="utf-8") as f:
            json.dump(records, f, indent=2, ensure_ascii=False)

        # persist seen IDs
        with open(seen_path, "w", encoding="utf-8") as f:
            json.dump(list(seen_ids), f)

if __name__ == "__main__":
    DigestGenerator().run()