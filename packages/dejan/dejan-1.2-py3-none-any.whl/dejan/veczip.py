import numpy as np
from sklearn.cluster import DBSCAN
from tqdm import tqdm


class veczip:
    """
    A core utility for compressing embeddings by reducing dimensionality based on holistic dimension analysis.

    It takes as input a numpy array of embeddings and returns the indices of the dimensions to retain,
    allowing the caller to then apply this selection to any column it wants.
    """

    def __init__(self, target_dims=16):
        """
        Initialize veczip for compressing embeddings.

        Args:
            target_dims (int): Number of dimensions to retain after pruning. Default is 16.
        """
        self.target_dims = target_dims

    def analyze_dimensions(self, embeddings):
        """
        Analyzes dimensions in bulk to identify which to prune.

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


    def compress(self, embeddings):
        """
        Compresses embeddings to the target dimensions.

        Args:
            embeddings (np.ndarray): Bulk embeddings (N x D).

        Returns:
            np.ndarray: Indices of the dimensions to retain.
        """
        n_dims = embeddings.shape[1]
        effective_target_dims = min(self.target_dims, n_dims)
        print(f"Pruning embeddings to {effective_target_dims} dimensions...")

        commonality_scores = self.analyze_dimensions(embeddings)
        sorted_indices = np.argsort(commonality_scores)
        top_indices = sorted_indices[:effective_target_dims]
        print("Compression completed.")
        return top_indices

if __name__ == '__main__':
    # Example usage (can be removed when used as lib)
    embeddings = np.random.rand(100, 50)
    compressor = veczip(target_dims=16)
    retained_indices = compressor.compress(embeddings)
    print("Retained indices:", retained_indices)
    compressed_embeddings = embeddings[:, retained_indices]
    print("Shape of compressed embeddings", compressed_embeddings.shape)