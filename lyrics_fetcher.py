from typing import Optional
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


def main() -> None:
    title = input("Song title: ").strip()
    artist = input("Artist: ").strip()
    lyrics = get_lyrics(title, artist)
    if lyrics:
        print("\n===== Lyrics =====\n")
        print(lyrics)
    else:
        print("Lyrics not found or service unavailable.")


if __name__ == "__main__":
    main()
