import numpy as np
from sklearn.cluster import DBSCAN
from tqdm import tqdm


class veczip:
    def __init__(self, target_dims=16):
        """
        Initialize veczip for compressing embeddings.

        Args:
            target_dims (int): Number of dimensions to retain after pruning. Default is 16.
        """
        self.target_dims = target_dims

    def analyze_dimensions(self, embeddings):
        """
        Analyze dimensions in bulk to identify which to prune.

        Args:
            embeddings (np.ndarray): Bulk embeddings (N x D).

        Returns:
            np.ndarray: Commonality scores for each dimension.
        """
        print("Analyzing dimensions...")
        n_samples, n_dims = embeddings.shape
        commonality_scores = []

        for dim in tqdm(range(n_dims), desc="Analyzing Dimensions"):
            dim_values = embeddings[:, dim].reshape(-1, 1)
            dbscan = DBSCAN(eps=0.01, min_samples=2)  # Fixed DBSCAN parameters
            labels = dbscan.fit_predict(dim_values)
            max_cluster_size = max((labels == l).sum() for l in set(labels) if l != -1)
            commonality_scores.append(max_cluster_size)

        return np.array(commonality_scores)

    def prune_dimensions(self, embeddings, commonality_scores):
        """
        Prune embeddings to retain the target number of dimensions.

        Args:
            embeddings (np.ndarray): Original embeddings (N x D).
            commonality_scores (np.ndarray): Commonality scores for each dimension.

        Returns:
            np.ndarray: Pruned embeddings (N x target_dims).
        """
        n_dims = embeddings.shape[1]
        effective_target_dims = min(self.target_dims, n_dims)
        print(f"Pruning embeddings to {effective_target_dims} dimensions...")

        sorted_indices = np.argsort(commonality_scores)
        top_indices = sorted_indices[:effective_target_dims]
        pruned_embeddings = embeddings[:, top_indices]
        return pruned_embeddings, top_indices

    def compress(self, embeddings):
        """
        Compress embeddings to the target dimensions.

        Args:
            embeddings (np.ndarray): Bulk embeddings (N x D).

        Returns:
            np.ndarray: Compressed embeddings (N x target_dims).
        """
        print(f"Analyzing all {embeddings.shape[0]} embeddings for dimensionality reduction...")
        commonality_scores = self.analyze_dimensions(embeddings)
        compressed_embeddings, retained_indices = self.prune_dimensions(embeddings, commonality_scores)
        print("Compression completed.")
        return compressed_embeddings, retained_indices
