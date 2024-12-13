import numpy as np
import pandas as pd
# from umap import UMAP
from typing import Optional


from .abstract.ClusterScorer import ClusterScorer
from .abstract.OutlierDetector import OutlierDetector
from .embedding_generators.SentenceTransformerEmbeddingGenerator import (
    SentenceTransformerEmbeddingGenerator,
)
from .cluster_scorers.SilhouetteClusterScorer import SilhouetteClusterScorer
from .cluster_scorers.CosineSimililarityClusterScorer import (
    CosineSimililarityClusterScorer,
)
from .clustering_algorithms.HDBSCANClustering import HDBSCANClustering
# from .result_visualizers.ResultVisualizer import ResultVisualizer
from .misc.EmbeddingTimestamper import EmbeddingTimestamper


class ClusteringPipeline:
    def __init__(
        self,
        config: dict,
        model_name: str,
        uuid_col: str,
        datetime_col: str,
        outlier_scorer: ClusterScorer,
        outlier_detector: OutlierDetector,
        # FIXME: unused variable
        embedding_col: Optional[str] = None,

        title_col: Optional[str] = None,
        description_col: Optional[str] = None,
        content_col: Optional[str] = None,

        verbose: bool = False,
    ):
        # if embedding_col is None and title_col is None:
        #     raise ValueError("Either 'embedding_col' or 'title_col' must be provided")

        self.config = config

        self.embedding_generator = SentenceTransformerEmbeddingGenerator(
            config, model_name
        )
        
        self.clustering_algorithm = HDBSCANClustering(config)
        
        self.dimensionality_reducer = None
        # self.dimensionality_reducer = UMAP(
        #     n_components=100, random_state=42, metric="euclidean"
        # )
        # self.dimensionality_reducer = VAEDimensionalityReducer(input_dim=1025, latent_dim=100)
        # self.dimensionality_reducer = ParametricUMAP(n_components=100, random_state=42)

        # self.visualizer = ResultVisualizer(config, outlier_scorer=outlier_scorer)
        self.embedding_timestamper = EmbeddingTimestamper(config)
        self.uuid_col = uuid_col

        self.title_col = title_col
        self.description_col = description_col
        self.content_col = content_col

        self.datetime_col = datetime_col

        self.raw_embeddings = None
        self.processed_embeddings = None
        self.data = None
        self.labels = None
        self.cluster_scores = None
        self.outlier_scorer = outlier_scorer
        self.outlier_detector = outlier_detector
        self.outlier_mask: Optional[np.ndarray] = None
        self.verbose = verbose

        if (self.verbose):
            print("Pipeline initialized")

    def run(self, data: pd.DataFrame, embeddings=None, process_embeddings=True):
        self._process_data(data, embeddings, process_embeddings)
        return self._run()

    def _process_data(self, data, embeddings, process_embeddings, data_is_list=False):
        self.data = data

        if data_is_list:
            titles = data
        else:
            titles = data[self.title_col].tolist()

        if embeddings is None:
            if (self.verbose):
                print("Generating embeddings")
            embeddings = self._generate_embeddings(titles)
            if (self.verbose):
                print("Embeddings generated")

        self.raw_embeddings = embeddings
        
        # FIXME: add timestamps
        # timestamps = self.get_timestamps(data)

        if process_embeddings:
            self.processed_embeddings = self._process_embeddings(embeddings)
        else:
            self.processed_embeddings = embeddings

    def get_timestamps(self, data):
        datetimes = data[self.datetime_col].tolist()
        timestamps = [dt.timestamp() for dt in datetimes]
        return timestamps

    def run_embeddings_only(self, embeddings_df):
        # embeddings = embeddings_df["title_embed"].values
        self.data = embeddings_df
        embeddings = np.stack(embeddings_df["title_embed"].values)
        # FIXME: add timestamps
        # timestamps = self.get_timestamps(embeddings_df)
        self.processed_embeddings = self._process_embeddings(embeddings)
        return self._run()

    def _run(self):
        # get labels
        self.labels = self._cluster(self.processed_embeddings)

        # detect outliers
        self.detect_outliers(self.raw_embeddings, self.labels)

        # mark outliers as -1
        for i, l in enumerate(self.labels):
            if self.outlier_mask[i]:
                self.labels[i] = -1

        # score clusters
        self.cluster_scores = self._calculate_cluster_scores(self.labels)

        # sort clusters by score
        self.cluster_scores = dict(
            sorted(self.cluster_scores.items(), key=lambda x: x[1], reverse=True)
        )

        return self.labels

    def detect_outliers(self, embeddings: np.ndarray, labels: list[int]):
        if self.outlier_detector is not None:
            outlier_mask, item_scores = self.outlier_detector.detect_outliers(
                embeddings, labels
            )

            if outlier_mask is not None:
                self.outlier_mask = outlier_mask
                self.item_scores = item_scores

        else:
            self.item_scores = self.outlier_scorer.calculate_scores(embeddings, labels)
            self.outlier_mask = np.full(len(labels), False)

        if (self.verbose):
            print("Outliers:", self.outlier_mask)

        return self.outlier_mask, self.item_scores

    def _generate_embeddings(self, data):
        embeddings = self.embedding_generator.generate_embeddings(data)
        return embeddings

    def _process_embeddings(self, embeddings):
        self.raw_embeddings = embeddings
        # timestamped_embeddings = self.embedding_timestamper.timestamp(embeddings, timestamps)
        # timestamped_embeddings = embeddings
        if self.dimensionality_reducer is not None:
            return self.dimensionality_reducer.fit_transform(
                embeddings
            )
        else:
            return embeddings

    def _cluster(self, embeddings):
        clusters = self.clustering_algorithm.cluster(embeddings)
        clusters_array = np.array(clusters)

        if (self.verbose):
            print("Shape of clusters_array:", clusters_array.shape)

        return clusters_array

    def _calculate_cluster_scores(self, labels):
        silhouette = SilhouetteClusterScorer()
        scored_silhouette_samples = silhouette.calculate_scores(
            self.raw_embeddings, labels
        )
        cosine = CosineSimililarityClusterScorer()
        scored_cosine_samples = cosine.calculate_scores(self.raw_embeddings, labels)

        if (self.verbose):
            print(scored_cosine_samples)

        cluster_scores = {}
        unique_labels = np.unique(labels)
        for label in unique_labels:
            # silhouette_scores = scored_silhouestte_samples[label]
            cosine_scores = scored_cosine_samples[label]
            cluster_scores[label] = np.mean(cosine_scores)

        if (self.verbose):
            print(scored_cosine_samples)

        return cluster_scores

    def get_clusters(self, threshold: bool | float = 0.70, include_outliers: bool = False):
        labels = self.labels
        item_dicts = []
        scorer = CosineSimililarityClusterScorer()
        scored_samples = scorer.calculate_scores(self.raw_embeddings, labels)
        if (self.verbose):
            print("Length of labels:", len(labels))
            print("Scored Samples:", scored_samples)

        for i, label in enumerate(labels):
            if label == -1:
                score = -1
            else:
                score = scored_samples[label][0]
                scored_samples[label].pop(0)

            if threshold and score < threshold:
                label = -1

            item_dicts.append(
                {
                    "uuid": self.data.iloc[i][self.uuid_col],
                    "label": int(label),
                    "score": float(score),
                }
            )

        clusters = {}
        for item in item_dicts:
            label = item["label"]

            if label not in clusters:
                # clusters[label] = {"score": item["score"], "items": [item["uuid"]]} OLD
                clusters[label] = {"score": item["score"], "items": [item]}
            else:
                # clusters[label]["items"].append(item["uuid"])        
                clusters[label]["items"].append(item)    

        result = map(lambda x: {**{"label": x}, **clusters[x]}, clusters)
        result = sorted(result, key=lambda x: x["score"], reverse=True)
        result = filter(lambda x: len(x["items"]) > 1, result)
        if not include_outliers:
            result = filter(lambda x: x["label"] != -1, result)

        result = list(result)

        return result

    # def visualize(self, method="tsne"):
    #     self.visualizer.visualize(
    #         self.labels, self.processed_embeddings, self.data, method
    #     )

    def hyperparameter_tuning(self, data: list[str], uuids: list[str], expected_labels: list[int], n_iter_search: int = 20):
        if self.raw_embeddings is None:
            self._process_data(data, None, False, data_is_list=True)

        print("shape of processed embeddings:", self.raw_embeddings.shape)
                
        best_params = self.clustering_algorithm.hyperparameter_tuning(
            self.raw_embeddings, uuids, expected_labels, self.outlier_detector, n_iter_search
        )

        return best_params