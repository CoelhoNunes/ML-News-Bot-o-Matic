# src/digest_generator.py

import os
import json
from datetime import datetime
from dotenv import load_dotenv

from reddit_client import RedditClient
from summarizer import Summarizer

# Load environment variables from .env
load_dotenv()

class DigestGenerator:
    def __init__(self, top_comments=3, search_limit=25):
        self.reddit = RedditClient()
        self.summarizer = Summarizer()
        self.top_comments = top_comments
        self.search_limit = search_limit

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
        # Load search parameters from environment (with defaults)
        query = os.environ.get(
            "SEARCH_QUERY",
            "machine learning OR jobs OR career advice OR problems OR algorithms OR tutorials OR research"
        )
        limit = int(os.environ.get("SEARCH_LIMIT", self.search_limit))

        # Prepare timestamp for files
        ts = datetime.utcnow().strftime("%Y-%m-%d_%H-%M")

        # Ensure data directory exists and load seen IDs
        os.makedirs("data", exist_ok=True)
        seen_file = "data/seen_ids.json"
        try:
            with open(seen_file, "r", encoding="utf-8") as f:
                seen_ids = set(json.load(f))
        except (FileNotFoundError, json.JSONDecodeError):
            seen_ids = set()

        md_lines = []
        records = []

        # Fetch posts and process only new ones
        for post in self.reddit.fetch_ml_posts(query, limit=limit):
            post_id = post["id"]
            if post_id in seen_ids:
                continue

            comments = self.reddit.fetch_top_comments(post_id, limit=self.top_comments)
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
                "post_id":   post_id,
                "title":     post["title"],
                "comments":  comments,
                "summary":   summary,
                "tags":      tags
            })

            seen_ids.add(post_id)

        # Write out markdown and JSON digest
        os.makedirs("digests", exist_ok=True)
        with open(f"digests/{ts}.md", "w", encoding="utf-8") as f_md:
            f_md.writelines(md_lines)
        with open(f"data/{ts}.json", "w", encoding="utf-8") as f_json:
            json.dump(records, f_json, indent=2, ensure_ascii=False)

        # Update seen IDs file
        with open(seen_file, "w", encoding="utf-8") as f_seen:
            json.dump(list(seen_ids), f_seen)

if __name__ == "__main__":
    DigestGenerator(
        top_comments=int(os.environ.get("TOP_COMMENTS", 3)),
        search_limit=int(os.environ.get("SEARCH_LIMIT", 25))
    ).run()