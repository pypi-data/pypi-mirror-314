from sklearn.cluster import KMeans
import numpy as np

from ..abstract.ClusteringAlgorithm import ClusteringAlgorithm


class KMeansClustering(ClusteringAlgorithm):
    def __init__(self, config: dict):
        self.config = config

    def cluster(self, embeddings: np.ndarray) -> list[int]:
        kmeans = KMeans(**self.config)
        labels = kmeans.fit_predict(embeddings)

        return labels
