"""Extract compressed files (tar.gz, bz2, zip)."""

import tarfile
import bz2
import zipfile
from pathlib import Path
from typing import List


class Extractor:
    """Extract various compressed file formats."""

    def __init__(self, extract_dir: str = "tmp/extracted"):
        """Initialize extractor with target directory."""
        self.extract_dir = Path(extract_dir)
        self.extract_dir.mkdir(parents=True, exist_ok=True)

    def extract(self, filepath: Path) -> List[Path]:
        """
        Extract a compressed file.

        Args:
            filepath: Path to compressed file

        Returns:
            List of paths to extracted files/directories
        """
        filepath = Path(filepath)
        if not filepath.exists():
            raise FileNotFoundError(f"File not found: {filepath}")

        print(f"Extracting {filepath.name}...")

        extracted_paths = []

        try:
            if filepath.suffix == ".bz2":
                extracted_paths.extend(self._extract_bz2(filepath))
            elif filepath.suffixes == [".tar", ".gz"] or filepath.suffix == ".tgz":
                extracted_paths.extend(self._extract_tar(filepath))
            elif filepath.suffix == ".zip":
                extracted_paths.extend(self._extract_zip(filepath))
            elif filepath.suffix == ".csv":
                # CSV files don't need extraction, just copy
                import shutil
                dest = self.extract_dir / filepath.name
                shutil.copy(filepath, dest)
                extracted_paths.append(dest)
            else:
                print(f"  Unknown format, copying as-is")
                import shutil
                dest = self.extract_dir / filepath.name
                shutil.copy(filepath, dest)
                extracted_paths.append(dest)

            print(f"✓ Extracted to {self.extract_dir}")
            return extracted_paths

        except Exception as e:
            print(f"✗ Error extracting {filepath}: {e}")
            raise

    def _extract_bz2(self, filepath: Path) -> List[Path]:
        """Extract .bz2 file."""
        output_path = self.extract_dir / filepath.stem

        if filepath.stem.endswith(".tar"):
            # tar.bz2
            with tarfile.open(filepath, "r:bz2") as tar:
                tar.extractall(self.extract_dir)
                return [self.extract_dir / member.name for member in tar.getmembers()]
        else:
            # Plain bz2
            output_path = self.extract_dir / filepath.stem
            with open(output_path, "wb") as out_f:
                with bz2.open(filepath, "rb") as in_f:
                    out_f.write(in_f.read())
            return [output_path]

    def _extract_tar(self, filepath: Path) -> List[Path]:
        """Extract .tar.gz file."""
        extracted = []
        with tarfile.open(filepath, "r:gz") as tar:
            tar.extractall(self.extract_dir)
            extracted = [self.extract_dir / member.name for member in tar.getmembers()]
        return extracted

    def _extract_zip(self, filepath: Path) -> List[Path]:
        """Extract .zip file."""
        extracted = []
        with zipfile.ZipFile(filepath, "r") as zip_ref:
            zip_ref.extractall(self.extract_dir)
            extracted = [self.extract_dir / name for name in zip_ref.namelist()]
        return extracted

    def extract_all(self, filepaths: List[Path]) -> List[Path]:
        """
        Extract multiple files.

        Args:
            filepaths: List of paths to compressed files

        Returns:
            List of all extracted paths
        """
        all_extracted = []
        for filepath in filepaths:
            try:
                extracted = self.extract(filepath)
                all_extracted.extend(extracted)
            except Exception as e:
                print(f"Skipping {filepath}: {e}")
                continue

        return all_extracted
