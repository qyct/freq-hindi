#!/home/workhill/PYENV/bin/python3
"""Download and process GitHub sources for Hindi word frequency."""

import requests
from pathlib import Path
from typing import List


class GitHubDownloader:
    """Download files from GitHub repositories."""

    def __init__(self, download_dir: str = "tmp/github"):
        """Initialize downloader with target directory."""
        self.download_dir = Path(download_dir)
        self.download_dir.mkdir(parents=True, exist_ok=True)

    def download(self, url: str) -> Path:
        """
        Download a file from GitHub.

        Args:
            url: URL to download from

        Returns:
            Path to downloaded file
        """
        filename = url.split("/")[-1]
        # Remove URL encoding
        filename = filename.replace("%20", "_")
        filepath = self.download_dir / filename

        print(f"Downloading {filename}...")

        try:
            response = requests.get(url, timeout=120)
            response.raise_for_status()

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(response.text)

            print(f"✓ Downloaded to {filepath} ({len(response.text):,} chars)")
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


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent))

    from src.github_sources import GITHUB_SOURCES

    print("=" * 60)
    print("GitHub Hindi Corpus Sources")
    print("=" * 60)

    downloader = GitHubDownloader()
    downloaded = downloader.download_all(GITHUB_SOURCES)

    print(f"\n✓ Downloaded {len(downloaded)} file(s)")
    print(f"  Location: {downloader.download_dir}")
