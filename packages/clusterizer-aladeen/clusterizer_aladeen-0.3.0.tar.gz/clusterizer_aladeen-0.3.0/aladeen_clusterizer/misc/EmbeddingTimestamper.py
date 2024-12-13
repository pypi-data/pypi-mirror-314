import numpy as np


class EmbeddingTimestamper:
    def __init__(self, config: dict):
        self.config = config

    def timestamp(self, embeddings: np.ndarray, timestamps: list[float]) -> np.ndarray:
        # Normalize timestamps to be between 0 and 1
        min_timestamp = min(timestamps)
        max_timestamp = max(timestamps)
        normalized_timestamps = [
            (t - min_timestamp) / (max_timestamp - min_timestamp) for t in timestamps
        ]

        # Add timestamp dimension to the embeddings
        timestamped_embeddings = np.hstack(
            (embeddings, np.array(normalized_timestamps)[:, np.newaxis])
        )

        return timestamped_embeddings
