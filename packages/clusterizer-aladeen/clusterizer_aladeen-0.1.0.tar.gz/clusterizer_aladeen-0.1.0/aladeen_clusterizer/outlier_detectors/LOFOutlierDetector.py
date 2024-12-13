from sklearn.neighbors import LocalOutlierFactor
from sklearn.metrics import silhouette_score
from typing import Optional
import numpy as np


from ..abstract.OutlierDetector import OutlierDetector
from ..abstract.ClusterScorer import ClusterScorer


class LOFOutlierDetector(OutlierDetector):
    def __init__(
        self,
        outlier_scorer: ClusterScorer,
        n_neighbors_range: tuple[int, int],
        step: int,
    ):
        super().__init__(outlier_scorer)
        self.n_neighbors_range = n_neighbors_range
        self.step = step

    def detect_outliers(
        self, embeddings: np.ndarray, labels: list[int]
    ) -> tuple[Optional[np.ndarray], dict[int, list[float]]]:
        # FIXME: remove unused variable
        # best_n_neighbors = None
        best_silhouette_score = -1
        best_outlier_mask = None
        scores = self.outlier_scorer.calculate_scores(embeddings, labels)

        for n_neighbors in range(
            self.n_neighbors_range[0], self.n_neighbors_range[1] + 1, self.step
        ):
            lof = LocalOutlierFactor(n_neighbors=n_neighbors, contamination="auto")
            outlier_scores = lof.fit_predict(embeddings)
            outlier_mask = outlier_scores == -1

            silhouette_avg = silhouette_score(
                embeddings[~outlier_mask], labels[~outlier_mask]
            )
            if silhouette_avg > best_silhouette_score:
                best_silhouette_score = silhouette_avg
                # FIXME: remove unused variable
                # best_n_neighbors = n_neighbors
                best_outlier_mask = outlier_mask

        return best_outlier_mask, scores
