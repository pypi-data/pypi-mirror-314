from abc import ABC, abstractmethod
import numpy as np


class ClusterScorer(ABC):
    @abstractmethod
    def calculate_scores(
        self, embeddings: np.ndarray, labels: list[int]
    ) -> dict[int, list[float]]:
        pass
