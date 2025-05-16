# ML-Reddi-Digest-O-Matic 9000

Hey, I’m the ML-Reddi-Digest-O-Matic 9000 (but you can call me **Reddio**). I’m built in **Python 3.10** with a touch of **YAML** (for GitHub Actions) and I use several key libraries to:

- Scrape & search Reddit/Pushshift  
- Summarize text offline  
- Serve a simple web API  
- Automate everything in the cloud

---

## 🛠️ Tech Stack & Languages

- **Languages:** Python 3.10, YAML (GitHub Actions), Markdown, JSON  
- **Data Formats:** Markdown (`.md`), JSON (`.json`)  
- **CI/CD:** GitHub Actions  

---

## 📦 Python Packages

- `requests` – HTTP client for Reddit & Pushshift  
- `transformers` – HuggingFace pipelines for summarization  
- `torch` – backend for the summarization model  
- `fastapi` – serve digests via REST API  
- `uvicorn` – ASGI server for FastAPI  
- `python-dotenv` – load environment variables  
- `pydantic` – request/response validation in FastAPI  

---

## What I Do

1. **Search** Reddit for your ML keywords via Pushshift’s API  
2. **Fetch** each post’s top comments from Reddit’s JSON endpoints  
3. **Summarize** everything offline with DistilBART  
4. **Tag** each summary (research, job advice, news, tools, other)  
5. **Save**:
   - `digests/YYYY-MM-DD_HH-mm.md` (human-readable)  
   - `data/YYYY-MM-DD_HH-mm.json` (machine-readable)  
6. **Automate**: run every 4 hours via GitHub Actions  
7. **Serve**: REST endpoint at `/api/digests` for easy data-science ingestion  

---

## 📥 Installation & Setup

```bash
git clone https://github.com/you/ML-Reddit-Digest-Bot.git
cd ML-Reddit-Digest-Bot

python3 -m venv venv
source venv/bin/activate      # macOS/Linux
.\venv\Scripts\Activate       # Windows

pip install -r requirements.txt