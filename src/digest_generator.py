import os, json
from datetime import datetime
from reddit_client import RedditClient
from summarizer import Summarizer

class DigestGenerator:
    def __init__(self, subreddits, top_comments=3):
        self.reddit = RedditClient()
        self.summarizer = Summarizer()
        self.subreddits = subreddits
        self.top_comments = top_comments

    def tag(self, summary: str):
        tags = []
        txt = summary.lower()
        if "paper" in txt or "research" in txt: tags.append("research")
        if "job" in txt:   tags.append("job advice")
        if "release" in txt or "update" in txt: tags.append("news")
        if "library" in txt or "tutorial" in txt: tags.append("tools")
        return tags or ["other"]

    def run(self):
        ts = datetime.utcnow().strftime("%Y-%m-%d_%H-%M")
        md_lines, records = [], []

        for sub in self.subreddits:
            for post in self.reddit.fetch_top_posts(sub):
                comments = [c.body for c in post.comments[:self.top_comments] if hasattr(c, "body")]
                content = post.title + "\n\n" + "\n\n".join(comments)
                summary = self.summarizer.summarize(content)
                tags = self.tag(summary)

                md_lines.append(f"## {post.title}\n\n{summary}\n\n_Tags: {', '.join(tags)}_\n\n---\n")
                records.append({
                    "timestamp": ts,
                    "subreddit": sub,
                    "post_id":  post.id,
                    "title":    post.title,
                    "comments": comments,
                    "summary":  summary,
                    "tags":     tags
                })

        os.makedirs("digests", exist_ok=True)
        os.makedirs("data", exist_ok=True)

        with open(f"digests/{ts}.md", "w") as f_md:
            f_md.writelines(md_lines)
        with open(f"data/{ts}.json", "w") as f_json:
            json.dump(records, f_json, indent=2)

if __name__ == "__main__":
    subs = ["MachineLearning","learnmachinelearning","MLQuestions","artificial","datascience"]
    DigestGenerator(subs).run()
