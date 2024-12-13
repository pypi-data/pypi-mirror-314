import time
from typing import Callable, Optional
import numpy as np
from hdbscan import HDBSCAN, all_points_membership_vectors
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import ParameterSampler
from ..misc.BenchmarkUtils import evaluate
from ..abstract.ClusteringAlgorithm import ClusteringAlgorithm
from ..cluster_scorers.CosineSimililarityClusterScorer import CosineSimililarityClusterScorer
from sklearn.decomposition import PCA
import umap
from tqdm import tqdm

class HDBSCANClustering(ClusteringAlgorithm):
    def __init__(self, config: dict):
        self.config = config

    def cluster(self, embeddings: np.ndarray) -> list[int]:
        embeddings, config = self._prepare_embeddings(embeddings)
        clusterer = HDBSCAN(**config)
        clusterer.fit(embeddings)
        labels = self._assign_labels(clusterer)
        return labels

    def hyperparameter_tuning(
        self,
        embeddings: np.ndarray,
        uuids: list[str],
        expected_labels: list[int],
        outlier_detector: Optional[Callable] = None,
        n_iter_search: int = 20,
    ) -> dict:
        print("Tuning hyperparameters for HDBSCAN, outlier detection, and dimensionality reduction...")
        param_list = self._generate_parameter_list(n_iter_search)
        best_params_list = self._evaluate_parameters(embeddings, uuids, expected_labels, outlier_detector, param_list)
        self._print_final_results(best_params_list)
        return best_params_list

    def _prepare_embeddings(self, embeddings: np.ndarray) -> tuple:
        config = self.config.copy()
        if self.config["metric"] == "cosine":
            embeddings = cosine_similarity(embeddings)
            config["metric"] = "precomputed"
        config["prediction_data"] = True
        embeddings = embeddings.astype(np.float64)
        return embeddings, config

    def _assign_labels(self, clusterer) -> list[int]:
        soft_clusters = all_points_membership_vectors(clusterer)
        labels_from_probabilities = np.argmax(soft_clusters, axis=1)
        labels = [
            label if label != -1 else labels_from_probabilities[idx]
            for idx, label in enumerate(clusterer.labels_)
        ]
        return labels

    def _generate_parameter_list(self, n_iter_search: int) -> list:
        hdbscan_param_dist, outlier_param_dist, pca_param_dist, _, no_dim_reducer_param_dist = self._define_param_distributions()
        # pca_param_list = list(ParameterSampler(
        #     {**hdbscan_param_dist, **outlier_param_dist, **pca_param_dist},
        #     n_iter=n_iter_search // 2
        # ))
        # umap_param_list = list(ParameterSampler(
        #     {**hdbscan_param_dist, **outlier_param_dist, **umap_param_dist},
        #     n_iter=n_iter_search // 3
        # ))
        no_dim_reducer_param_list = list(ParameterSampler(
            {**hdbscan_param_dist, **outlier_param_dist, **no_dim_reducer_param_dist},
            n_iter=n_iter_search
        ))
        # return pca_param_list + umap_param_list + no_dim_reducer_param_list
        return no_dim_reducer_param_list

    def _define_param_distributions(self) -> tuple:
        hdbscan_param_dist = {
            "min_samples": [5, 6, 7, 8, 9, 10],
            "min_cluster_size": [2],
            "cluster_selection_method": ["eom"],
            "metric": ["euclidean"],
            "algorithm": ["best", "prims_kdtree"],
            "cluster_selection_epsilon": [0.1, 0.15],
            "alpha": [0.5, 0.55, 0.6, 0.65],
            "prediction_data": [True]
        }

        outlier_param_dist = {
            "threshold": [0.6, 0.7, 0.75, 0.8, 0.85, 0.9, 1.0],
            "min_score": [0.8, 0.75, 0.7, 0.65, 0.6]
        }

        pca_param_dist = {
            'reducer': ['pca'],
            'pca__n_components': [25, 50, 100, 150, 300, 500],
            'pca__svd_solver': ['auto', 'full', 'arpack', 'randomized'],
            'pca__whiten': [True, False]
        }
        umap_param_dist = {
            'reducer': ['umap'],
            'umap__n_neighbors': [5, 10, 15],
            'umap__min_dist': [0.1, 0.5, 0.9],
            'umap__n_components': [50, 75, 100, 125, 150]
        }
        no_dim_reducer_param_dist = {
            'reducer': ['none']
        }
        return hdbscan_param_dist, outlier_param_dist, pca_param_dist, umap_param_dist, no_dim_reducer_param_dist

    def _evaluate_parameters(self, embeddings, uuids, expected_labels, outlier_detector, param_list) -> list:
        best_params_list = []
        start_time = time.time()

        for i, params in tqdm(enumerate(param_list), total=len(param_list)):
            # Rest of the code...
            # print(f"Iteration {i+1}/{len(param_list)}")
            # print(f"Trying parameters: {params}")
            try:
                metrics, predicted_labels = self._attempt_clustering(embeddings, params, uuids, expected_labels, outlier_detector)
                # score = aggregate_metrics(metrics)
                score = metrics['final_score']
                best_params_list.append({'params': params, 'score': score, 'metrics': metrics})
                best_params_list.sort(key=lambda x: x['score'], reverse=True)
                if len(best_params_list) > 10:
                    best_params_list.pop()
            except Exception as e:
                print(f"Error with parameters {params}: {e}")
                # raise e
                continue

            if i % 50 == 0:
                self._print_intermediate_results(i, best_params_list)

        elapsed_time = time.time() - start_time
        print(f"Tuning completed in {elapsed_time:.2f} seconds")
        return best_params_list

    # def aggregate_metrics(metrics: dict) -> float:
    #     return metrics['final_score']

    def _attempt_clustering(self, embeddings, params, uuids, expected_labels, outlier_detector) -> tuple:
        hdbscan_params, outlier_params, dim_reducer_params = self._split_param_dict(params)
        reduced_embeddings = self._apply_dimensionality_reduction(embeddings, dim_reducer_params)
        predicted_labels = self._apply_clustering_and_outlier_detection(reduced_embeddings, hdbscan_params, outlier_detector, outlier_params)
        metrics = evaluate(uuids, predicted_labels.tolist(), expected_labels, reduced_embeddings)
        # print(f"Score: {metrics['final_score']}")
        return metrics, predicted_labels

    def _split_param_dict(self, params: dict) -> tuple:
        hdbscan_param_dist, outlier_param_dist, _, _, _ = self._define_param_distributions()
        hdbscan_params = {k: v for k, v in params.items() if k in hdbscan_param_dist}
        outlier_params = {k: v for k, v in params.items() if k in outlier_param_dist}
        dim_reducer_params = {k: v for k, v in params.items() if 'reducer' in k or k.startswith(params['reducer'])}
        return hdbscan_params, outlier_params, dim_reducer_params

    def _apply_dimensionality_reduction(self, embeddings: np.ndarray, params: dict) -> np.ndarray:
        if params['reducer'] == 'pca':
            pca = PCA(n_components=params['pca__n_components'])
            return pca.fit_transform(embeddings)
        elif params['reducer'] == 'umap':
            umap_reducer = umap.UMAP(n_neighbors=params['umap__n_neighbors'], min_dist=params['umap__min_dist'])
            return umap_reducer.fit_transform(embeddings)
        elif params['reducer'] == 'none':
            return embeddings
        return embeddings

    def _apply_clustering_and_outlier_detection(
        self,
        embeddings: np.ndarray,
        hdbscan_params: dict,
        outlier_detector: Optional[Callable],
        outlier_params: dict
    ) -> np.ndarray:
        clusterer = HDBSCAN(**hdbscan_params)
        clusterer.fit(embeddings)
        labels = self._assign_labels(clusterer)
        labels = self._detect_outliers_and_adjust_labels(embeddings, labels, outlier_detector, outlier_params)
        return labels

    def _detect_outliers_and_adjust_labels(self, embeddings, labels, outlier_detector, outlier_params) -> np.ndarray:
        outlier_scorer = CosineSimililarityClusterScorer()
        if outlier_detector:
            outlier_mask, item_scores = outlier_detector.detect_outliers(embeddings, labels)
        else:
            item_scores = outlier_scorer.calculate_scores(embeddings, labels)
            outlier_mask = np.full(len(labels), False)

        if outlier_detector:
            outlier_detector.threshold = outlier_params['threshold']
            outlier_detector.min_score = outlier_params['min_score']
            outlier_mask, _ = outlier_detector.detect_outliers(embeddings, labels)
            labels = np.where(outlier_mask, -1, labels)
        return labels

    def _print_intermediate_results(self, iteration: int, best_params_list: list):
        print("Top 10 Best Parameters at iteration", iteration)
        for idx, entry in enumerate(best_params_list):
            print(f"Rank {idx+1}: Score {entry['score']}, Parameters: {entry['params']}\nMetrics: {entry['metrics']},")
            print()

    def _print_final_results(self, best_params_list: list):
        print("! Final - Top 10 Best Parameters: !")
        for idx, entry in enumerate(best_params_list):
            print(f"Rank {idx+1}: Score {entry['score']}, Parameters: {entry['params']}")