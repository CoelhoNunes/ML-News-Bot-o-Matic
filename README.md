# 🤖 ML-News-Bot-o-Matic 9000

Hey, I’m the **ML-News-Bot-o-Matic 9000** (but you can call me **Newsie**).  
I scour Google News *and Hugging Face* every few hours for the freshest machine learning headlines, trending models, and insights. I summarize everything with AI, tag it for easy reference, and log it neatly in Markdown and JSON.

---

## 🛠️ Tech Stack & Languages

- **Languages**: Python 3.10, YAML (GitHub Actions), Markdown, JSON  
- **Data Formats**: `.md` (digest for humans), `.json` (for machines)  
- **Automation**: GitHub Actions (runs every 8 hours)  
- **Summarization Model**: DistilBART (`sshleifer/distilbart-cnn-12-6`)  
- **Data Sources**:  
  - 📰 Google News via [SerpAPI](https://serpapi.com/)  
  - 🤗 Hugging Face Trending Models via [HuggingFace API](https://huggingface.co/docs/api-inference/index)

---

## 📦 Python Packages Used

| Package         | Purpose                                                  |
|-----------------|----------------------------------------------------------|
| `requests`      | Query Google News & Hugging Face APIs                   |
| `transformers`  | Hugging Face pipeline for summarization (DistilBART)    |
| `torch`         | Backend for model acceleration (CPU/GPU)                |
| `python-dotenv` | Load API keys from `.env` file                          |
| `logging`       | Keep the console clean and readable                     |

---

## ⚙️ What I Do

1. **Search Google News** for ML-related topics  
2. **Fetch trending models** from Hugging Face  
3. **Summarize articles and model metadata** using DistilBART  
4. **Tag** each entry (e.g. `research`, `job advice`, `tools`, `model`)  
5. **Save summaries** to:
   - `digests/YYYY-MM-DD_HH-mm.md` (human-readable format)
   - `data/YYYY-MM-DD_HH-mm.json` (machine-parseable format)
6. 🔁 **Auto-run every 8 hours** via GitHub Actions  
7. 📤 **Commit new data to GitHub** to show daily progress

---

## 🔌 Setup & Installation

```bash
git clone https://github.com/CoelhoNunes/ML-Reddit-Digest-Bot.git
cd ML-Reddit-Digest-Bot

python3 -m venv venv
source venv/bin/activate       # macOS/Linux
.\venv\Scripts\activate        # Windows