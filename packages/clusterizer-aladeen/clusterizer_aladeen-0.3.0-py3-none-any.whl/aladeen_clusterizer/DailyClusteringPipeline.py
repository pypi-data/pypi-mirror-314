from typing import Optional
import numpy as np
import pandas as pd

from .abstract import ClusterScorer, OutlierDetector
from .ClusteringPipeline import ClusteringPipeline
from .embedding_generators.SentenceTransformerEmbeddingGenerator import SentenceTransformerEmbeddingGenerator

class DailyClusteringPipeline(ClusteringPipeline):
    def __init__(
        self,
        config: dict,
        model_name: str,
        uuid_col: str,
        datetime_col: str,
        outlier_scorer: ClusterScorer,
        outlier_detector: OutlierDetector,
        title_col: Optional[str] = None,
        description_col: Optional[str] = None,
        content_col: Optional[str] = None,

        verbose: bool = False,
    ):
        super().__init__(
            config=config,
            model_name=model_name,
            uuid_col=uuid_col,
            datetime_col=datetime_col,
            outlier_scorer=None,
            outlier_detector=None,
            title_col=title_col,
            description_col=description_col,
            content_col=content_col,
            verbose=verbose
        )
        self.embedding_generator = SentenceTransformerEmbeddingGenerator(config, model_name)
        self.precomputed_embeddings = None

 
    def compute_embeddings(self, data: pd.DataFrame, batch_size: int = 1000):
        # Initialize a list to store all embeddings
        all_embeddings = []

        # Get the total number of articles
        total_articles = len(data)

        # Iterate over the data in batches
        for start_idx in range(0, total_articles, batch_size):
            end_idx = min(start_idx + batch_size, total_articles)
            batch_data = data.iloc[start_idx:end_idx]

            # Generate embeddings for the current batch
            content_list = batch_data[self.title_col].fillna('').replace('\n', ' ').tolist()
            batch_embeddings = self.embedding_generator.generate_embeddings(content_list)

            # Append batch embeddings to the list
            all_embeddings.append(batch_embeddings)

            if self.verbose:
                print(f"Processed batch {start_idx // batch_size + 1}/{(total_articles - 1) // batch_size + 1}")

        # Concatenate all batch embeddings
        self.precomputed_embeddings = pd.DataFrame(np.vstack(all_embeddings), index=data[self.uuid_col])

        if self.verbose:
            print("Embeddings computed for all articles.")


    def run_daily_clustering(self, data: pd.DataFrame):
        # Ensure embeddings are precomputed
        if self.precomputed_embeddings is None:
            raise ValueError("Embeddings are not precomputed. Call compute_embeddings first.")

        # Group data by date
        data['date'] = data[self.datetime_col].dt.date
        daily_groups = data.groupby('date')

        for date, group in daily_groups:
            print(f"Processing date: {date}")
            # Retrieve embeddings for the current group
            group_embeddings = self.precomputed_embeddings.loc[group[self.uuid_col]]
            # Run clustering directly with precomputed embeddings
            labels = self.run(group, embeddings=group_embeddings.values, process_embeddings=True)
            # Store results
            self.results[date] = {
                'data': group,
                'labels': labels
            }

    def get_results(self):
        return self.results

# Usage
# Assuming you have a DataFrame `df` with the required columns