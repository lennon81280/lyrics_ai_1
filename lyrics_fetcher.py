from typing import Optional
import argparse
import json
import urllib.request
import urllib.error
import urllib.parse

API_URL = "https://api.lyrics.ovh/v1/{artist}/{title}"

def get_lyrics(title: str, artist: str, timeout: int = 10) -> Optional[str]:
    """Return song lyrics using the lyrics.ovh API.

    Args:
        title: Title of the song.
        artist: Performing artist.
        timeout: Request timeout in seconds.
    Returns:
        Lyrics text if found, otherwise None.
    """
    url = API_URL.format(
        artist=urllib.parse.quote(artist),
        title=urllib.parse.quote(title),
    )
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if resp.status == 200:
                data = json.loads(resp.read().decode())
                return data.get("lyrics")
    except (urllib.error.URLError, TimeoutError):
        pass
    return None


def clean_lyrics(text: str) -> str:
    """Return lyrics stripped of surrounding whitespace and extra blank lines."""
    lines = [line.rstrip() for line in text.splitlines()]
    cleaned: list[str] = []
    previous_blank = False
    for line in lines:
        is_blank = line == ""
        if is_blank and previous_blank:
            continue
        cleaned.append(line)
        previous_blank = is_blank
    return "\n".join(cleaned).strip()


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch song lyrics")
    parser.add_argument("title", nargs="?", help="Song title")
    parser.add_argument("artist", nargs="?", help="Song artist")
    args = parser.parse_args()

    title = args.title or input("Song title: ").strip()
    artist = args.artist or input("Artist: ").strip()

    lyrics = get_lyrics(title, artist)
    if lyrics:
        print(clean_lyrics(lyrics))
    else:
        print("Lyrics not found or service unavailable.")


if __name__ == "__main__":
    main()
