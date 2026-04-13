# Hindi Word Frequency Analysis

Download and process Hindi corpus files to generate word frequency statistics.

## Overview

This project downloads Hindi text from multiple sources (Wikipedia, Leipzig corpora, HuggingFace datasets, GitHub repositories), processes the text to remove non-Hindi characters and punctuation, and generates a comprehensive word frequency list sorted by occurrence count.

## Structure

```
.
├── main.py                    # Main entry point (uses ~/PYENV)
├── words.txt                  # Output file - 3.66M+ unique words (word,freq format)
├── requirements.txt           # Python dependencies
├── .gitignore                 # Excludes tmp/, words.txt
├── words/                     # Top 30,000 words split into 10 files
│   ├── hw01.txt              # Words 1-3000 (highest frequency)
│   ├── hw02.txt              # Words 3001-6000
│   └── ...                   # ... hw10.txt (words 27001-30000)
└── src/                      # Helper modules
    ├── __init__.py           # Package init
    ├── sources.py            # Data source URLs (object-oriented)
    ├── downloader.py         # Download files from URLs
    ├── extractor.py          # Extract compressed files (.tar.gz, .bz2)
    ├── processor.py          # Process text & count frequencies
    └── split_top_words.py    # Split top 30K words into chunks
```

## Installation

Install dependencies using ~/PYENV:
```bash
~/PYENV/bin/pip install -r requirements.txt
```

Required packages:
- `requests` - HTTP downloads
- `beautifulsoup4` - HTML parsing
- `pyarrow` - Parquet file processing (HuggingFace datasets)
- `datasets` - HuggingFace datasets access

## Usage

### Full Pipeline (download + extract + process)
```bash
~/PYENV/bin/python3 main.py
```

### Resume from Checkpoint
```bash
~/PYENV/bin/python3 main.py --resume
```
Saves progress to `tmp/processing_checkpoint.pkl` after each directory. Can resume if interrupted.

### Skip Steps
```bash
# Skip download (if tmp/downloads exists)
~/PYENV/bin/python3 main.py --skip-download

# Skip extraction (if tmp/extracted, tmp/huggingface, tmp/github exist)
~/PYENV/bin/python3 main.py --skip-extract

# Skip both (just process existing data)
~/PYENV/bin/python3 main.py --skip-download --skip-extract
```

### Custom Output Location
```bash
~/PYENV/bin/python3 main.py --output my_words.txt
```

### Generate Top 30,000 Split Files
```bash
~/PYENV/bin/python3 src/split_top_words.py
```
Creates `hw01.txt` to `hw10.txt` in `words/` folder (3000 words each).

## Data Sources

Currently configured (in `src/sources.py`):

### 1. **WIKIPEDIA** (Wikimedia Hindi Dumps)
- URL: `https://dumps.wikimedia.org/hiwiki/latest/hiwiki-latest-pages-articles.xml.bz2`
- Size: 224 MB → 1.6 GB extracted
- Content: All Hindi Wikipedia articles
- Best for: Formal, encyclopedic content
- Type: `download`

### 2. **LEIPZIG_2019** (Leipzig Hindi Corpora)
- URL: `https://downloads.wortschatz-leipzig.de/corpora/hin_mixed_2019_1M.tar.gz`
- Size: 218 MB compressed
- Content: 1M randomized sentences from web sources
- Best for: Balanced frequency analysis
- Type: `download`

### 3. **HUGGINGFACE_SANGRAHA** (AI4Bharat Sangraha Dataset)
- Repository: `ai4bharat/sangraha`
- Content: Diverse Hindi text corpus
- Best for: Modern Hindi text from multiple domains
- Type: `huggingface` (no authentication required)

### 4. **GITHUB_GAYATRI** (Hindi Stop Lemmas)
- URL: `https://raw.githubusercontent.com/gayatrivenugopal/hindi-corpus-stoplemmas/master/final%20stop%20lemma%20list.txt`
- Size: 4.8 KB
- Content: Hindi stop words and lemmas
- Type: `github` (raw file download)

### 5. **GITHUB_HUNSPELL** (Hindi Hunspell Dictionary)
- URL: `https://raw.githubusercontent.com/Shreeshrii/hindi-hunspell/master/Hindi/hi_IN.txt`
- Size: 11 MB
- Content: Hindi dictionary words
- Best for: Correct word forms and spellings
- Type: `github` (raw file download)

**Temporary files:** Stored in `tmp/` directory
- `tmp/downloads/` - Downloaded compressed files
- `tmp/extracted/` - Wikipedia and Leipzig extracted data
- `tmp/huggingface/` - Sangraha dataset files
- `tmp/github/` - Downloaded GitHub files
- `tmp/processing_checkpoint.pkl` - Resume checkpoint

## Current Statistics

- **Total unique words:** 3,664,322
- **Sources processed:** 5 (Wikipedia + Leipzig + HuggingFace + 2 GitHub)
- **Text cleaning:**
  - ✅ Removes purna viram (।) and deergha viram (॥)
  - ✅ Removes visarga (ः) character
  - ✅ Only keeps Devanagari Unicode range (0x0900-0x097F)
  - ✅ Splits on whitespace
  - ✅ No length filtering (keeps short words like के, में, है)

## Top 20 Words by Frequency

| Rank | Word | Frequency | Meaning |
|------|------|-----------|---------|
| 1 | के | 17,346,039 | of (masc) |
| 2 | में | 13,225,211 | in |
| 3 | और | 7,953,249 | and |
| 4 | है | 7,154,672 | is |
| 5 | की | 6,820,037 | of (fem) |
| 6 | को | 5,455,303 | to |
| 7 | से | 5,440,468 | from |
| 8 | एक | 4,941,024 | one |
| 9 | का | 4,349,977 | of (masc) |
| 10 | किया | 3,168,557 | did |
| 11 | पर | 3,085,114 | on |
| 12 | ने | 2,597,406 | by (past tense marker) |
| 13 | भी | 2,237,581 | also |
| 14 | लिए | 2,167,606 | for |
| 15 | कि | 2,009,241 | that |
| 16 | गया | 1,860,297 | went |
| 17 | था | 1,804,699 | was |
| 18 | यह | 1,752,204 | this |
| 19 | वह | 1,718,282 | he/that |
| 20 | हैं | 1,692,882 | are |

## Output Format

### words.txt (main output)
Format: `word,frequency` (comma-separated, no header)
```
के,17346039
में,13225211
और,7953249
...
```

### words/hw01.txt to hw10.txt (top 30,000 split)
Format: `word,frequency` (comma-separated, no header)
- `hw01.txt`: Words 1-3000 (freq: 17,346,039 → 10,011)
- `hw02.txt`: Words 3001-6000 (freq: 10,011 → 3,931)
- ...
- `hw10.txt`: Words 27001-30000 (freq: 369 → 312)

## Technical Decisions

### 1. **Output Format: TXT instead of CSV**
- Decision: Changed from CSV to comma-separated TXT
- Reason: Simpler format, easier to parse, no header row
- Format: `word,frequency\n` (one word per line)

### 2. **Text Cleaning: Remove Visarga**
- Decision: Remove visarga (ः) character during cleaning
- Issue: Words like "हैः" were being counted separately from "है"
- Solution: Added visarga to regex pattern: `re.sub(r'[।॥ः]+', ' ', text)`

### 3. **Tokenization: No Length Filter**
- Decision: Removed `len(word) > 1` filter
- Issue: Common Hindi words (के, में, है) were being excluded
- Solution: Keep all non-empty tokens from whitespace split
- Impact: Corrected word frequency rankings

### 4. **Source Management: Object-Oriented**
- Decision: Use `HindiSources` class with `DataSource` objects
- Pattern:
  ```python
  class HindiSources:
      WIKIPEDIA = DataSource("url", "download")
      LEIPZIG_2019 = DataSource("url", "download")
      # etc.
  ```
- Benefit: Type-safe, extensible, supports different source types

### 5. **Resume Support with Checkpoints**
- Decision: Save progress using pickle after each directory
- Files: `tmp/processing_checkpoint.pkl`
- Usage: `--resume` flag to continue from checkpoint
- Benefit: Can interrupt and resume long-running processing

### 6. **Top 30,000 Words in 10 Files**
- Decision: Split top 30K words into fixed-size chunks
- Format: hw01.txt to hw10.txt (3000 words each)
- Sorted: By frequency (highest first)
- Use case: Easy access to most common words

### 7. **HuggingFace Integration**
- Decision: Use public datasets (no authentication)
- Dataset: `ai4bharat/sangraha`
- Reason: OSCAR and MC4 require authentication
- Format: Parquet files processed with PyArrow

### 8. **Git History Management**
- Decision: Never commit large output files (words.txt, words.csv)
- .gitignore: `tmp/`, `words.txt`
- Tracked: `words/` folder (top 30K split files)
- Reason: Keep repository size small

## Processing Pipeline

### Step 1: Download
- Downloads compressed files from URLs
- Handles `.tar.gz`, `.bz2`, `.zip` formats
- Skips existing files with `--skip-download`
- Output: `tmp/downloads/`

### Step 2: Extract
- Extracts Wikipedia XML dump (1.6 GB)
- Extracts Leipzig corpora
- Downloads HuggingFace dataset files
- Downloads GitHub text files
- Skips if directories exist with `--skip-extract`
- Output: `tmp/extracted/`, `tmp/huggingface/`, `tmp/github/`

### Step 3: Process
- Reads all text files from three directories
- Cleans text (removes punctuation, non-Hindi chars)
- Tokenizes on whitespace
- Counts word frequencies using `collections.Counter`
- Merges all sources
- Sorts by frequency (descending)
- Saves to `words.txt`
- Output: `words.txt`

### Step 4: Split (optional)
- Reads `words.txt`
- Takes top 30,000 words
- Splits into 10 files of 3000 each
- Output: `words/hw01.txt` to `words/hw10.txt`

## Architecture

### `main.py`
- Entry point, argument parsing
- Orchestrates download → extract → process pipeline
- Handles checkpoint save/load

### `src/sources.py`
- Defines `DataSource` class (url, source_type)
- Defines `HindiSources` class with all 5 sources
- Supports: download, huggingface, github types

### `src/downloader.py`
- Downloads files from URLs
- Handles resuming interrupted downloads
- Progress bars for large files

### `src/extractor.py`
- Extracts `.tar.gz`, `.bz2`, `.zip` files
- Preserves directory structure
- Skips if already extracted

### `src/processor.py`
- `HindiProcessor` class
- Methods:
  - `clean_text()`: Removes punctuation and non-Hindi chars
  - `tokenize()`: Splits text into words
  - `process_file()`: Processes single file
  - `process_directory()`: Processes all files in directory
  - `save_frequencies()`: Saves to text file
  - `save_checkpoint()`: Saves pickle checkpoint
  - `load_checkpoint()`: Loads pickle checkpoint
  - `merge_frequencies()`: Merges multiple frequency dicts

### `src/split_top_words.py`
- `split_top_words()` function
- Reads `words.txt`
- Sorts by frequency
- Takes top 30,000
- Splits into 10 files

## Performance

- **Processing time:** ~15-20 minutes (full pipeline)
- **Disk usage:**
  - tmp/downloads/: ~500 MB
  - tmp/extracted/: ~1.8 GB
  - tmp/huggingface/: ~100 MB
  - tmp/github/: ~11 MB
  - words.txt: 107 MB
  - words/: 650 KB (10 files)

## Error Handling

- Skip unsupported file formats (e.g., `.dic` files)
- Continue on individual file processing errors
- Log errors to console
- Checkpoint recovery on interruption

## Future Improvements

- Add more data sources (news websites, book corpora)
- Implement parallel processing for faster performance
- Add word filtering options (min frequency, word length)
- Generate n-grams (bigrams, trigrams)
- Add part-of-speech tagging
- Create web interface for searching word frequencies

## License

This project downloads and processes data from various sources. Please check the licenses of the original data sources before using the output for commercial purposes.

## Contributing

To add new data sources:

1. Edit `src/sources.py`
2. Add new `DataSource` to `HindiSources` class
3. Re-run: `~/PYENV/bin/python3 main.py --skip-download`

Example:
```python
class HindiSources:
    # ... existing sources ...
    NEW_SOURCE = DataSource("https://example.com/hindi-corpus.tar.gz", "download")
```
