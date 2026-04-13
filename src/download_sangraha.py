#!/home/workhill/PYENV/bin/python3
"""Download multiple files from ai4bharat/sangraha dataset."""

from pathlib import Path
from huggingface_hub import hf_hub_download
from concurrent.futures import ThreadPoolExecutor, as_completed
import time


def download_parquet_file(dataset_name, file_path, output_dir):
    """Download a single parquet file."""
    try:
        filepath = hf_hub_download(
            repo_id=dataset_name,
            filename=file_path,
            repo_type="dataset",
            local_dir=output_dir,
            local_dir_use_symlinks=False
        )
        return filepath
    except Exception as e:
        print(f"✗ Error downloading {file_path}: {e}")
        return None


def main():
    """Download Hindi Wikipedia files from sangraha dataset."""
    dataset_name = "ai4bharat/sangraha"
    output_dir = Path("tmp/huggingface/ai4bharat_sangraha")
    output_dir.mkdir(parents=True, exist_ok=True)

    print("Downloading Hindi Wikipedia files from ai4bharat/sangraha...")
    print("This dataset has 63 parquet files (~500MB each)")
    print("\nDownloading first 5 files (this may take a while)...\n")

    # Download first 5 files
    files_to_download = [
        f"synthetic/hin_Deva/wiki_hin_Deva_{i:04d}_of_0063.parquet"
        for i in range(5)
    ]

    downloaded = []
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {
            executor.submit(download_parquet_file, dataset_name, file_path, output_dir): file_path
            for file_path in files_to_download
        }

        for future in as_completed(futures):
            file_path = futures[future]
            try:
                result = future.result()
                if result:
                    downloaded.append(result)
                    print(f"✓ Downloaded {file_path}")
            except Exception as e:
                print(f"✗ Failed {file_path}: {e}")

    elapsed = time.time() - start_time

    print(f"\n{'='*60}")
    print(f"Downloaded {len(downloaded)} files in {elapsed:.1f}s")
    print(f"{'='*60}")

    if downloaded:
        print(f"\nFiles are in: {output_dir}")
        return 0
    else:
        print("\n✗ No files downloaded")
        return 1


if __name__ == "__main__":
    exit(main())
