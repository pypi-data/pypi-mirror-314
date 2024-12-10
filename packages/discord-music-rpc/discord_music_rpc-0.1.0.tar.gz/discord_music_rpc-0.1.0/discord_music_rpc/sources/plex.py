import datetime
import pprint
from plexapi.server import PlexServer
from plexapi.audio import Audio, Track as PlexTrack, Album, Artist
from . import Track
from ..config import Config
from .. import logger


class PlexSource:
    def __init__(self, config: Config):
        if not config.PLEX_SERVER_URL or not config.PLEX_TOKEN:
            logger.debug("Plex credentials not configured.")
            self.plex = None
            return

        self.plex = PlexServer(config.PLEX_SERVER_URL, config.PLEX_TOKEN)

    def get_current_track(self) -> Track | None:
        if not self.plex:
            logger.debug("Plex credentials not configured.")
            return None

        for session in self.plex.sessions():
            if session.type != "track":
                continue

            track: PlexTrack = session
            artist: Artist = track.artist()
            album: Album = track.album()

            return Track(
                name=track.title,
                artist=artist.title,
                album=album.title,
                url=None,
                image=None,  # todo: track.thumbUrl
                progress_ms=track.viewOffset,
                duration_ms=track.duration,
                source="plex",
            )
