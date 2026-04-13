"""Download datasets from HuggingFace."""

import os
from pathlib import Path
from datasets import load_dataset


class HuggingFaceDownloader:
    """Download Hindi datasets from HuggingFace."""

    def __init__(self, output_dir: str = "tmp/huggingface"):
        """Initialize downloader with target directory."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def download_oscar_hindi(self, split: str = "train", max_samples: int = None):
        """
        Download OSCAR Hindi dataset.

        Args:
            split: Dataset split to download
            max_samples: Maximum number of samples to download (None for all)

        Returns:
            Path to saved text file
        """
        print("Downloading OSCAR Hindi dataset from HuggingFace...")
        print("This may take a while...")

        try:
            # Download OSCAR Hindi dataset
            dataset = load_dataset("oscar", "unshuffled_deduplicated_hi", split=split)

            if max_samples:
                dataset = dataset.select(range(min(max_samples, len(dataset))))

            # Save to text file
            output_file = self.output_dir / "oscar_hindi.txt"
            with open(output_file, "w", encoding="utf-8") as f:
                for item in dataset:
                    if "text" in item:
                        f.write(item["text"] + "\n")

            print(f"✓ Downloaded {len(dataset)} samples to {output_file}")
            return output_file

        except Exception as e:
            print(f"✗ Error downloading OSCAR: {e}")
            return None

    def download_mc4_hindi(self, split: str = "train", max_samples: int = None):
        """
        Download MC4 Hindi dataset.

        Args:
            split: Dataset split to download
            max_samples: Maximum number of samples to download (None for all)

        Returns:
            Path to saved text file
        """
        print("Downloading MC4 Hindi dataset from HuggingFace...")
        print("This may take a while...")

        try:
            # Download MC4 Hindi dataset
            dataset = load_dataset("mc4", "hi", split=split)

            if max_samples:
                dataset = dataset.select(range(min(max_samples, len(dataset))))

            # Save to text file
            output_file = self.output_dir / "mc4_hindi.txt"
            with open(output_file, "w", encoding="utf-8") as f:
                for item in dataset:
                    if "text" in item:
                        f.write(item["text"] + "\n")

            print(f"✓ Downloaded {len(dataset)} samples to {output_file}")
            return output_file

        except Exception as e:
            print(f"✗ Error downloading MC4: {e}")
            return None


if __name__ == "__main__":
    # Test download
    downloader = HuggingFaceDownloader()

    # Download small sample first
    print("Downloading small sample of OSCAR Hindi...")
    downloader.download_oscar_hindi(max_samples=1000)

    print("\nDownloading small sample of MC4 Hindi...")
    downloader.download_mc4_hindi(max_samples=1000)
