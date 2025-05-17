# src/summarizer.py

import logging
from transformers import pipeline, AutoTokenizer
import torch

logging.getLogger("transformers").setLevel(logging.ERROR)

class Summarizer:
    def __init__(self):
        model_name = "sshleifer/distilbart-cnn-12-6"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        # GPU=0 if available, else CPU=-1
        device = 0 if torch.cuda.is_available() else -1
        self.summarizer = pipeline(
            "summarization",
            model=model_name,
            tokenizer=self.tokenizer,
            device=device
        )

    def summarize(self, text: str, min_ratio: float = 0.3) -> str:
        if not text.strip():
            print("⚠️ Skipping empty text.")
            return ""

        try:
            print("🔍 Summarizing:", text[:120].replace("\n", " "), "...")
            tokens   = self.tokenizer.encode(text, truncation=True,
                                             max_length=self.tokenizer.model_max_length)
            max_len  = len(tokens)
            min_len  = max(1, int(max_len * min_ratio))

            result = self.summarizer(text, max_length=max_len,
                                     min_length=min_len, truncation=True)
            summary = result[0]["summary_text"].strip()
            print("✅ Summary:", summary[:120].replace("\n", " "), "...")
            return summary or text  # fallback to original if summary is empty
        except Exception as e:
            print(f"❌ Summarization error: {e}")
            return text.strip()  # fallback to full text