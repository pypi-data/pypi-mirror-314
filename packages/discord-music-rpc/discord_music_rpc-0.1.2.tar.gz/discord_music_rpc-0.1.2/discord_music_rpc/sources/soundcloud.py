import datetime

from soundcloud import SoundCloud

from .. import logger
from . import BaseSource, Track


class SoundCloudSource(BaseSource):
    def initialize_client(self):
        if not self.config.soundcloud.auth_token:
            logger.debug("SoundCloud credentials not configured.")
            self.client = None
        else:
            self.client = SoundCloud(auth_token=self.config.soundcloud.auth_token)

    def get_current_track(self) -> Track | None:
        if not self.client:
            logger.debug("SoundCloud credentials not configured.")
            return None

        song = next(self.client.get_my_history())
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

        return None
