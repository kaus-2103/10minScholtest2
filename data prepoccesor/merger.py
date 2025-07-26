def merge_and_fix_numbers(file1_path, file2_path, output_path='data/merged_chunks.txt'):
    def read_chunks(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.readlines()

    # Read both files
    chunk1 = read_chunks('data/important_chunk_passage.txt')
    chunk2 = read_chunks('data/important_chunk_table.txt')

    # Merge chunks
    merged = chunk1 + chunk2

    # Fix numbering (assumes lines start with a number and a dot, e.g., "1. ...")
    fixed = []
    for idx, line in enumerate(merged, start=1):
        # Remove existing numbering if present
        parts = line.strip().split('.', 1)
        if len(parts) == 2 and parts[0].isdigit():
            content = parts[1].strip()
        else:
            content = line.strip()
        fixed.append(f"{idx}. {content}\n")

    # Write to output file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(fixed)

# Example usage:
# merge_and_fix_numbers('chunk1.txt', 'chunk2.txt', 'merged.txt')