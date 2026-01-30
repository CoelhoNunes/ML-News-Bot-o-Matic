# api.py
from fastapi import FastAPI, Query
import glob, json, os
from typing import List, Optional

app = FastAPI(title="ML Digest API")

def load_all_records():
    # Ensure the path is correct and files exist
    data_dir = "data"
    if not os.path.exists(data_dir):
        return []

    records = []
    for path in sorted(glob.glob(os.path.join(data_dir, "*.json")), reverse=True):
        try:
            with open(path, "r", encoding="utf-8") as f:
                for rec in json.load(f):
                    records.append(rec)
        except Exception as e:
            print(f"⚠️ Failed to read {path}: {e}")
    return records

@app.get("/api/digests")
def get_digests(
    date:      Optional[str] = None,
    tag:       Optional[str] = None,
    limit:     int            = Query(10, ge=1),
    offset:    int            = Query(0, ge=0),
):
    records = load_all_records()
    if date:
        records = [r for r in records if r.get("timestamp", "").startswith(date)]
    if tag:
        records = [r for r in records if tag.lower() in (t.lower() for t in r.get("tags", []))]
    return {"total": len(records), "items": records[offset : offset + limit]}

@app.get("/api/latest")
def get_latest():
    records = load_all_records()
    return records[:1] if records else []

@app.get("/api/tags")
def get_all_tags():
    tags = set()
    for record in load_all_records():
        for tag in record.get("tags", []):
            tags.add(tag.lower())
    return sorted(tags)

@app.get("/api/health")
def health_check():
    files = sorted(glob.glob("data/*.json"), reverse=True)
    return {
        "status": "ok",
        "file_count": len(files),
        "latest_file": os.path.basename(files[0]) if files else None
    }
