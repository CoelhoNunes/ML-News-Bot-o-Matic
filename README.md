# ML Reddit Digest Bot

Automated, **free** bot that scrapes ML-related subreddits every 4 hours, summarizes posts offline, tags by topic, and version-controls results.

## Features

- **Fetch** top posts + comments from:
  - r/MachineLearning, r/learnmachinelearning, r/MLQuestions, r/artificial, r/datascience
- **Offline summarization** via HuggingFace `distilbart-cnn-12-6` (no paid APIs)
- **Tagging** by topic (`docs/TAGS.md`)
- **Outputs**:
  - `digests/YYYY-MM-DD_HH-mm.md` (human-readable)
  - `data/YYYY-MM-DD_HH-mm.json` (machine-readable; matches `schema/digest.schema.json`)
- **FastAPI** server on `/api/digests` for filtering/pagination
- **CI/CD**: GitHub Actions cron every 4 hrs to run & commit only new files

## Installation

```bash
git clone https://github.com/you/ML-Reddit-Digest-Bot.git
cd ML-Reddit-Digest-Bot
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

## Configuration

1. In your GitHub repo **Settings → Secrets**, add:
   - `REDDIT_CLIENT_ID`
   - `REDDIT_CLIENT_SECRET`
   - `REDDIT_USER_AGENT`
2. Protect `main` so only GitHub Actions can push.

## Usage

```bash
# Local run:
export REDDIT_CLIENT_ID=…
export REDDIT_CLIENT_SECRET=…
export REDDIT_USER_AGENT=…
python src/digest_generator.py

# Run API:
uvicorn src.api:app --reload
```