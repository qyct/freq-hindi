"""Process Hindi text and compute word frequencies."""

import re
import csv
from pathlib import Path
from typing import Dict, List
from collections import Counter
import xml.etree.ElementTree as ET


class HindiProcessor:
    """Process Hindi text for word frequency analysis."""

    def __init__(self):
        """Initialize processor."""
        # Common Hindi vowel signs (matras) and modifiers
        self.hindi_range = (0x0900, 0x097F)  # Unicode range for Devanagari

    def is_hindi_char(self, char: str) -> bool:
        """Check if character is in Hindi/Devanagari Unicode range."""
        code = ord(char)
        return self.hindi_range[0] <= code <= self.hindi_range[1]

    def clean_text(self, text: str) -> str:
        """
        Clean text by removing non-Hindi characters and punctuation.

        Args:
            text: Raw text input

        Returns:
            Cleaned Hindi text
        """
        # Replace purna viram, deergha viram, and visarga with space
        text = re.sub(r'[।॥ः]+', ' ', text)

        # Keep only Hindi characters and spaces
        cleaned = ""
        for char in text:
            if self.is_hindi_char(char) or char.isspace():
                cleaned += char
        return cleaned

    def tokenize(self, text: str) -> List[str]:
        """
        Tokenize Hindi text into words.

        Args:
            text: Hindi text

        Returns:
            List of words
        """
        # Split on whitespace and filter empty strings
        words = text.split()
        return [word for word in words if word]

    def process_file(self, filepath: Path) -> Dict[str, int]:
        """
        Process a single file and return word frequencies.

        Args:
            filepath: Path to text file

        Returns:
            Dictionary mapping words to frequencies
        """
        filepath = Path(filepath)

        if not filepath.exists():
            print(f"  File not found: {filepath}")
            return {}

        print(f"  Processing {filepath.name}...")

        counter = Counter()

        try:
            if filepath.suffix == ".xml":
                counter.update(self._process_xml(filepath))
            elif filepath.suffix == ".csv":
                counter.update(self._process_csv(filepath))
            elif filepath.suffix == ".txt" or filepath.suffix == "":
                counter.update(self._process_text(filepath))
            elif filepath.suffix == ".parquet":
                counter.update(self._process_parquet(filepath))
            else:
                print(f"    Skipping unsupported format: {filepath.suffix}")

        except Exception as e:
            print(f"    Error processing {filepath}: {e}")

        return dict(counter)

    def _process_xml(self, filepath: Path) -> Dict[str, int]:
        """Process XML file (e.g., Wikipedia dump)."""
        counter = Counter()

        try:
            # For large XML files, use iterative parsing
            print(f"    Parsing XML (this may take a while)...")
            context = ET.iterparse(str(filepath), events=("start", "end"))

            text_content = []
            for event, elem in context:
                if event == "end" and elem.text:
                    text_content.append(elem.text)
                    elem.clear()  # Clear to save memory

            combined_text = " ".join(text_content)
            words = self._extract_words_from_text(combined_text)
            counter.update(words)

        except Exception as e:
            print(f"    XML parsing error: {e}")

        return dict(counter)

    def _process_csv(self, filepath: Path) -> Dict[str, int]:
        """Process CSV file."""
        counter = Counter()

        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                reader = csv.reader(f)
                for row in reader:
                    text = " ".join(row)
                    words = self._extract_words_from_text(text)
                    counter.update(words)

        except Exception as e:
            print(f"    CSV reading error: {e}")

        return dict(counter)

    def _process_text(self, filepath: Path) -> Dict[str, int]:
        """Process plain text file."""
        counter = Counter()

        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
                words = self._extract_words_from_text(text)
                counter.update(words)

        except Exception as e:
            print(f"    Text reading error: {e}")

        return dict(counter)

    def _process_parquet(self, filepath: Path) -> Dict[str, int]:
        """Process Parquet file (HuggingFace format)."""
        counter = Counter()

        try:
            import pyarrow.parquet as pq

            print(f"    Reading parquet file...")
            table = pq.read_table(filepath)
            df = table.to_pandas()

            # Look for text column
            text_column = None
            for col in ['text', 'content', 'data']:
                if col in df.columns:
                    text_column = col
                    break

            if text_column:
                print(f"    Processing {len(df)} rows...")
                combined_text = " ".join(df[text_column].fillna('').astype(str).tolist())
                words = self._extract_words_from_text(combined_text)
                counter.update(words)
            else:
                print(f"    No text column found in {filepath}")

        except ImportError:
            print(f"    PyArrow not installed, skipping parquet file")
        except Exception as e:
            print(f"    Parquet reading error: {e}")

        return dict(counter)

    def _extract_words_from_text(self, text: str) -> List[str]:
        """Extract and count words from text."""
        cleaned = self.clean_text(text)
        return self.tokenize(cleaned)

    def process_directory(self, directory: Path) -> Dict[str, int]:
        """
        Process all files in a directory.

        Args:
            directory: Path to directory

        Returns:
            Combined word frequency dictionary
        """
        directory = Path(directory)
        if not directory.exists():
            return {}

        total_counter = Counter()
        file_count = 0

        # Process all text-based files
        for filepath in directory.rglob("*"):
            if filepath.is_file() and not filepath.name.startswith("."):
                freq = self.process_file(filepath)
                total_counter.update(freq)
                file_count += 1

        print(f"\nProcessed {file_count} files")
        print(f"Found {len(total_counter)} unique words")

        return dict(total_counter)

    def save_frequencies(self, frequencies: Dict[str, int], output_path: str = "words.txt"):
        """
        Save word frequencies to text file.

        Args:
            frequencies: Dictionary of word -> frequency
            output_path: Path to output text file
        """
        # Sort by frequency (descending)
        sorted_freq = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)

        with open(output_path, "w", encoding="utf-8") as f:
            for word, freq in sorted_freq:
                f.write(f"{word},{freq}\n")

        print(f"\n✓ Saved {len(sorted_freq)} words to {output_path}")

    def save_checkpoint(self, frequencies: Dict[str, int], checkpoint_path: str = "tmp/checkpoint.pkl"):
        """
        Save processing checkpoint for resume support.

        Args:
            frequencies: Dictionary of word -> frequency
            checkpoint_path: Path to checkpoint file
        """
        import pickle

        checkpoint_dir = Path(checkpoint_path).parent
        checkpoint_dir.mkdir(parents=True, exist_ok=True)

        with open(checkpoint_path, "wb") as f:
            pickle.dump(frequencies, f)

        print(f"  ✓ Saved checkpoint ({len(frequencies):,} words)")

    def load_checkpoint(self, checkpoint_path: str = "tmp/checkpoint.pkl") -> Dict[str, int]:
        """
        Load processing checkpoint for resume support.

        Args:
            checkpoint_path: Path to checkpoint file

        Returns:
            Dictionary of word -> frequency, or empty dict if not found
        """
        import pickle

        checkpoint_file = Path(checkpoint_path)
        if not checkpoint_file.exists():
            return {}

        try:
            with open(checkpoint_path, "rb") as f:
                frequencies = pickle.load(f)

            print(f"  ✓ Loaded checkpoint ({len(frequencies):,} words)")
            return frequencies
        except Exception as e:
            print(f"  ✗ Could not load checkpoint: {e}")
            return {}

    def merge_frequencies(self, *freq_dicts: Dict[str, int]) -> Dict[str, int]:
        """
        Merge multiple frequency dictionaries.

        Args:
            *freq_dicts: Variable number of frequency dictionaries

        Returns:
            Merged dictionary with summed frequencies
        """
        merged = Counter()
        for freq_dict in freq_dicts:
            merged.update(freq_dict)
        return dict(merged)
