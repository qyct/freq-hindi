#!/home/workhill/PYENV/bin/python3
"""Main script to download and process Hindi corpus for word frequency analysis."""

import argparse
from pathlib import Path
from collections import Counter

from src.downloader import Downloader
from src.extractor import Extractor
from src.processor import HindiProcessor
from src.sources import HindiSources


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Download and process Hindi corpus for word frequency analysis"
    )
    parser.add_argument(
        "--skip-download",
        action="store_true",
        help="Skip downloading if files already exist"
    )
    parser.add_argument(
        "--skip-extract",
        action="store_true",
        help="Skip extraction if already extracted"
    )
    parser.add_argument(
        "--output",
        default="words.txt",
        help="Output file path (default: words.txt)"
    )
    parser.add_argument(
        "--data-dir",
        default="tmp/extracted",
        help="Directory containing extracted data (default: tmp/extracted)"
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Resume from checkpoint if available"
    )
    parser.add_argument(
        "--no-checkpoint",
        action="store_true",
        help="Disable checkpoint saving"
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Hindi Word Frequency Analysis")
    print("=" * 60)

    # Step 1: Download
    if not args.skip_download:
        print("\n[Step 1/3] Downloading corpus files...")
        downloader = Downloader()
        try:
            downloaded = downloader.download_all(HindiSources.get_all_download_urls())
            print(f"✓ Downloaded {len(downloaded)} file(s)")
        except Exception as e:
            print(f"✗ Download failed: {e}")
            return 1
    else:
        print("\n[Step 1/3] Skipping download (--skip-download)")

    # Step 2: Extract
    if not args.skip_extract:
        print("\n[Step 2/3] Extracting compressed files...")
        extractor = Extractor()
        download_dir = Path("tmp/downloads")

        if not download_dir.exists():
            print(f"✗ Download directory not found: {download_dir}")
            print("  Run without --skip-download first")
            return 1

        files_to_extract = list(download_dir.glob("*"))
        if not files_to_extract:
            print("✗ No files to extract")
            return 1

        try:
            extractor.extract_all(files_to_extract)
        except Exception as e:
            print(f"✗ Extraction failed: {e}")
            return 1
    else:
        print("\n[Step 2/3] Skipping extraction (--skip-extract)")

    # Step 3: Process
    print("\n[Step 3/3] Processing text and counting word frequencies...")
    processor = HindiProcessor()

    # Try to load checkpoint if resume is enabled
    total_frequencies = {}
    if args.resume:
        checkpoint_path = "tmp/processing_checkpoint.pkl"
        total_frequencies = processor.load_checkpoint(checkpoint_path)
        if total_frequencies:
            print(f"\nResuming from checkpoint...")
        else:
            print(f"\nNo checkpoint found, starting fresh...")

    # Process all data directories
    data_dir = Path(args.data_dir)
    hf_dir = Path("tmp/huggingface")
    gh_dir = Path("tmp/github")

    if not data_dir.exists() and not hf_dir.exists() and not gh_dir.exists():
        print(f"✗ No data directories found")
        print("  Run without --skip-extract first")
        return 1

    checkpoint_enabled = not args.no_checkpoint
    checkpoint_path = "tmp/processing_checkpoint.pkl"

    # Process extracted directory
    if data_dir.exists():
        print(f"\nProcessing {data_dir}...")
        frequencies = processor.process_directory(data_dir)
        total_frequencies = processor.merge_frequencies(total_frequencies, frequencies)
        if checkpoint_enabled:
            processor.save_checkpoint(total_frequencies, checkpoint_path)

    # Process huggingface directory
    if hf_dir.exists():
        print(f"\nProcessing {hf_dir}...")
        frequencies = processor.process_directory(hf_dir)
        total_frequencies = processor.merge_frequencies(total_frequencies, frequencies)
        if checkpoint_enabled:
            processor.save_checkpoint(total_frequencies, checkpoint_path)

    # Process github directory
    if gh_dir.exists():
        print(f"\nProcessing {gh_dir}...")
        frequencies = processor.process_directory(gh_dir)
        total_frequencies = processor.merge_frequencies(total_frequencies, frequencies)
        if checkpoint_enabled:
            processor.save_checkpoint(total_frequencies, checkpoint_path)

    if not total_frequencies:
        print("✗ No word frequencies found")
        return 1

    # Combine frequencies from multiple sources
    combined = Counter(total_frequencies)

    processor.save_frequencies(dict(combined), args.output)

    print("\n" + "=" * 60)
    print("✓ Complete!")
    print(f"  Output: {args.output}")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    exit(main())
