from transformers import pipeline

class Summarizer:
    def __init__(self):
        self.summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

    def summarize(self, text: str, max_length: int = 100, min_length: int = 30) -> str:
        result = self.summarizer(text, max_length=max_length, min_length=min_length)
        return result[0]["summary_text"].strip()
