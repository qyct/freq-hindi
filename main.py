#!/home/workhill/PYENV/bin/python3
"""Main script to download and process Hindi corpus for word frequency analysis."""

import argparse
from pathlib import Path

from src.downloader import Downloader
from src.extractor import Extractor
from src.processor import HindiProcessor
from src.sources import SOURCES


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
        default="words.csv",
        help="Output CSV file path (default: words.csv)"
    )
    parser.add_argument(
        "--data-dir",
        default="tmp/extracted",
        help="Directory containing extracted data (default: tmp/extracted)"
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
            downloaded = downloader.download_all(SOURCES)
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

    data_dir = Path(args.data_dir)
    if not data_dir.exists():
        print(f"✗ Data directory not found: {data_dir}")
        print("  Run without --skip-extract first")
        return 1

    frequencies = processor.process_directory(data_dir)

    if not frequencies:
        print("✗ No word frequencies found")
        return 1

    processor.save_frequencies(frequencies, args.output)

    print("\n" + "=" * 60)
    print("✓ Complete!")
    print(f"  Output: {args.output}")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    exit(main())
