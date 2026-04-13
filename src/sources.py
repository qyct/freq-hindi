"""Hindi corpus data sources."""


class DataSource:
    """Base class for data sources."""

    def __init__(self, url: str, source_type: str = "download"):
        """
        Initialize a data source.

        Args:
            url: URL to download from
            source_type: Type of source (download, github, huggingface)
        """
        self.url = url
        self.source_type = source_type


class HindiSources:
    """Hindi corpus sources configuration."""

    # Wikimedia Hindi dumps (encyclopedic text)
    WIKIPEDIA = DataSource(
        "https://dumps.wikimedia.org/hiwiki/latest/hiwiki-latest-pages-articles.xml.bz2",
        "download"
    )

    # Leipzig Hindi Corpora (frequency analysis samples)
    LEIPZIG_2019 = DataSource(
        "https://downloads.wortschatz-leipzig.de/corpora/hin_mixed_2019_1M.tar.gz",
        "download"
    )

    # HuggingFace: ai4bharat/sangraha (Hindi Wikipedia)
    # Downloaded via: src/download_sangraha.py
    HUGGINGFACE_SANGRAHA = DataSource(
        "ai4bharat/sangraha",
        "huggingface"
    )

    # GitHub: Gayatri Venugopal - Hindi stop lemmas with frequencies
    GITHUB_GAYATRI = DataSource(
        "https://raw.githubusercontent.com/gayatrivenugopal/hindi-corpus-stoplemmas/master/final%20stop%20lemma%20list.txt",
        "github"
    )

    # GitHub: Shreeshrii - Hindi Hunspell dictionary
    GITHUB_HUNSPELL = DataSource(
        "https://raw.githubusercontent.com/Shreeshrii/hindi-hunspell/master/Hindi/hi_IN.txt",
        "github"
    )

    @classmethod
    def get_all_download_urls(cls):
        """Get all download URLs for the downloader."""
        return [
            cls.WIKIPEDIA.url,
            cls.LEIPZIG_2019.url,
        ]

    @classmethod
    def get_all_github_urls(cls):
        """Get all GitHub URLs."""
        return [
            cls.GITHUB_GAYATRI.url,
            cls.GITHUB_HUNSPELL.url,
        ]

    @classmethod
    def get_huggingface_datasets(cls):
        """Get all HuggingFace dataset names."""
        return [
            cls.HUGGINGFACE_SANGRAHA.url,
        ]
