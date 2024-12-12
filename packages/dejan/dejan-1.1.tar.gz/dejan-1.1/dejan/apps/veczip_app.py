from dejan.veczip import veczip
import pandas as pd
import numpy as np
import csv
import ast
import sys

def is_numeric(s):
    try:
        float(s)
        return True
    except:
        return False

def parse_as_array(val):
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
    try:
        nums = [int(float(v)) for v in col_values]
        return nums == list(range(nums[0], nums[0] + len(nums)))
    except:
        return False

def detect_columns(file_path):
    raw_lines = []
    with open(file_path, "r", newline="", encoding="utf-8") as f:
        for _ in range(10):
            pos = f.tell()
            line = f.readline()
            if not line:
                break
            raw_lines.append(line)
        f.seek(0)

        try:
            sample = ''.join(raw_lines)
            dialect = csv.Sniffer().sniff(sample, delimiters=[',','\t',';','|'])
            delimiter = dialect.delimiter
        except:
            delimiter = ','

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
    print(f"Loading data from {input_file}...")
    has_header, embedding_columns, metadata_columns, delimiter = detect_columns(input_file)
    data = pd.read_csv(input_file, header=0 if has_header else None, delimiter=delimiter)

    def to_uniform_array(row):
        arrays = []
        for c in embedding_columns:
            arr = parse_as_array(row[c])
            if arr is None:
                return None
            arrays.append(arr)
        return np.hstack(arrays)

    embeddings_list = data.apply(to_uniform_array, axis=1)
    data = data[embeddings_list.notnull()]
    embeddings = np.vstack(embeddings_list.dropna().values)
    metadata = data[metadata_columns]

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

    return embeddings, metadata, embedding_columns, list(data.columns), has_header

def save_compressed_embeddings(output_file, metadata, compressed_embeddings, embedding_columns, original_columns, has_header):
    print(f"Saving compressed data to {output_file}...")
    num_embedding_cols = len(embedding_columns)
    total_dims = compressed_embeddings.shape[1]
    if total_dims % num_embedding_cols != 0:
        raise ValueError("Compressed dimensions cannot be evenly split across embedding columns.")
    split_size = total_dims // num_embedding_cols

    for i, col in enumerate(embedding_columns):
        start_idx = i * split_size
        end_idx = (i + 1) * split_size
        metadata[col] = [
            compressed_embeddings[j, start_idx:end_idx].tolist() for j in range(compressed_embeddings.shape[0])
        ]

    # If source had no header, write no header
    header_option = True if has_header else False
    final_df = metadata.reindex(columns=original_columns) if original_columns else metadata
    final_df.to_csv(output_file, index=False, header=header_option)
    print(f"Data saved to {output_file}.")

def run_veczip(input_file, output_file, target_dims=16):
    embeddings, metadata, embedding_columns, original_columns, has_header = load_and_validate_embeddings(input_file, target_dims)
    compressor = veczip(target_dims=target_dims)
    compressed_embeddings, retained_indices = compressor.compress(embeddings)
    save_compressed_embeddings(output_file, metadata, compressed_embeddings, embedding_columns, original_columns, has_header)
    print("Veczip operation completed successfully.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py <input_file> <output_file> [target_dims]")
        sys.exit(1)
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    td = int(sys.argv[3]) if len(sys.argv) > 3 else 16
    run_veczip(input_path, output_path, td)
