# from sklearn.manifold import TSNE
# # from umap import UMAP
# import pandas as pd
# import matplotlib.pyplot as plt
# import numpy as np
# from typing import Optional


# from ..abstract.ClusterScorer import ClusterScorer


# class ResultVisualizer:
#     def __init__(
#         self,
#         config: dict,
#         outlier_scorer: ClusterScorer,
#         cluster_scores: Optional[list[int]] = None,
#     ):
#         self.config = config
#         self.outlier_scorer = outlier_scorer
#         self.labels: Optional[list[int]] = None
#         self.embeddings: Optional[np.ndarray] = None
#         self.data: Optional[list[str]] = None
#         self.cluster_scores = cluster_scores
#         self.outlier_scores: Optional[dict[int, list[float]]] = None

#     def visualize(
#         self,
#         clusters: list[int],
#         embeddings: np.ndarray,
#         data: list[str],
#         method="tsne",
#     ):
#         self.labels = clusters
#         self.embeddings = embeddings
#         self.data = data

#         reduced_embeddings = self._reduce_dimensions(embeddings, method)
#         self._plot_clusters(reduced_embeddings, clusters, method)

#     def _reduce_dimensions(self, embeddings: np.ndarray, method: str) -> np.ndarray:
#         # if method == "tsne":
#         #     reducer = TSNE(n_components=2, random_state=42)
#         # elif method == "umap":
#         #     reducer = UMAP(n_components=2, random_state=42)
#         # else:
#         #     raise ValueError(f"Invalid visualization method: {method}")

#         # reduced_embeddings = reducer.fit_transform(embeddings)
#         # return reduced_embeddings

#     def _plot_clusters(
#         self, reduced_embeddings: np.ndarray, clusters: list[int], method: str
#     ):
#         fig, ax = plt.subplots(figsize=(8, 6))
#         scatter = ax.scatter(
#             reduced_embeddings[:, 0],
#             reduced_embeddings[:, 1],
#             c=clusters,
#             cmap="viridis",
#         )
#         legend = ax.legend(*scatter.legend_elements(), title="Clusters")
#         ax.add_artist(legend)
#         ax.set_title(f"{method.upper()} Visualization")
#         plt.show()

#     def print_clusters(
#         self,
#         clusters: list[int],
#         embeddings: np.ndarray,
#         data: pd.DataFrame,
#         title_col: str,
#         content_col: str,
#         sort_by="mean_similarity",
#     ):
#         self.labels = clusters
#         self.embeddings = embeddings
#         self.data = data

#         cluster_metrics = self._calculate_cluster_metrics()
#         sorted_clusters = self._sort_clusters(cluster_metrics, sort_by)

#         self.outlier_scores = self.outlier_scorer.calculate_scores(
#             self.embeddings, self.labels
#         )

#         assert self.data is not None

#         for label, metrics in sorted_clusters:
#             cluster_mask = self.labels == label
#             cluster_data = self.data[cluster_mask]
#             cluster_embeddings = self.embeddings[cluster_mask]
#             cluster_outlier_scores = self.outlier_scores[label]

#             self._print_cluster_details(
#                 label,
#                 metrics,
#                 cluster_data,
#                 cluster_embeddings,
#                 title_col,
#                 content_col,
#                 cluster_outlier_scores,
#             )

#     def _print_cluster_details(
#         self,
#         label: int,
#         metrics: dict[str, float],
#         cluster_data: pd.DataFrame,
#         cluster_embeddings: np.ndarray,
#         title_col: str,
#         content_col: str,
#         cluster_outlier_scores: list[float],
#     ):
#         print(
#             f"Cluster {label} (Mean Similarity: {metrics['mean_similarity']:.2f}, "
#             f"Silhouette Score: {metrics['silhouette_score']:.2f}):"
#         )

#         sorted_indices = np.argsort(cluster_outlier_scores)[::-1]

#         for i in sorted_indices:
#             row = cluster_data.iloc[i]
#             combined_text = f"{row[title_col]}".replace("\n", " ").strip()
#             outlier_score = cluster_outlier_scores[i]
#             is_outlier = self.outlier_mask[np.where(self.labels == label)[0][i]]
#             if is_outlier:
#                 print(f"Score.: {outlier_score:.2f}) [OUTLIER]  {combined_text}")
#             else:
#                 print(f"Score.: {outlier_score:.2f})            {combined_text}")

#         print()

#     def _calculate_cluster_metrics(self) -> dict[int, dict[str, float]]:
#         assert self.labels is not None
#         assert self.outlier_scores is not None
#         assert self.cluster_scores is not None

#         cluster_metrics = {}
#         for label in np.unique(self.labels):
#             avg_scores = self.outlier_scores[label]
#             # print('-----------------')
#             # print(avg_scores)
#             # print('-----------------')

#             mean_similarity = np.mean(avg_scores)
#             silhouette_score = self.cluster_scores[label]
#             cluster_metrics[label] = {
#                 "mean_similarity": mean_similarity,
#                 "silhouette_score": silhouette_score,
#             }
#         return cluster_metrics

#     def _sort_clusters(
#         self, cluster_metrics: dict[int, dict[str, float]], sort_by: str
#     ) -> list[tuple[int, dict[str, float]]]:
#         if sort_by == "mean_similarity":
#             return sorted(
#                 cluster_metrics.items(),
#                 key=lambda x: x[1]["mean_similarity"],
#                 reverse=True,
#             )
#         elif sort_by == "silhouette_score":
#             return sorted(
#                 cluster_metrics.items(),
#                 key=lambda x: x[1]["silhouette_score"],
#                 reverse=True,
#             )
#         elif sort_by == "combined":
#             return sorted(
#                 cluster_metrics.items(),
#                 key=lambda x: (x[1]["mean_similarity"] + x[1]["silhouette_score"]) / 2,
#                 reverse=True,
#             )
#         else:
#             raise ValueError(f"Invalid sorting criterion: {sort_by}")

#     def set_outlier_mask(self, outlier_mask: np.ndarray):
#         self.outlier_mask = outlier_mask
