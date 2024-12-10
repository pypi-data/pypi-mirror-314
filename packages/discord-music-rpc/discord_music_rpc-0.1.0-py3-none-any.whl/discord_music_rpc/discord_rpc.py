import datetime
from pypresence import Presence, ActivityType
from .sources import Track
from .config import Config
from .utils import is_same_track
from . import logger


class DiscordRichPresence:
    def __init__(self, config: Config):
        self.client_id = config.DISCORD_CLIENT_ID
        self.rpc = Presence(self.client_id)
        self.last_track: Track | None = None
        self.last_progress: int | None = None

    def connect(self):
        self.rpc.connect()
        logger.info("Connected to Discord RPC")

    def update(self, track: Track | None):
        if not track:
            self.clear()
            return

        # buttons = []
        # buttons.append(
        #     {
        #         "label": f"View {track.source.capitalize()} Track",
        #         "url": track.url or "",
        #     }
        # )

        start_time = None
        end_time = None

        if not is_same_track(track, self.last_track):
            self.last_progress = None

        if track.progress_ms is not None and track.duration_ms is not None:
            if (
                track.progress_ms == self.last_progress
            ):  # haven't gotten any progress, don't update - discord will handle it
                return

            start_time = (
                int(datetime.datetime.now().timestamp() * 1000) - track.progress_ms
            )
            end_time = start_time + track.duration_ms
            self.last_progress = track.progress_ms

        self.rpc.update(
            activity_type=ActivityType.LISTENING,
            details=track.name,
            state=track.artist,
            large_image=track.image,
            large_text=track.album.ljust(
                2
            ),  # "large_text" length must be at least 2 characters long
            # buttons=buttons,
            start=start_time,
            end=end_time,
        )

        self.last_track = track

    def clear(self):
        self.rpc.clear()

    def close(self):
        try:
            self.clear()
            self.rpc.close()
        except Exception as e:
            logger.error(e)
