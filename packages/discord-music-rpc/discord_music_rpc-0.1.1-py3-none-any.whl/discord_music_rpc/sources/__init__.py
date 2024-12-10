from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Literal, Optional


@dataclass
class Track:
    name: str
    artist: str
    source: Literal["spotify", "lastfm", "soundcloud", "plex"]
    album: Optional[str] = None
    url: Optional[str] = None
    image: Optional[str] = None
    progress_ms: Optional[int] = None
    duration_ms: Optional[int] = None


class BaseSource(ABC):
    def __init__(self, config):
        self.client = None
        self.config = config
        self.initialize_client()

    @abstractmethod
    def initialize_client(self):
        """
        Initialize the client for the specific source.
        Should be implemented by subclasses.
        """
        pass

    @abstractmethod
    def get_current_track(self):
        """
        Retrieve the currently playing track.
        Should return a Track object or None if no track is playing.
        """
        pass
