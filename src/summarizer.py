# src/summarizer.py

import logging
from transformers import pipeline, AutoTokenizer
import torch

# Silence the “consider decreasing max_length” warnings
logging.getLogger("transformers.tokenization_utils_base").setLevel(logging.ERROR)

class Summarizer:
    def __init__(self):
        model_name = "sshleifer/distilbart-cnn-12-6"
        # Load tokenizer & model pipeline
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.summarizer = pipeline(
            "summarization",
            model=model_name,
            tokenizer=self.tokenizer,
            device=torch.device("cpu").index if torch.cuda.is_available() else -1
        )

    def summarize(self, text: str, min_ratio: float = 0.3) -> str:
        """
        Summarize `text`, allowing the summary length to scale with input length.
        `min_ratio` is the minimum fraction of input tokens (e.g. 0.3 → 30%).
        """
        # 1) Tokenize and truncate input to model’s max
        tokens = self.tokenizer.encode(
            text,
            truncation=True,
            max_length=self.tokenizer.model_max_length
        )
        input_len = len(tokens)

        # 2) Let the summary be as long as the input
        max_len = input_len

        # 3) Set a minimum summary length
        min_len = max(1, int(max_len * min_ratio))

        # 4) Run the summarization
        result = self.summarizer(
            text,
            max_length=max_len,
            min_length=min_len,
            truncation=True
        )
        return result[0]["summary_text"].strip()