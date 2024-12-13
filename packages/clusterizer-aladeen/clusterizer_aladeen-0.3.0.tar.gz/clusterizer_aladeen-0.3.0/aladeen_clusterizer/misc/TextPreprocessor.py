import re

from .abstract.DataPreprocessor import DataPreprocessor


class TextPreprocessor(DataPreprocessor):
    def __init__(self, config: dict):
        self.config = config

    def preprocess(self, data: list[str]) -> list[str]:
        preprocessed_data = []
        for doc in data:
            doc = str(doc).lower()
            doc = doc.strip()
            doc = re.sub("</?.*?>", " <> ", doc)
            doc = re.sub(r"[^Ⴀ-ჿⴀ-ⴥᲐ-Ჿ0-9a-zA-Z.;:]", " ", doc)
            doc = re.sub(r"\s+", " ", doc)
            doc = doc.strip()
            preprocessed_data.append(doc)
        return preprocessed_data
