# 🤖 ML-News-Bot-o-Matic 9000

Hey, I’m the **ML-News-Bot-o-Matic 9000** (but you can call me **Newsie**).  
I scour Google News every few hours for the freshest machine learning headlines, summarize them with AI, tag them for your convenience, and log it all neatly in Markdown and JSON.

---

## 🛠️ Tech Stack & Languages

- **Languages**: Python 3.10, YAML (GitHub Actions), Markdown, JSON
- **Data Formats**: `.md` (digest for humans), `.json` (for machines)
- **Automation**: GitHub Actions (runs every 8 hours)
- **Summarization Model**: DistilBART (`sshleifer/distilbart-cnn-12-6`)
- **News Source**: Google News via [SerpAPI](https://serpapi.com/)

---

## 📦 Python Packages Used

| Package         | Purpose                                     |
|-----------------|---------------------------------------------|
| `requests`      | Querying Google News via SerpAPI            |
| `transformers`  | HuggingFace pipeline for summarization      |
| `torch`         | Backend for model acceleration (CPU/GPU)    |
| `python-dotenv` | Load API keys from `.env`                   |
| `logging`       | Keep the console calm and clean             |

---

## ⚙️ What I Do

1. **Search Google News** for ML-related topics  
2. **Summarize headlines** with DistilBART  
3. **Tag** them as research, news, tools, job advice, or other  
4. **Save summaries** as:
   - `digests/YYYY-MM-DD_HH-mm.md` (for humans)
   - `data/YYYY-MM-DD_HH-mm.json` (for machines)
5. 🔁 **Auto-run every 8 hours** via GitHub Actions

---

## 🔌 Setup & Installation

```bash
git clone https://github.com/CoelhoNunes/ML-Reddit-Digest-Bot.git
cd ML-Reddit-Digest-Bot

python3 -m venv venv
source venv/bin/activate       # macOS/Linux
.\venv\Scripts\activate        # Windows