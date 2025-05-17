# src/digest_generator.py

import os
import json
from datetime import datetime

from reddit_client import RedditClient
from summarizer import Summarizer

import os
from dotenv import load_dotenv

# pull in your .env into os.environ
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
        if any(k in txt for k in ("paper", "research")):    tags.append("research")
        if "job" in txt:                                    tags.append("job advice")
        if any(k in txt for k in ("release", "update")):    tags.append("news")
        if any(k in txt for k in ("library", "tutorial")):  tags.append("tools")
        return tags or ["other"]

    def run(self):
        # load search query & limits from env (or use defaults)
        query = os.environ.get(
            "SEARCH_QUERY",
            "machine learning OR jobs OR career advice OR problems OR algorithms OR tutorials OR research"
        )
        limit = int(os.environ.get("SEARCH_LIMIT", self.search_limit))

        ts = datetime.utcnow().strftime("%Y-%m-%d_%H-%M")
        md_lines = []
        records = []

        for post in self.reddit.fetch_ml_posts(query, limit=limit):
            comments = self.reddit.fetch_top_comments(post["id"], limit=self.top_comments)
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
                "post_id":   post["id"],
                "title":     post["title"],
                "comments":  comments,
                "summary":   summary,
                "tags":      tags
            })

        os.makedirs("digests", exist_ok=True)
        os.makedirs("data", exist_ok=True)
        with open(f"digests/{ts}.md", "w", encoding="utf-8") as f_md:
            f_md.writelines(md_lines)
        with open(f"data/{ts}.json", "w", encoding="utf-8") as f_json:
            json.dump(records, f_json, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    DigestGenerator(
        top_comments=int(os.environ.get("TOP_COMMENTS", 3)),
        search_limit=int(os.environ.get("SEARCH_LIMIT", 25))
    ).run()
