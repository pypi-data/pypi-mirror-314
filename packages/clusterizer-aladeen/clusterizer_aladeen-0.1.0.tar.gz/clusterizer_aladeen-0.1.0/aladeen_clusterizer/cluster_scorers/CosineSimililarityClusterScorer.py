from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


from ..abstract.ClusterScorer import ClusterScorer


class CosineSimililarityClusterScorer(ClusterScorer):
    def calculate_scores(
        self, embeddings: np.ndarray, labels: np.ndarray
    ) -> dict[int, list[float]]:
        unique_labels = np.unique(labels)
        scores = {}
        for label in unique_labels:
            cluster_mask = labels == label
            cluster_embeddings = embeddings[cluster_mask]
            cluster_scores = self._calculate_cosine_similarity_scores(
                cluster_embeddings
            )
            scores[label] = cluster_scores
        return scores

    def _calculate_cosine_similarity_scores(
        self, embeddings: np.ndarray
    ) -> list[float]:
        if len(embeddings) == 1:
            return [1.0]
        similarities = cosine_similarity(embeddings)
        np.fill_diagonal(similarities, 0)
        scores = np.sum(similarities, axis=1) / (len(embeddings) - 1)
        return scores.tolist()
