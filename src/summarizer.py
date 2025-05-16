# src/summarizer.py

from transformers import pipeline, AutoTokenizer
import torch

class Summarizer:
    def __init__(self):
        # load tokenizer + model pipeline
        model_name = "sshleifer/distilbart-cnn-12-6"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.summarizer = pipeline(
            "summarization",
            model=model_name,
            tokenizer=self.tokenizer,
            device=torch.device("cpu").index if torch.cuda.is_available() else -1
        )

    def summarize(self, text: str, max_length: int = 100, min_length: int = 30) -> str:
        # Tokenize and truncate to the first 1024 tokens
        tokens = self.tokenizer.encode(text, truncation=True, max_length=self.tokenizer.model_max_length)
        truncated_text = self.tokenizer.decode(tokens, skip_special_tokens=True)

        # Summarize the (now-safe) text
        result = self.summarizer(
            truncated_text,
            max_length=max_length,
            min_length=min_length,
            truncation=True  # ensure no overflow in generation
        )
        return result[0]["summary_text"].strip()
