import spotipy
from spotipy.oauth2 import SpotifyOAuth
from . import Track
from ..config import Config
from .. import logger


class SpotifySource:
    def __init__(self, config: Config):
        if (
            not config.SPOTIFY_CLIENT_ID
            or not config.SPOTIFY_CLIENT_SECRET
            or not config.SPOTIFY_REDIRECT_URI
        ):
            logger.debug("Spotify credentials not configured.")
            self.client = None
            return

        self.client = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=config.SPOTIFY_CLIENT_ID,
                client_secret=config.SPOTIFY_CLIENT_SECRET,
                redirect_uri=config.SPOTIFY_REDIRECT_URI,
                scope="user-read-currently-playing user-read-playback-state",
            )
        )

    def get_current_track(self) -> Track | None:
        if not self.client:
            logger.debug("Spotify credentials not configured.")
            return

        try:
            current_track = self.client.current_playback()

            if not current_track or not current_track["is_playing"]:
                return None

            # Extract track information
            track = current_track["item"]
            return Track(
                name=track["name"],
                artist=track["artists"][0]["name"],
                album=track["album"]["name"],
                url=track["external_urls"]["spotify"],
                image=(
                    track["album"]["images"][0]["url"]
                    if track["album"]["images"]
                    else None
                ),
                progress_ms=current_track["progress_ms"],
                duration_ms=track["duration_ms"],
                source="spotify",
            )
        except Exception as e:
            logger.error(f"Error fetching Spotify track: {e}")
            return None
