# from sklearn.manifold import TSNE
# # from umap import UMAP
# import numpy as np
# import matplotlib.pyplot as plt


# from .ResultVisualizer import ResultVisualizer


# class MultiResultVisualizer(ResultVisualizer):
#     def __init__(self, config: dict, cluster_scores: list[int] = None):
#         super().__init__(config, cluster_scores)

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

#         # if method == "tsne":
#         #     tsne = TSNE(n_components=2, random_state=42)
#         #     reduced_embeddings = tsne.fit_transform(embeddings)
#         # elif method == "umap":
#         #     umap_reducer = UMAP(n_components=2, random_state=42)
#         #     reduced_embeddings = umap_reducer.fit_transform(embeddings)
#         # else:
#         #     raise ValueError(f"Invalid visualization method: {method}")

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
#         self, clusters: list[int], embeddings: np.ndarray, data: List[str]
#     ):
#         self.labels = clusters
#         self.embeddings = embeddings
#         self.data = data

#         for label, score in sorted(
#             self.cluster_scores.items(), key=lambda x: x[1], reverse=True
#         ):
#             print(f"Cluster {label} (Silhouette Score: {score}):")
#             self._print_cluster(label)
#             print()

#     def _print_cluster(self, label):
#         cluster_data = [
#             self.data[i] for i in range(len(self.data)) if self.labels[i] == label
#         ]
#         for doc in cluster_data:
#             print(doc[0].replace("\n", "").strip())
