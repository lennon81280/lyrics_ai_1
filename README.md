# Lyrics Fetcher


Simple script to retrieve song lyrics. It first tries the
[lyrics.ovh](https://lyrics.ovh) API and falls back to scraping
[lyrics.com](https://www.lyrics.com) if necessary.


## Usage

Run the script and follow prompts for song title and artist:

```bash
python lyrics_fetcher.py
```

To avoid prompts, pass the title and artist as arguments:

```bash
python lyrics_fetcher.py "Mother" "Pink Floyd"
```

The script prints only the lyrics, with extra blank lines removed.
Input prompts are written to stderr so that redirecting stdout captures just the lyrics.
