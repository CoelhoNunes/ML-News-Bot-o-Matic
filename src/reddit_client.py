import os
import praw

class RedditClient:
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id=os.environ["REDDIT_CLIENT_ID"],
            client_secret=os.environ["REDDIT_CLIENT_SECRET"],
            user_agent=os.environ.get("REDDIT_USER_AGENT", "ml-reddit-digest-bot")
        )

    def fetch_top_posts(self, subreddit: str, limit: int = 5):
        return self.reddit.subreddit(subreddit).hot(limit=limit)
