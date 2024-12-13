from sklearn.metrics import silhouette_score
from typing import Optional
import numpy as np


from ..abstract.OutlierDetector import OutlierDetector
from ..abstract.ClusterScorer import ClusterScorer


class DynamicZScoreOutlierDetector(OutlierDetector):
    def __init__(
        self,
        outlier_scorer: ClusterScorer,
        threshold_range: tuple[float, float],
        step: float,
    ):
        super().__init__(outlier_scorer)
        self.threshold_range = threshold_range
        self.step = step

    def detect_outliers(
        self, embeddings: np.ndarray, labels: list[int]
    ) -> tuple[Optional[np.ndarray], dict[int, list[float]]]:
        scores = self.outlier_scorer.calculate_scores(embeddings, labels)
        best_threshold = None
        best_silhouette_score = -1
        best_outlier_mask = None

        for threshold in np.arange(
            self.threshold_range[0], self.threshold_range[1] + self.step, self.step
        ):
            outlier_mask = np.full(len(labels), False)
            for label, cluster_scores in scores.items():
                mean_score = np.mean(cluster_scores)
                std_score = np.std(cluster_scores)
                cluster_mask = labels == label
                adjusted_threshold = threshold * (1 + std_score * 2)

                z_scores = (np.array(cluster_scores) - mean_score) / std_score
                outlier_mask[cluster_mask] = z_scores < -adjusted_threshold

            silhouette_avg = silhouette_score(
                embeddings[~outlier_mask], labels[~outlier_mask]
            )
            if silhouette_avg > best_silhouette_score:
                best_silhouette_score = silhouette_avg
                best_threshold = threshold
                best_outlier_mask = outlier_mask

        print(f"Best threshold: {best_threshold:.2f}")
        print(f"Best Silhouette Score: {best_silhouette_score:.2f}")

        return best_outlier_mask, scores
