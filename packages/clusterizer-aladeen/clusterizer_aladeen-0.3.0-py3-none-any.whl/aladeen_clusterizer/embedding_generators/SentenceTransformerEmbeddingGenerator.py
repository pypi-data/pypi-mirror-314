import os
import numpy as np
from sentence_transformers import SentenceTransformer

from typing import cast, Any


from ..abstract.EmbeddingGenerator import EmbeddingGenerator


class SentenceTransformerEmbeddingGenerator(EmbeddingGenerator):
    def __init__(self, config: dict, model_name: str):
        self.config = config
        models_cache_dir = os.environ.get("MODELS_CACHE_DIR")
        if (models_cache_dir is None):
            raise Exception("MODELS_CACHE_DIR environment variable is not set")
        model_path = os.path.join(models_cache_dir, model_name)
        self.model = SentenceTransformer(model_path)

    def generate_embeddings(self, data: list[str]) -> np.ndarray:
        embeddings = self.model.encode(data)
        # FIXME: types...
        return cast(Any, embeddings)
