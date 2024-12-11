from dejan.veczip import veczip
import pandas as pd
import numpy as np

def load_and_validate_embeddings(input_file, target_dims):
    """
    Load and preprocess the embeddings file.

    Args:
        input_file (str): Path to the input file.
        target_dims (int): Target dimensionality for reduction.

    Returns:
        tuple: Cleaned embeddings (np.ndarray), metadata (pd.DataFrame), embedding column names (list).
    """
    print(f"Loading data from {input_file}...")
    data = pd.read_csv(input_file)

    # Identify embedding columns (stringified arrays)
    embedding_cols = []
    for col in data.columns:
        if data[col].apply(lambda x: isinstance(x, str) and x.startswith('[')).all():
            embedding_cols.append(col)
    if not embedding_cols:
        raise ValueError("No embedding columns detected. Ensure embeddings are stored as stringified arrays.")

    # Identify non-embedding (metadata) columns
    metadata_cols = data.columns.difference(embedding_cols).tolist()

    # Parse stringified embeddings into numeric arrays
    def parse_embedding(embedding_str):
        try:
            return np.array(eval(embedding_str), dtype=float)
        except Exception:
            return None

    embeddings = []
    valid_rows = []
    for index, row in data.iterrows():
        row_embeddings = []
        for col in embedding_cols:
            parsed = parse_embedding(row[col])
            if parsed is not None:
                row_embeddings.extend(parsed)
            else:
                print(f"Warning: Malformed embedding in row {index}, column {col}. Skipping row.")
                row_embeddings = None
                break  # Skip the row entirely
        if row_embeddings is not None:
            embeddings.append(row_embeddings)
            valid_rows.append(index)  # Track rows that are valid

    if not embeddings:
        raise ValueError("No valid embeddings found in the input file.")

    # Convert embeddings to numpy array
    embeddings = np.array(embeddings)
    print(f"Loaded {embeddings.shape[0]} embeddings with {embeddings.shape[1]} dimensions.")

    # Preserve metadata for valid rows
    metadata = data.loc[valid_rows, metadata_cols]

    return embeddings, metadata, embedding_cols


def save_compressed_embeddings(output_file, metadata, compressed_embeddings, embedding_cols, original_columns):
    """
    Save compressed embeddings to a file, preserving the original column structure.

    Args:
        output_file (str): Path to save the processed output file.
        metadata (pd.DataFrame): Metadata for valid rows.
        compressed_embeddings (np.ndarray): Compressed embedding matrix.
        embedding_cols (list): Original embedding column names.
        original_columns (list): Original column order from the input file.
    """
    print(f"Saving compressed data to {output_file}...")

    # Replace embedding columns with compressed data
    num_embedding_cols = len(embedding_cols)
    split_size = compressed_embeddings.shape[1] // num_embedding_cols

    for i, col in enumerate(embedding_cols):
        start_idx = i * split_size
        end_idx = (i + 1) * split_size
        metadata[col] = [
            compressed_embeddings[j, start_idx:end_idx].tolist() for j in range(compressed_embeddings.shape[0])
        ]

    # Align column order to the original input file
    metadata = metadata.reindex(columns=original_columns)

    # Save the updated DataFrame to the output file
    metadata.to_csv(output_file, index=False)
    print(f"Data saved to {output_file}.")




def run_veczip(input_file, output_file, target_dims=16):
    """
    Main workflow for compressing embeddings using veczip.

    Args:
        input_file (str): Path to the input file containing embeddings.
        output_file (str): Path to save the processed output file.
        target_dims (int): Number of dimensions to retain after compression. Default is 16.
    """
    # Load embeddings, metadata, and column order
    embeddings, metadata, embedding_cols = load_and_validate_embeddings(input_file, target_dims)
    original_columns = list(pd.read_csv(input_file).columns)  # Capture original column order

    # Perform dimensionality reduction
    compressor = veczip(target_dims=target_dims)
    compressed_embeddings, retained_indices = compressor.compress(embeddings)

    # Save compressed embeddings, preserving original column order
    save_compressed_embeddings(output_file, metadata, compressed_embeddings, embedding_cols, original_columns)
    print("Veczip operation completed successfully.")

