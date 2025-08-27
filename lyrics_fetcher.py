from typing import Optional
import argparse
import json
import sys
import re
import html
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

            if resp.status != 200:
                return None
            data = json.loads(resp.read().decode())
            return data.get("lyrics")
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):

        return None
    return None


def fetch_lyrics_lyricscom(title: str, artist: str, timeout: int = 10) -> Optional[str]:
    """Fetch lyrics by scraping lyrics.com as a fallback."""
    query = urllib.parse.quote(f"{title} {artist}")
    search_url = f"https://www.lyrics.com/lyrics/{query}"
    try:
        with urllib.request.urlopen(search_url, timeout=timeout) as resp:
            if resp.status != 200:
                return None
            search_html = resp.read().decode(errors="ignore")
    except (urllib.error.URLError, TimeoutError):
        return None

    match = re.search(r'<td class="tal qx"><strong><a href="(/lyric/[^"?]+)"', search_html)
    if not match:
        return None

    song_url = "https://www.lyrics.com" + match.group(1)
    try:
        with urllib.request.urlopen(song_url, timeout=timeout) as resp:
            if resp.status != 200:
                return None
            song_html = resp.read().decode(errors="ignore")
    except (urllib.error.URLError, TimeoutError):
        return None

    body = re.search(r'<pre id="lyric-body-text"[^>]*>(.*?)</pre>', song_html, re.S)
    if not body:
        return None
    return html.unescape(body.group(1)).strip()


def get_lyrics(title: str, artist: str, timeout: int = 10) -> Optional[str]:
    """Return song lyrics from available sources."""
    lyrics = fetch_lyrics_ovh(title, artist, timeout)
    if lyrics:
        return lyrics
    return fetch_lyrics_lyricscom(title, artist, timeout)

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

    if args.title:
        title = args.title
    else:
        print("Song title: ", end="", file=sys.stderr)
        title = input().strip()

    if args.artist:
        artist = args.artist
    else:
        print("Artist: ", end="", file=sys.stderr)
        artist = input().strip()

    lyrics = get_lyrics(title, artist)
    if lyrics:
        print(clean_lyrics(lyrics))
    else:
        print("Lyrics not found or service unavailable.")


if __name__ == "__main__":
    main()
