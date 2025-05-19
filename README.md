# 🤖 ML-News-Bot-o-Matic

Hey, I’m the **ML-News-Bot-o-Matic 9000** — but you can call me **Newsie**.

Every 8 hours, I scour Google News and Hugging Face for the **freshest machine learning stories**, **new model releases**, and **industry updates**. I summarize them using AI, tag each one by topic, and log them in both Markdown and JSON.

---

## 🛠️ Tech Stack & Languages

| Type            | Details                                   |
|-----------------|-------------------------------------------|
| Languages       | Python 3.10, YAML (GitHub Actions)        |
| Data Formats    | `.md` (digest for humans), `.json` (for machines) |
| Automation      | GitHub Actions (runs every 8 hours)       |
| Summarization   | [DistilBART](https://huggingface.co/sshleifer/distilbart-cnn-12-6) from Hugging Face |

---

## 🔍 Data Sources

- 📰 **Google News** via [SerpAPI](https://serpapi.com/)
- 🤗 **Hugging Face** trending models via [Hugging Face API](https://huggingface.co/docs/api)

---

## 📦 Python Packages

| Package         | Purpose                                |
|-----------------|----------------------------------------|
| `requests`      | Query Google News & Hugging Face APIs |
| `transformers`  | Summarization using DistilBART        |
| `torch`         | Backend for Hugging Face models       |
| `python-dotenv` | Load environment variables             |
| `logging`       | (Optional) Log cleaner CLI output      |

---

## ⚙️ What I Do (Workflow)

1. Search Google News using broad ML/AI queries (updated to include DSA, quantum, etc.)
2. Fetch trending Hugging Face models
3. Summarize articles and models using DistilBART
4. Tag each entry by topic:
   - `research`, `tools`, `model`, `job advice`, etc.
5. Save results to:
   - `digests/YYYY-MM-DD_HH-mm.md` (Markdown for humans)
   - `data/YYYY-MM-DD_HH-mm.json` (JSON for machines)
6. Fallback to old unseen records if no new data is found
7. ✅ Commit the results to GitHub to show contribution activity

---

## 🔁 Automation

This project runs automatically every 8 hours via GitHub Actions.  
Even if there’s no new data, it reuses unseen entries and updates the log.

---

## 📤 GitHub Contributions

Every successful pull:
- Updates digest files
- Commits results to `master`
- Shows green dots on your GitHub graph (daily activity ✅)

---

## 🔌 Setup & Installation (Local Dev)

```bash
git clone https://github.com/CoelhoNunes/ML-Reddit-Digest-Bot.git
cd ML-Reddit-Digest-Bot

python3 -m venv venv
source venv/bin/activate       # macOS/Linux
.\venv\Scripts\activate        # Windows
