import requests
from . import Track
from ..config import Config
from .. import logger


class LastFmSource:
    def __init__(self, config: Config):
        self.username = config.LASTFM_USERNAME
        self.api_key = config.LASTFM_API_KEY

        if not self.username or not self.api_key:
            logger.debug("Last.fm credentials not configured.")

    def get_current_track(self) -> Track | None:
        if not self.username or not self.api_key:
            logger.debug("Last.fm username or API key not configured.")
            return None

        params = {
            "method": "user.getrecenttracks",
            "api_key": self.api_key,
            "user": self.username,
            "limit": "1",
            "format": "json",
        }

        try:
            response = requests.get("https://ws.audioscrobbler.com/2.0/", params=params)
            data = response.json()

            # Check if a track is currently playing
            track = data["recenttracks"]["track"][0]
            if "@attr" in track and track["@attr"].get("nowplaying") == "true":
                return Track(
                    name=track["name"],
                    artist=track["artist"]["#text"],
                    album=track["album"]["#text"],
                    url=track["url"],
                    image=next(
                        (
                            img["#text"]
                            for img in track["image"]
                            if img["size"] == "large"
                        ),
                        None,
                    ),
                    source="lastfm",
                )
            return None
        except Exception as e:
            logger.error(f"Error fetching Last.fm track: {e}")
            return None
