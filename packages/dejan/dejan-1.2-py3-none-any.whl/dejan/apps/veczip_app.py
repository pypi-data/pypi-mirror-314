from dejan.veczip import veczip
import pandas as pd
import numpy as np
import csv
import ast
import sys


def is_numeric(s):
    """Checks if a given string is numeric."""
    try:
        float(s)
        return True
    except:
        return False

def parse_as_array(val):
    """Parses a string as an array of numbers."""
    if isinstance(val, (int, float)):
        return [val]
    val_str = str(val).strip()
    if val_str.startswith("[") and val_str.endswith("]"):
        try:
            arr = ast.literal_eval(val_str)
            if isinstance(arr, list) and all(is_numeric(str(x)) for x in arr):
                return arr
            return None
        except:
            return None
    parts = val_str.split(",")
    if len(parts) > 1 and all(is_numeric(p.strip()) for p in parts):
        return [float(p.strip()) for p in parts]
    return None

def get_line_pattern(row):
    """Detects the pattern (text, number, or array) of a row."""
    pattern = []
    for val in row:
        arr = parse_as_array(val)
        if arr is not None:
            pattern.append('arr')
        else:
            if is_numeric(val):
                pattern.append('num')
            else:
                pattern.append('text')
    return pattern

def detect_header(lines):
    """Detects if a CSV has a header."""
    if len(lines) < 2:
        return False
    first_line_pattern = get_line_pattern(lines[0])
    subsequent_patterns = [get_line_pattern(r) for r in lines[1:]]
    if len(subsequent_patterns) > 1:
        if all(p == subsequent_patterns[0] for p in subsequent_patterns) and first_line_pattern != subsequent_patterns[0]:
            return True
    else:
        if subsequent_patterns and first_line_pattern != subsequent_patterns[0]:
            return True
    return False


def looks_like_id_column(col_values):
    """Checks if a column looks like an ID column (sequential integers)."""
    try:
        nums = [int(float(v)) for v in col_values]
        return nums == list(range(nums[0], nums[0] + len(nums)))
    except:
        return False

def detect_columns(file_path):
    """Detects embedding and metadata columns in a CSV file."""
    with open(file_path, "r", newline="", encoding="utf-8") as f:
        try:
            sample = f.read(1024*10)  # Read a larger sample for sniffing
            dialect = csv.Sniffer().sniff(sample, delimiters=[',','\t',';','|'])
            delimiter = dialect.delimiter
        except:
            delimiter = ','
        f.seek(0) # reset file pointer
        reader = csv.reader(f, delimiter=delimiter)
        first_lines = list(reader)[:10]

    if not first_lines:
        raise ValueError("No data")

    has_header = detect_header(first_lines)
    if has_header:
        header = first_lines[0]
        data = first_lines[1:]
    else:
        header = []
        data = first_lines

    if not data:
        return has_header, [], [], delimiter

    cols = list(zip(*data))

    candidate_arrays = []
    candidate_numeric = []
    id_like_columns = set()
    text_like_columns = set()

    for ci, col in enumerate(cols):
        col = list(col)
        parsed_rows = [parse_as_array(val) for val in col]

        if all(r is not None for r in parsed_rows):
            lengths = {len(r) for r in parsed_rows}
            if len(lengths) == 1:
                candidate_arrays.append(ci)
                continue
            else:
                text_like_columns.add(ci)
                continue

        if all(is_numeric(v) for v in col):
            if looks_like_id_column(col):
                id_like_columns.add(ci)
            else:
                candidate_numeric.append(ci)
        else:
            text_like_columns.add(ci)

    identified_embedding_columns = set(candidate_arrays)
    identified_metadata_columns = set()

    if candidate_arrays:
        identified_metadata_columns.update(candidate_numeric)
    else:
        if len(candidate_numeric) > 1:
            identified_embedding_columns.update(candidate_numeric)
        else:
            identified_metadata_columns.update(candidate_numeric)

    identified_metadata_columns.update(id_like_columns)
    identified_metadata_columns.update(text_like_columns)


    if header:
        for ci, col_name in enumerate(header):
            if col_name.lower() == 'id':
                if ci in identified_embedding_columns:
                    identified_embedding_columns.remove(ci)
                identified_metadata_columns.add(ci)
                break

    emb_cols = [header[i] if header and i < len(header) else i for i in identified_embedding_columns]
    meta_cols = [header[i] if header and i < len(header) else i for i in identified_metadata_columns]


    return has_header, emb_cols, meta_cols, delimiter

def load_and_validate_embeddings(input_file, target_dims, confirm=True):
    """Loads, validates, and summarizes embedding data from a CSV."""
    print(f"Loading data from {input_file}...")
    has_header, embedding_columns, metadata_columns, delimiter = detect_columns(input_file)
    data = pd.read_csv(input_file, header=0 if has_header else None, delimiter=delimiter)


    def is_valid_row(row):
        for col in embedding_columns:
            if parse_as_array(row[col]) is None:
                return False
        return True

    valid_rows_filter = data.apply(is_valid_row, axis=1)
    data = data[valid_rows_filter]

    print("\n=== File Summary ===")
    print(f"File: {input_file}")
    print(f"Rows: {len(data)}")
    print(f"Metadata Columns: {metadata_columns}")
    print(f"Embedding Columns: {embedding_columns}")
    print("====================\n")

    if confirm:
        proceed = input("Proceed with these settings? (y/n): ").strip().lower()
        if proceed != "y":
            print("Operation canceled by user.")
            sys.exit(0)

    return data, embedding_columns, metadata_columns, has_header, list(data.columns)

def save_compressed_embeddings(output_file, metadata, compressed_embeddings, embedding_columns, original_columns, has_header):
    """Saves compressed embeddings to a CSV file."""
    print(f"Saving compressed data to {output_file}...")
    metadata = metadata.copy()


    for i, col in enumerate(embedding_columns):
        metadata[col] = [compressed_embeddings[i][j].tolist() for j in range(compressed_embeddings[i].shape[0])]

    header_option = True if has_header else False
    final_df = metadata.reindex(columns=original_columns) if original_columns else metadata
    final_df.to_csv(output_file, index=False, header=header_option)
    print(f"Data saved to {output_file}.")


def run_veczip(input_file, output_file, target_dims=16):
    """Runs veczip compression on the input data."""
    data, embedding_columns, metadata_columns, has_header, original_columns = load_and_validate_embeddings(input_file, target_dims)

    all_embeddings = []
    for col in embedding_columns:
        embeddings = np.array([parse_as_array(x) for x in data[col].values])
        all_embeddings.append(embeddings)

    combined_embeddings = np.concatenate(all_embeddings, axis=0)
    compressor = veczip(target_dims=target_dims)
    retained_indices = compressor.compress(combined_embeddings)


    compressed_embeddings = []
    for embeddings in all_embeddings:
       compressed_embeddings.append(embeddings[:, retained_indices])



    save_compressed_embeddings(output_file, data[metadata_columns], compressed_embeddings, embedding_columns, original_columns, has_header)
    print("Veczip operation completed successfully.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py <input_file> <output_file> [target_dims]")
        sys.exit(1)
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    td = int(sys.argv[3]) if len(sys.argv) > 3 else 16
    run_veczip(input_path, output_path, td)