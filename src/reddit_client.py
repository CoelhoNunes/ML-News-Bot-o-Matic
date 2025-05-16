# src/reddit_client.py

import os
import requests
from urllib.parse import quote_plus

class RedditClient:
    def __init__(self):
        # only a custom User-Agent is needed for read-only public endpoints
        ua = os.environ.get("REDDIT_USER_AGENT", "ml-reddit-digest-bot")
        self.headers = {"User-Agent": ua}

    def fetch_ml_posts(self, query: str = "machine learning", limit: int = 25):
        """
        Search Reddit across all subreddits for 'query'.
        Yields dicts with keys: id, title, subreddit.
        """
        q = quote_plus(query)
        url = f"https://www.reddit.com/search.json?q={q}&limit={limit}"
        resp = requests.get(url, headers=self.headers)
        resp.raise_for_status()
        for child in resp.json()["data"]["children"]:
            d = child["data"]
            yield {
                "id":        d["id"],
                "title":     d["title"],
                "subreddit": d["subreddit"]
            }

    def fetch_top_comments(self, post_id: str, limit: int = 3):
        """
        Fetches the top-level comments for a post by ID.
        """
        url = f"https://www.reddit.com/comments/{post_id}.json?limit={limit}"
        resp = requests.get(url, headers=self.headers)
        resp.raise_for_status()
        comments = []
        for child in resp.json()[1]["data"]["children"]:
            if child["kind"] == "t1":
                comments.append(child["data"]["body"])
        return comments[:limit]
