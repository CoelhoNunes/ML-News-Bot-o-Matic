# api.py
from fastapi import FastAPI, Query
import glob, json
from typing import List, Optional

app = FastAPI(title="ML Reddit Digest API")

def load_all_records():
    # grab JSON files most‐recent first
    for path in sorted(glob.glob("data/*.json"), reverse=True):
        with open(path, "r", encoding="utf-8") as f:
            for rec in json.load(f):
                yield rec

@app.get("/api/digests")
def get_digests(
    date:      Optional[str] = None,
    subreddit: Optional[str] = None,
    tag:       Optional[str] = None,
    limit:     int            = Query(10, ge=1),
    offset:    int            = Query(0, ge=0),
):
    records = list(load_all_records())
    if date:
        records = [r for r in records if r["timestamp"].startswith(date)]
    if subreddit:
        records = [r for r in records if r.get("subreddit", "").lower() == subreddit.lower()]
    if tag:
        records = [r for r in records if tag.lower() in (t.lower() for t in r["tags"])]
    return {"total": len(records), "items": records[offset : offset + limit]}
