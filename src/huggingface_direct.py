"""Direct file download from HuggingFace repositories."""

from pathlib import Path
from huggingface_hub import hf_hub_download


class HuggingFaceDirect:
    """Download files directly from HuggingFace repositories."""

    def __init__(self, output_dir: str = "tmp/huggingface"):
        """Initialize downloader with target directory."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def download_file(self, repo_id: str, filename: str):
        """
        Download a single file from a HuggingFace repository.

        Args:
            repo_id: Repository ID (e.g., "ai4bharat/IndicCorpV2")
            filename: Filename to download

        Returns:
            Path to downloaded file
        """
        print(f"Downloading {filename} from {repo_id}...")

        try:
            filepath = hf_hub_download(
                repo_id=repo_id,
                filename=filename,
                repo_type="dataset",
                local_dir=self.output_dir / repo_id.replace("/", "_"),
                local_dir_use_symlinks=False
            )

            print(f"✓ Downloaded to {filepath}")
            return Path(filepath)

        except Exception as e:
            print(f"✗ Error downloading: {e}")
            return None


if __name__ == "__main__":
    # Test with some known Hindi datasets
    downloader = HuggingFaceDirect()

    # Try to download from ai4bharat/IndicCorpV2
    print("Testing IndicCorpV2...")
    # Note: Need to know the exact filename structure
    print("Repository files need to be checked at:")
    print("https://huggingface.co/datasets/ai4bharat/IndicCorpV2/tree/main")
