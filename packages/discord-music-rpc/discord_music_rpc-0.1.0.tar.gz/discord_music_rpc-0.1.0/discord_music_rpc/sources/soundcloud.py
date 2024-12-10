import datetime
from soundcloud import SoundCloud
from . import Track
from ..config import Config
from .. import logger


class SoundCloudSource:
    def __init__(self, config: Config):
        if not config.SOUNDCLOUD_AUTH_TOKEN:
            logger.debug("SoundCloud credentials not configured.")
            self.sc = None
            return

        self.sc = SoundCloud(auth_token=config.SOUNDCLOUD_AUTH_TOKEN)

    def get_current_track(self) -> Track | None:
        if not self.sc:
            logger.debug("SoundCloud credentials not configured.")
            return None

        song = next(self.sc.get_my_history())
        if not song:
            return None

        now = int(datetime.datetime.now().timestamp() * 1000)

        if now > song.played_at and now <= song.played_at + song.track.duration:
            return Track(
                name=song.track.title,
                artist=song.track.user.username,
                url=song.track.permalink_url,
                image=song.track.artwork_url,
                source="soundcloud",
            )
