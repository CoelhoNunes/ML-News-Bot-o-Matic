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
            (
                "AI OR artificial intelligence OR machine learning OR deep learning OR reinforcement learning OR supervised learning "
                "OR unsupervised learning OR semi-supervised OR self-supervised OR few-shot learning OR zero-shot learning OR transfer learning "
                "OR meta-learning OR neural network OR CNN OR RNN OR LSTM OR GRU OR transformer OR attention OR GPT OR BERT OR diffusion model "
                "OR GAN OR VAE OR autoencoder OR clustering OR K-means OR DBSCAN OR classification OR regression OR decision tree OR random forest "
                "OR gradient boosting OR XGBoost OR LightGBM OR CatBoost OR SVM OR KNN OR anomaly detection OR time series OR forecasting OR optimization "
                "OR genetic algorithm OR evolutionary algorithm OR fuzzy logic OR Bayesian OR probabilistic OR graph neural network OR GNN "
                "OR federated learning OR MLOps OR model deployment OR Docker OR Kubernetes OR edge AI OR TinyML OR IoT OR robotics OR computer vision "
                "OR NLP OR speech recognition OR audio processing OR recommender OR collaborative filtering OR explainable AI OR interpretability OR fairness "
                "OR bias OR ethics OR synthetic data OR data augmentation OR feature engineering OR data pipeline OR quantum computing OR quantum ML "
                "OR neuromorphic computing OR hardware acceleration OR GPU OR TPU OR FPGA OR HPC OR jobs OR career OR interview OR tutorial OR research "
                "OR challenge OR problem"
            )
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