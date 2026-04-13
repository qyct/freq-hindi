# Hindi Word Frequency Analysis

Download and process Hindi corpus files to generate word frequency statistics.

## Structure

```
.
├── main.py           # Main entry point (uses ~/PYENV)
├── words.csv         # Output file (word, freq) - 1.7M+ words
├── requirements.txt  # Python dependencies
├── .gitignore        # Excludes tmp/, words.csv
└── src/             # Helper modules
    ├── __init__.py   # Package init
    ├── sources.py    # Data source URLs
    ├── downloader.py # Download files from URLs
    ├── extractor.py  # Extract compressed files (.tar.gz, .bz2)
    └── processor.py  # Process text & count frequencies
```

## Usage

Install dependencies (using ~/PYENV):
```bash
~/PYENV/bin/pip install -r requirements.txt
```

Run the full pipeline:
```bash
./main.py
```

Skip steps if files already exist:
```bash
./main.py --skip-download --skip-extract
```

## Data Sources

Currently configured (in `src/sources.py`):

1. **Wikimedia Hindi Dumps**
   - URL: `https://dumps.wikimedia.org/hiwiki/latest/hiwiki-latest-pages-articles.xml.bz2`
   - Size: 224 MB → 1.6 GB extracted
   - Content: All Hindi Wikipedia articles
   - Best for: Formal, encyclopedic content

2. **Leipzig Hindi Corpora**
   - URL: `https://downloads.wortschatz-leipzig.de/corpora/hin_mixed_2019_1M.tar.gz`
   - Size: 218 MB compressed
   - Content: 1M randomized sentences from web sources
   - Best for: Balanced frequency analysis

**Temporary files:** Stored in `tmp/` (downloads, extracted)

## Current Statistics

- **Total unique words:** 1,723,497
- **Sources processed:** 2 (Wikipedia + Leipzig)
- **Files processed:** 9 text files
- **Text cleaning:** Removes purna viram (।), non-Hindi characters

## Top 20 Words by Frequency

| Rank | Word | Frequency | Meaning |
|------|------|-----------|---------|
| 1 | के | 3,556,908 | of (masc) |
| 2 | में | 2,507,042 | in |
| 3 | है | 2,080,930 | is |
| 4 | की | 1,711,162 | of (fem) |
| 5 | और | 1,376,401 | and |
| 6 | का | 1,236,982 | of (masc) |
| 7 | से | 1,225,860 | from |
| 8 | को | 1,137,761 | to |
| 9 | एक | 741,349 | one |
| 10 | हैं | 738,926 | are |
| 11 | पर | 688,160 | on |
| 12 | ने | 583,667 | by (past tense marker) |
| 13 | भी | 499,093 | also |
| 14 | किया | 491,982 | did |
| 15 | लिए | 476,268 | for |
| 16 | कि | 407,346 | that |
| 17 | गया | 376,942 | went |
| 18 | था | 359,603 | was |
| 19 | यह | 358,362 | this |

## Output

**File:** `words.csv` - Two columns:
- `word` - Hindi word (Devanagari script, cleaned)
- `freq` - Frequency count (descending order)

**Cleaning features:**
- ✅ Removes purna viram (।) and deergha viram (॥)
- ✅ Splits on multiple consecutive punctuation
- ✅ Only keeps pure Hindi characters
- ✅ Filters single-character words

## Development

Add new sources in `src/sources.py`:
```python
SOURCES = [
    "https://example.com/hindi-corpus.tar.gz",
    # Add more URLs here
]
```

Then re-run:
```bash
./main.py --skip-download  # If already downloaded
```
