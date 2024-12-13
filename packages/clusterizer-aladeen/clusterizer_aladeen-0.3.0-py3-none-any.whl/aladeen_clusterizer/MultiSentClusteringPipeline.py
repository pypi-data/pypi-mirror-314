# import numpy as np
# from umap import UMAP

# from .result_visualizers.MultiResultVisualizer import MultiResultVisualizer
# from .ClusteringPipeline import ClusteringPipeline


# class MultiSentClusteringPipeline(ClusteringPipeline):
#     """
#     A class representing a double clustering pipeline.
#     Embeds first and second sentences separately and concatenates the embeddings to form the final embedding.
#     Then performs dimensionality reduction and clustering on the final embeddings.

#     Args:
#         config (Dict): A dictionary containing the configuration parameters for the pipeline.
#         model_name (str, optional): The name of the model to be used. Defaults to None.
#     """

#     def __init__(self, config: dict, model_name: str = None):
#         super().__init__(config, model_name)
#         self.dimensionality_reducer = UMAP(n_components=100, random_state=42)
#         self.visualizer = MultiResultVisualizer(config)
#         print("DoubleClusteringPipeline initialized")

#     def run(self, data: list[list[str]]):
#         # self.data = TextPreprocessor(self.config).preprocess(data)
#         self.data = data
#         self.embeddings = self._generate_double_embeddings(self.data)
#         print("Shape of embeddings:", self.embeddings.shape)
#         print("timestamp", self.embeddings[0][-1])
#         return self._run(self.data)

#     def _generate_double_embeddings(self, data: list[list[str]]):
#         print(data[0])
#         sentence_embeddings = []
#         for i in range(len(data[0])):
#             print("Processing sentence", i)
#             sentences = [d[i] for d in data]
#             embeddings = self.embedding_generator.generate_embeddings(sentences)
#             sentence_embeddings.append(embeddings)

#         concatenated_embeddings = np.concatenate(sentence_embeddings, axis=1)
#         if self.dimensionality_reducer is not None:
#             concatenated_embeddings = self.dimensionality_reducer.fit_transform(
#                 concatenated_embeddings
#             )
#         print("Shape of concatenated embeddings:", concatenated_embeddings.shape)

#         return concatenated_embeddings
