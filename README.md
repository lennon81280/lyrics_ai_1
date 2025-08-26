# Lyrics Fetcher

Simple script to retrieve song lyrics using the [lyrics.ovh](https://lyrics.ovh) API.

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
