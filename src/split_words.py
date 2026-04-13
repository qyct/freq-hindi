#!/home/workhill/PYENV/bin/python3
"""Split words.csv into smaller chunks."""

import csv
from pathlib import Path


def split_words_csv(input_file: str, output_dir: str, chunk_size: int = 3000):
    """
    Split words.csv into smaller files.

    Args:
        input_file: Path to words.csv
        output_dir: Directory to save chunk files
        chunk_size: Number of words per chunk
    """
    input_path = Path(input_file)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    print(f"Reading {input_file}...")

    with open(input_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)  # Save header

        words = []
        chunk_num = 1

        for row in reader:
            words.append(row)

            if len(words) >= chunk_size:
                # Write chunk
                output_file = output_path / f"hw{chunk_num:03d}.csv"
                with open(output_file, 'w', newline='', encoding='utf-8') as out:
                    writer = csv.writer(out)
                    writer.writerow(header)
                    writer.writerows(words)

                print(f"✓ Created {output_file.name} with {len(words)} words")
                words = []
                chunk_num += 1

        # Write remaining words
        if words:
            output_file = output_path / f"hw{chunk_num:03d}.csv"
            with open(output_file, 'w', newline='', encoding='utf-8') as out:
                writer = csv.writer(out)
                writer.writerow(header)
                writer.writerows(words)

            print(f"✓ Created {output_file.name} with {len(words)} words")

    print(f"\n✓ Total chunks created: {chunk_num}")
    print(f"✓ Output directory: {output_path}")


if __name__ == "__main__":
    import sys

    input_file = sys.argv[1] if len(sys.argv) > 1 else "words.csv"
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "words"

    split_words_csv(input_file, output_dir, chunk_size=3000)
