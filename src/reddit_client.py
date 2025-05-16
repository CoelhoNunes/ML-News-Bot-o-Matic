# src/reddit_client.py

import os
import time
import requests
from urllib.parse import quote_plus

class RedditClient:
    def __init__(self):
        # User-Agent for Reddit comment fetches (still needed)
        ua = os.environ.get(
            "REDDIT_USER_AGENT",
            "script:ml-reddit-digest-bot:1.0 (by /u/your_reddit_username)"
        )
        self.headers = {"User-Agent": ua}

    def fetch_ml_posts(self, query: str = "machine learning", limit: int = 25):
        """
        Primary: try Pushshift.io; fallback to Reddit search if needed.
        Yields dicts with keys: id, title, subreddit.
        """
        # 1) Try Pushshift
        ps_url = f"https://api.pushshift.io/reddit/search/submission/?q={quote_plus(query)}&size={limit}"
        try:
            resp = requests.get(ps_url, timeout=10)
            resp.raise_for_status()
            data = resp.json().get("data", [])
            if data:
                for item in data:
                    yield {
                        "id":        item.get("id"),
                        "title":     item.get("title"),
                        "subreddit": item.get("subreddit")
                    }
                return
        except requests.RequestException:
            # If Pushshift fails, fall back to Reddit’s search
            pass

        # 2) Fallback: Reddit’s own search (with retries)
        url = f"https://www.reddit.com/search.json?q={quote_plus(query)}&limit={limit}"
        for attempt in range(1, 4):
            try:
                r = requests.get(url, headers=self.headers, timeout=10)
                r.raise_for_status()
                children = r.json().get("data", {}).get("children", [])
                for child in children:
                    d = child["data"]
                    yield {
                        "id":        d["id"],
                        "title":     d["title"],
                        "subreddit": d["subreddit"]
                    }
                return
            except requests.HTTPError as e:
                if r is not None and r.status_code == 503:
                    print(f"[attempt {attempt}] Reddit 503, retrying…")
                    time.sleep(2)
                else:
                    print(f"Reddit search error ({getattr(r,'status_code',None)}): {e}")
                    return
            except requests.RequestException as e:
                print(f"[attempt {attempt}] network error: {e}, retrying…")
                time.sleep(2)
        print("Reddit fallback failed after 3 retries.")
        return

    def fetch_top_comments(self, post_id: str, limit: int = 3):
        """
        Fetch top-level comments via Reddit.  If Reddit is down, returns [].
        """
        url = f"https://www.reddit.com/comments/{post_id}.json?limit={limit}"
        try:
            resp = requests.get(url, headers=self.headers, timeout=10)
            resp.raise_for_status()
            children = resp.json()[1]["data"]["children"]
            return [c["data"]["body"] for c in children if c["kind"] == "t1"][:limit]
        except:
            return []
