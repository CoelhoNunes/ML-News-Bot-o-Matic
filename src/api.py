# api.py
from fastapi import FastAPI, Query
import glob, json
from typing import List, Optional

app = FastAPI(title="ML Digest API")

def load_all_records():
    # grab JSON files most‐recent first
    for path in sorted(glob.glob("data/*.json"), reverse=True):
        with open(path, "r", encoding="utf-8") as f:
            for rec in json.load(f):
                yield rec

@app.get("/api/digests")
def get_digests(
    date:      Optional[str] = None,
    tag:       Optional[str] = None,
    limit:     int            = Query(10, ge=1),
    offset:    int            = Query(0, ge=0),
):
    records = list(load_all_records())
    if date:
        records = [r for r in records if r.get("timestamp", "").startswith(date)]
    if tag:
        records = [r for r in records if tag.lower() in (t.lower() for t in r.get("tags", []))]
    return {"total": len(records), "items": records[offset : offset + limit]}

@app.get("/api/latest")
def get_latest():
    records = list(load_all_records())
    return records[:1] if records else []

@app.get("/api/tags")
def get_all_tags():
    tags = set()
    for record in load_all_records():
        for tag in record.get("tags", []):
            tags.add(tag.lower())
    return sorted(tags)
