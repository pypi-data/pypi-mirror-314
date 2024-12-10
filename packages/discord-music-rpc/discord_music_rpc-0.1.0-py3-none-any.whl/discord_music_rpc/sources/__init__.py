from dataclasses import dataclass
from typing import Optional, Literal


@dataclass
class Track:
    name: str
    artist: str
    source: Literal["spotify", "lastfm", "soundcloud"]
    album: Optional[str] = None
    url: Optional[str] = None
    image: Optional[str] = None
    progress_ms: Optional[int] = None
    duration_ms: Optional[int] = None
