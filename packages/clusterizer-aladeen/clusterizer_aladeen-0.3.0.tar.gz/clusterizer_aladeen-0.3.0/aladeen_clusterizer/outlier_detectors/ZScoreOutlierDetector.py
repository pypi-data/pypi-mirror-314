import numpy as np
from typing import Optional


from ..abstract.OutlierDetector import OutlierDetector
from ..abstract.ClusterScorer import ClusterScorer


class ZScoreOutlierDetector(OutlierDetector):
    def __init__(
        self, outlier_scorer: ClusterScorer, threshold: float, min_score: float
    ):
        super().__init__(outlier_scorer)
        self.threshold = threshold
        self.min_score = min_score

    def detect_outliers(
        self, embeddings: np.ndarray, labels: list[int]
    ) -> tuple[Optional[np.ndarray], dict[int, list[float]]]:
        scores = self.outlier_scorer.calculate_scores(embeddings, labels)
        outlier_mask = np.full(len(labels), False)
        for label, cluster_scores in scores.items():
            mean_score = np.mean(cluster_scores)
            std_score = np.std(cluster_scores)
            cluster_mask = labels == label

            z_scores = np.divide((np.array(cluster_scores) - mean_score), std_score, out=np.zeros_like(cluster_scores), where=std_score!=0)
            outlier_mask[cluster_mask] = (z_scores < -self.threshold) & (
                np.array(cluster_scores) < self.min_score
            )

        return outlier_mask, scores
