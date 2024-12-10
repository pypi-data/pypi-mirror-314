from contextlib import contextmanager
import os
import yaml
from pathlib import Path
from . import utils
from pydantic import BaseModel

from . import logger, CONFIG_DIR

CFG_PATH = CONFIG_DIR / "config.yaml"


class Config(BaseModel):
    # Spotify Configuration
    SPOTIFY_CLIENT_ID: str | None = None
    SPOTIFY_CLIENT_SECRET: str | None = None
    SPOTIFY_REDIRECT_URI: str = "http://localhost:8888/callback"

    # Last.fm Configuration
    LASTFM_USERNAME: str | None = None
    LASTFM_API_KEY: str | None = None

    # SoundCloud Configuration
    SOUNDCLOUD_AUTH_TOKEN: str | None = None

    # Plex Configuration
    PLEX_SERVER_URL: str | None = None
    PLEX_TOKEN: str | None = None

    # Discord RPC Configuration
    DISCORD_CLIENT_ID: str | None = None

    def validate(self):
        # Spotify configuration checks
        if not self.SPOTIFY_CLIENT_ID:
            logger.info(
                "Note: SPOTIFY_CLIENT_ID not configured. Spotify support will be disabled."
            )
        if not self.SPOTIFY_CLIENT_SECRET:
            logger.info(
                "Note: SPOTIFY_CLIENT_SECRET not configured. Spotify support will be disabled."
            )

        # Last.fm configuration checks
        if not self.LASTFM_USERNAME:
            logger.info(
                "Note: LASTFM_USERNAME not configured. Spotify support will be disabled."
            )
        if not self.LASTFM_API_KEY:
            logger.info(
                "Note: LASTFM_API_KEY not configured. Spotify support will be disabled."
            )

        if not self.SOUNDCLOUD_AUTH_TOKEN:
            logger.info(
                "Note: SOUNDCLOUD_AUTH_TOKEN not configured. SoundCloud support will be disabled."
            )

        if not self.PLEX_SERVER_URL:
            logger.info(
                "Note: PLEX_SERVER_URL not configured. SoundCloud support will be disabled."
            )
        if not self.PLEX_TOKEN:
            logger.info(
                "Note: PLEX_TOKEN not configured. SoundCloud support will be disabled."
            )

        # todo return false if nothings enabled? idk

    def dump(self):
        return self.model_dump()

    def save(self, path: Path = CFG_PATH):
        with path.open("w") as f:
            yaml.dump(self.dump(), f, Dumper=utils.PrettyDumper, sort_keys=False)

    @staticmethod
    def load(path: Path = CFG_PATH):
        if not path.exists() or path.stat().st_size == 0:
            Config().save()

        with path.open("r") as f:
            yaml_data = yaml.safe_load(f)

            if not isinstance(yaml_data, dict):
                raise ValueError("YAML data is not a dictionary")

            return Config(**yaml_data)


def load_config():
    config = Config.load()

    # config might be missing or have extra variables, save after validating
    # todo: i know if you just created a config for the first time this will save pointlessly but idc
    config.save()

    return config
