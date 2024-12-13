import numpy as np

from abc import ABC, abstractmethod


class EmbeddingGenerator(ABC):
    @abstractmethod
    def generate_embeddings(self, data: list[str]) -> np.ndarray:
        pass
