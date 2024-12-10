from pathlib import Path

import yaml
from pydantic import BaseModel

from . import CONFIG_DIR, logger, utils

CFG_PATH = CONFIG_DIR / "config.yaml"


class DiscordConfig(BaseModel):
    client_id: str | None = None


class SpotifyConfig(BaseModel):
    client_id: str | None = None
    client_secret: str | None = None
    redirect_uri: str = "http://localhost:8888/callback"


class LastFmConfig(BaseModel):
    username: str | None = None
    api_key: str | None = None


class SoundCloudConfig(BaseModel):
    auth_token: str | None = None


class PlexConfig(BaseModel):
    server_url: str | None = None
    token: str | None = None


class Config(BaseModel):
    discord: DiscordConfig = DiscordConfig()
    spotify: SpotifyConfig = SpotifyConfig()
    lastfm: LastFmConfig = LastFmConfig()
    soundcloud: SoundCloudConfig = SoundCloudConfig()
    plex: PlexConfig = PlexConfig()

    def validate(self):
        if not self.discord.client_id:
            logger.error(
                f"discord.client_id not configured. Please follow the steps in the README and fill out {CFG_PATH}"
            )
            return False

        # Spotify configuration checks
        if not self.spotify.client_id:
            logger.info(
                "Note: spotify.client_id not configured. Spotify support will be disabled."
            )
        if not self.spotify.client_secret:
            logger.info(
                "Note: spotify.client_secret not configured. Spotify support will be disabled."
            )

        # Last.fm configuration checks
        if not self.lastfm.username:
            logger.info(
                "Note: lastfm.username not configured. Spotify support will be disabled."
            )
        if not self.lastfm.api_key:
            logger.info(
                "Note: lastfm.api_key not configured. Spotify support will be disabled."
            )

        if not self.soundcloud.auth_token:
            logger.info(
                "Note: soundcloud.auth_token not configured. SoundCloud support will be disabled."
            )

        if not self.plex.server_url:
            logger.info(
                "Note: plex.server_url not configured. SoundCloud support will be disabled."
            )
        if not self.plex.token:
            logger.info(
                "Note: plex.token not configured. SoundCloud support will be disabled."
            )

        # todo return false if nothings enabled? idk
        return True

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
