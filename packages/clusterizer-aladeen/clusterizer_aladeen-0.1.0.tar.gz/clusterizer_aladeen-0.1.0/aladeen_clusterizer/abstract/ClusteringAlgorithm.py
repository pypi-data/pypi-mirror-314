from abc import ABC, abstractmethod
import numpy as np


class ClusteringAlgorithm(ABC):
    @abstractmethod
    def cluster(self, embeddings: np.ndarray) -> list[int]:
        pass
