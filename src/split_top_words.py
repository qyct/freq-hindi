#!/home/workhill/PYENV/bin/python3
"""Split top 30,000 words by frequency into 10 txt files (hw01.txt to hw10.txt)."""

from pathlib import Path


def split_top_words(input_file: str = "words.txt", output_dir: str = "words"):
    """
    Split top 30,000 words (sorted by frequency descending) into 10 files.

    Args:
        input_file: Path to words.txt
        output_dir: Directory to save chunk files
    """
    input_path = Path(input_file)
    output_path = Path(output_dir)

    # Remove existing words directory
    if output_path.exists():
        print(f"Removing existing {output_path}...")
        import shutil
        shutil.rmtree(output_path)

    output_path.mkdir(parents=True, exist_ok=True)

    print(f"Reading {input_file}...")

    words = []
    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            if ',' in line:
                word, freq = line.strip().rsplit(',', 1)
                words.append((word, int(freq)))

    print(f"Total words read: {len(words):,}")

    # Sort by frequency descending
    print("Sorting by frequency (highest first)...")
    words.sort(key=lambda x: x[1], reverse=True)

    # Take top 30,000
    top_words = words[:30000]
    print(f"Top 30,000 words: {top_words[0][0]} (freq: {top_words[0][1]:,}) to {top_words[-1][0]} (freq: {top_words[-1][1]:,})")

    # Split into 10 files of 3000 words each
    chunk_size = 3000
    for i in range(10):
        start_idx = i * chunk_size
        end_idx = start_idx + chunk_size
        chunk = top_words[start_idx:end_idx]

        output_file = output_path / f"hw{i+1:02d}.txt"

        with open(output_file, 'w', encoding='utf-8') as out:
            for word, freq in chunk:
                out.write(f"{word},{freq}\n")

        print(f"✓ Created {output_file.name} with {len(chunk)} words (freq: {chunk[0][1]:,} to {chunk[-1][1]:,})")

    print(f"\n✓ Total files created: 10")
    print(f"✓ Total words: {len(top_words):,}")
    print(f"✓ Output directory: {output_path}")


if __name__ == "__main__":
    split_top_words()
