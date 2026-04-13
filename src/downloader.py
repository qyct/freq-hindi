"""Download Hindi corpus files from various sources."""

import requests
from typing import List
from pathlib import Path


class Downloader:
    """Download files from URLs with progress tracking."""

    def __init__(self, download_dir: str = "tmp/downloads"):
        """Initialize downloader with target directory."""
        self.download_dir = Path(download_dir)
        self.download_dir.mkdir(parents=True, exist_ok=True)

    def download(self, url: str, filename: str = None) -> Path:
        """
        Download a file from URL.

        Args:
            url: URL to download from
            filename: Optional filename to save as. If not provided, extracted from URL.

        Returns:
            Path to downloaded file
        """
        if filename is None:
            filename = url.split("/")[-1]
            if "?" in filename:
                filename = filename.split("?")[0]

        filepath = self.download_dir / filename

        print(f"Downloading {url}...")
        print(f"Saving to {filepath}...")

        try:
            response = requests.get(url, stream=True, timeout=300)
            response.raise_for_status()

            total_size = int(response.headers.get("content-length", 0))

            with open(filepath, "wb") as f:
                if total_size > 0:
                    downloaded = 0
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            if downloaded % (1024 * 1024) == 0:  # Every MB
                                mb = downloaded / (1024 * 1024)
                                total_mb = total_size / (1024 * 1024)
                                print(f"  Progress: {mb:.1f}MB / {total_mb:.1f}MB")
                else:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)

            print(f"✓ Downloaded to {filepath}")
            return filepath

        except Exception as e:
            print(f"✗ Error downloading {url}: {e}")
            if filepath.exists():
                filepath.unlink()
            raise

    def download_all(self, urls: List[str]) -> List[Path]:
        """
        Download all files from list of URLs.

        Args:
            urls: List of URLs to download

        Returns:
            List of paths to downloaded files
        """
        downloaded = []

        for url in urls:
            try:
                filepath = self.download(url)
                downloaded.append(filepath)
            except Exception as e:
                print(f"Skipping {url} due to error: {e}")
                continue

        return downloaded
