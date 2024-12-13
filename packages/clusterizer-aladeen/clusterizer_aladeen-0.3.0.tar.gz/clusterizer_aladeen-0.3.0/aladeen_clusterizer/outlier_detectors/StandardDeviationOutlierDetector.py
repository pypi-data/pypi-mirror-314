import numpy as np
from typing import Optional

from ..abstract.OutlierDetector import OutlierDetector
from ..abstract.ClusterScorer import ClusterScorer


class StandardDeviationOutlierDetector(OutlierDetector):
    def __init__(self, outlier_scorer: ClusterScorer, threshold: float):
        super().__init__(outlier_scorer)
        self.threshold = threshold

    def detect_outliers(
        self, embeddings: np.ndarray, labels: list[int]
    ) -> tuple[Optional[np.ndarray], dict[int, list[float]]]:
        scores = self.outlier_scorer.calculate_scores(embeddings, labels)
        outlier_mask = np.full(len(labels), False)
        for label, cluster_scores in scores.items():
            mean_score = np.mean(cluster_scores)
            std_score = np.std(cluster_scores)
            cluster_mask = labels == label

            outlier_mask[cluster_mask] = (
                np.array(cluster_scores) < mean_score - self.threshold * std_score
            )

        return outlier_mask, scores
