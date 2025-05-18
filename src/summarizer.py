# src/summarizer.py

import logging
from transformers import pipeline, AutoTokenizer
import torch

logging.getLogger("transformers").setLevel(logging.ERROR)

class Summarizer:
    def __init__(self):
        model_name = "sshleifer/distilbart-cnn-12-6"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        device = 0 if torch.cuda.is_available() else -1
        self.summarizer = pipeline(
            "summarization",
            model=model_name,
            tokenizer=self.tokenizer,
            device=device
        )

    def summarize(self, text: str, min_ratio: float = 0.3) -> str:
        if not text.strip():
            print("⚠️ Empty input received for summarization.")
            return ""

        try:
            print("🔍 Summarizing:", text[:120].replace("\n", " "), "...")

            # Encode and get actual length, respecting model's max limit
            tokens = self.tokenizer.encode(text, truncation=True, max_length=self.tokenizer.model_max_length)
            token_len = min(len(tokens), self.tokenizer.model_max_length)
            min_len = max(5, int(token_len * min_ratio))  # ensure a minimum of 5 tokens

            # Generate summary
            result = self.summarizer(
                text,
                max_length=token_len,
                min_length=min_len,
                truncation=True
            )

            summary = result[0]["summary_text"].strip()
            print("✅ Summary:", summary[:120].replace("\n", " "), "...")
            return summary or text.strip()

        except Exception as e:
            print(f"❌ Summarization error: {e}")
            return text.strip()