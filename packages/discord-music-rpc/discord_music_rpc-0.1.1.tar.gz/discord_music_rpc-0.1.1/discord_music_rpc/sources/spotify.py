import spotipy
from spotipy.oauth2 import SpotifyOAuth

from .. import logger
from . import BaseSource, Track


class SpotifySource(BaseSource):
    def initialize_client(self):
        if (
            not self.config.spotify.client_id
            or not self.config.spotify.client_secret
            or not self.config.SPOTIFY_REDIRECT_URI
        ):
            logger.debug("Spotify credentials not configured.")
            return

        self.client = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=self.config.spotify.client_id,
                client_secret=self.config.spotify.client_secret,
                redirect_uri=self.config.SPOTIFY_REDIRECT_URI,
                scope="user-read-currently-playing user-read-playback-state",
            )
        )

    def get_current_track(self):
        if not self.client:
            logger.debug("Spotify credentials not configured.")
            return None

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
