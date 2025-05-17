# src/reddit_client.py

import os
import time
import requests
from urllib.parse import quote_plus
from datetime import datetime, timedelta

class RedditClient:
    def __init__(self):
        ua = os.environ.get(
            "REDDIT_USER_AGENT",
            "script:ml-reddit-digest-bot:1.0 (by /u/your_reddit_username)"
        )
        self.headers = {"User-Agent": ua}

    def fetch_ml_posts(self, query: str = "machine learning", limit: int = 25):
        ps_url = (
            "https://api.pushshift.io/reddit/search/submission/"
            f"?q={quote_plus(query)}&size={limit}"
        )
        try:
            r = requests.get(ps_url, timeout=10)
            r.raise_for_status()
            data = r.json().get("data", [])
            if data:
                for item in data:
                    yield {
                        "id":        item.get("id"),
                        "title":     item.get("title"),
                        "subreddit": item.get("subreddit")
                    }
                return
        except requests.RequestException:
            pass

        url = f"https://www.reddit.com/search.json?q={quote_plus(query)}&limit={limit}"
        for attempt in range(1, 4):
            try:
                r = requests.get(url, headers=self.headers, timeout=10)
                r.raise_for_status()
                children = r.json().get("data", {}).get("children", [])
                for c in children:
                    d = c["data"]
                    yield {"id": d["id"], "title": d["title"], "subreddit": d["subreddit"]}
                return
            except Exception:
                time.sleep(2)
        return

    def fetch_top_comments(self, post_id: str, limit: int = 3):
        url = f"https://www.reddit.com/comments/{post_id}.json?limit={limit}"
        try:
            r = requests.get(url, headers=self.headers, timeout=10)
            r.raise_for_status()
            children = r.json()[1]["data"]["children"]
            return [c["data"]["body"] for c in children if c["kind"] == "t1"][:limit]
        except:
            return []

    def fetch_posts_by_subreddit(self, subreddit: str, limit: int = 25, max_days_back: int = 7):
        now = datetime.utcnow()

        for days_back in range(max_days_back):
            end_time = int((now - timedelta(days=days_back)).timestamp())
            start_time = int((now - timedelta(days=days_back + 1)).timestamp())
            url = (
                f"https://api.pushshift.io/reddit/search/submission/?subreddit={subreddit}"
                f"&after={start_time}&before={end_time}&size={limit}&sort=desc"
            )
            try:
                r = requests.get(url, timeout=10)
                r.raise_for_status()
                data = r.json().get("data", [])
                if data:
                    for item in data:
                        yield {
                            "id": item.get("id"),
                            "title": item.get("title"),
                            "subreddit": subreddit
                        }
                    break  # Stop as soon as we find posts for any past day
            except requests.RequestException:
                continue