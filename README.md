# 🤖 ML-Reddi-Digest-O-Matic 9000

Hey, I’m the **ML-Reddi-Digest-O-Matic 9000** (but you can call me **Reddio**).  
I roam the web every few hours searching for the latest and greatest in **machine learning**, **AI**, and everything in between.  
Then I summarize it, tag it, and drop it off here for your research or reading pleasure.

---

## 🛠️ Tech Stack & Languages

- **Languages**: Python 3.10, YAML (GitHub Actions), Markdown, JSON
- **Data Formats**: `.md` (digest for humans), `.json` (for machines)
- **Automation**: GitHub Actions (runs every ~7.5 hours)
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
