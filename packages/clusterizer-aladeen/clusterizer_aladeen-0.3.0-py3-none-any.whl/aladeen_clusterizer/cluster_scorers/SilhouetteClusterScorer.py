from sklearn.metrics import silhouette_samples
import numpy as np

from ..abstract.ClusterScorer import ClusterScorer


class SilhouetteClusterScorer(ClusterScorer):
    def calculate_scores(
        self, embeddings: np.ndarray, labels: np.ndarray
    ) -> dict[int, list[float]]:
        silhouette_scores = silhouette_samples(embeddings, labels)
        scores = {}
        for label in np.unique(labels):
            cluster_mask = labels == label
            scores[label] = silhouette_scores[cluster_mask].tolist()
        return scores
