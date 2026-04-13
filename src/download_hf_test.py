#!/home/workhill/PYENV/bin/python3
"""Test downloading from public HuggingFace datasets without authentication."""

from pathlib import Path
from huggingface_hub import hf_hub_download, list_repo_files
import sys


def try_download_dataset(dataset_name, file_pattern=None):
    """Try to download from a public HuggingFace dataset."""
    print(f"\n{'='*60}")
    print(f"Trying: {dataset_name}")
    print(f"{'='*60}")

    output_dir = Path("tmp/huggingface")
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        # List files in the repository
        print(f"Listing files in {dataset_name}...")
        files = list_repo_files(dataset_name, repo_type="dataset")
        print(f"Found {len(files)} files")

        # Filter for relevant files
        relevant_files = []
        for f in files:
            if file_pattern:
                if file_pattern in f:
                    relevant_files.append(f)
            elif any(ext in f for ext in ['.txt', '.csv', '.json', '.parquet', '.tar.gz', '.gz']):
                # Skip very small files
                if not any(skip in f for skip in ['README', 'LICENSE', '.gitignore']):
                    relevant_files.append(f)

        print(f"Relevant files: {len(relevant_files)}")
        for f in relevant_files[:10]:  # Show first 10
            print(f"  - {f}")

        if relevant_files:
            # Download first relevant file
            file_to_download = relevant_files[0]
            print(f"\nDownloading: {file_to_download}")

            filepath = hf_hub_download(
                repo_id=dataset_name,
                filename=file_to_download,
                repo_type="dataset",
                local_dir=output_dir / dataset_name.replace("/", "_"),
                local_dir_use_symlinks=False
            )

            print(f"✓ Downloaded to: {filepath}")
            return filepath

        else:
            print("✗ No suitable files found")
            return None

    except Exception as e:
        print(f"✗ Error: {e}")
        return None


def main():
    """Try multiple public HuggingFace Hindi datasets."""

    # Public datasets to try (no authentication required)
    datasets = [
        ("ai4bharat/sangraha", "hi"),
        ("crowdlab/crowdask_hindi", None),
        ("rahular/electricity_hindi", None),
        ("mosesmlab/iitb-hindi-eng", None),
    ]

    print("Attempting to download from public HuggingFace datasets...")
    print("No authentication required for these datasets.\n")

    downloaded = []

    for dataset_name, pattern in datasets:
        result = try_download_dataset(dataset_name, pattern)
        if result:
            downloaded.append(result)

    print(f"\n{'='*60}")
    print(f"Summary: Downloaded {len(downloaded)} file(s)")
    print(f"{'='*60}")

    if downloaded:
        print("\nDownloaded files:")
        for f in downloaded:
            print(f"  - {f}")

    return len(downloaded) > 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
