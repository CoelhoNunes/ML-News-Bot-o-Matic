# src/summarizer.py

import logging
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

logging.getLogger("transformers").setLevel(logging.ERROR)

class Summarizer:
    def __init__(self):
        model_name = "sshleifer/distilbart-cnn-12-6"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)

    def summarize(self, text: str, min_ratio: float = 0.3) -> str:
        if not text.strip():
            print("⚠️ Empty input received for summarization.")
            return ""

        try:
            print("🔍 Summarizing:", text[:120].replace("\n", " "), "...")

            # Tokenize input
            inputs = self.tokenizer(text, max_length=1024, truncation=True, return_tensors="pt")
            inputs = inputs.to(self.device)
            
            # Calculate lengths
            input_length = inputs['input_ids'].shape[1]
            max_length = input_length
            min_length = max(5, int(input_length * min_ratio))

            # Generate summary
            summary_ids = self.model.generate(
                inputs['input_ids'],
                max_length=max_length,
                min_length=min_length,
                num_beams=4,
                early_stopping=True
            )

            # Decode summary
            summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True).strip()
            print("✅ Summary:", summary[:120].replace("\n", " "), "...")
            return summary or text.strip()

        except Exception as e:
            print(f"❌ Summarization error: {e}")
            return text.strip()