from . import Track
from .lastfm import LastFmSource
from .soundcloud import SoundCloudSource
from .spotify import SpotifySource
from .plex import PlexSource
from ..config import Config


class MusicSourceManager:
    def __init__(self, config: Config):
        self.sources = [  # also works as priority highest -> lowest
            SpotifySource(config),  # highest priority because it has progress info
            PlexSource(config),
            LastFmSource(config),
            SoundCloudSource(
                config
            ),  # lowest priority because poo code for checking if currently playing
        ]

    def get_current_track(self) -> Track | None:
        for source in self.sources:
            track = source.get_current_track()
            if track:
                return track
        return None
