from abc import ABC, abstractmethod


class DataPreprocessor(ABC):
    @abstractmethod
    def preprocess(self, data: list[str]) -> list[str]:
        pass
