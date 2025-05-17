# src/digest_generator.py

import os
import json
from datetime import datetime
from dotenv import load_dotenv

from reddit_client import RedditClient
from summarizer import Summarizer

load_dotenv()

SUBREDDITS = [
    "MachineLearning", "ArtificialIntelligence", "datascience", "technology", "AI_News",
    "DeepLearning", "NeuralNetworks", "ReinforcementLearning", "MLJobs", "MLPapers",
    "MLProjects", "MLTutorials", "DeepDream", "AIArt", "AI_Music", "AI_Video",
    "AI_Design", "AI_Writing", "AI_Coding", "LearnMachineLearning", "LearnAI",
    "AI_Courses", "AI_Books", "AI_Podcasts", "AI_Ethics", "AI_Safety", "AGI",
    "Singularity", "Futurology", "Transhumanism", "AI_Policy", "AI_Law",
    "AI_Philosophy", "TensorFlow", "PyTorch", "Keras", "ScikitLearn", "MLops",
    "AI_Dev", "AI_Engineering", "AI_Hardware", "AI_Cloud", "AI_Startup",
    "AI_Healthcare", "AI_Finance", "Robotics", "Automation", "AutonomousVehicles",
    "NLP", "ComputerVision", "AI_GenerativeModels", "CognitiveScience", "Neuroscience",
    "cnn", "foxnews", "worldnews", "news", "science", "technews"
]

class DigestGenerator:
    def __init__(self):
        self.reddit = RedditClient()
        self.summarizer = Summarizer()
        self.top_comments = int(os.getenv("TOP_COMMENTS") or 5)
        self.search_limit = int(os.getenv("SEARCH_LIMIT") or 100)

    def tag(self, summary: str):
        tags = []
        txt = summary.lower()
        if any(k in txt for k in ("paper", "research")):    tags.append("research")
        if "job" in txt:                                    tags.append("job advice")
        if any(k in txt for k in ("release", "update", "breaking")): tags.append("news")
        if any(k in txt for k in ("library", "tutorial")):  tags.append("tools")
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

        for subreddit in SUBREDDITS:
            posts = self.reddit.fetch_posts_by_subreddit(subreddit, limit=self.search_limit)
            for post in posts:
                pid = post["id"]
                if pid in seen_ids:
                    continue

                comments = self.reddit.fetch_top_comments(pid, limit=self.top_comments)
                content = f"{post['title']}\n\n" + "\n\n".join(comments)
                summary = self.summarizer.summarize(content)
                tags = self.tag(summary)

                md_lines.append(
                    f"## [{post['subreddit']}] {post['title']}\n\n"
                    f"{summary}\n\n"
                    f"_Tags: {', '.join(tags)}_\n\n---\n"
                )
                records.append({
                    "timestamp": ts,
                    "subreddit": post["subreddit"],
                    "post_id": pid,
                    "title": post["title"],
                    "comments": comments,
                    "summary": summary,
                    "tags": tags
                })
                seen_ids.add(pid)

        os.makedirs("digests", exist_ok=True)
        with open(f"digests/{ts}.md", "w", encoding="utf-8") as f:
            f.writelines(md_lines)

        with open(f"data/{ts}.json", "w", encoding="utf-8") as f:
            json.dump(records, f, indent=2, ensure_ascii=False)

        with open(seen_path, "w", encoding="utf-8") as f:
            json.dump(list(seen_ids), f)

if __name__ == "__main__":
    DigestGenerator().run()