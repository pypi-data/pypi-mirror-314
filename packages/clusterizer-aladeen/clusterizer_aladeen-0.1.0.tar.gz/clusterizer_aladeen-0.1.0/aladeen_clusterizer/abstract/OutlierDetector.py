from abc import ABC, abstractmethod
from typing import Optional
import numpy as np


from .ClusterScorer import ClusterScorer


class OutlierDetector(ABC):
    def __init__(self, outlier_scorer: ClusterScorer):
        self.outlier_scorer = outlier_scorer

    @abstractmethod
    def detect_outliers(
        self, embeddings: np.ndarray, labels: list[int]
    ) -> tuple[Optional[np.ndarray], dict[int, list[float]]]:
        pass
