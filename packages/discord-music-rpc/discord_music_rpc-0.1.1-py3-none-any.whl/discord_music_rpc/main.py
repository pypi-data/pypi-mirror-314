import time

import pypresence

from . import killer, logger
from .config import load_config
from .discord_rpc import DiscordRichPresence
from .sources.sources import MusicSourceManager
from .tray import run_tray_icon, update_tray
from .utils import is_same_track


def run_rpc(music_sources, discord_rpc, icon):
    last_track = None

    while not killer.kill_now:
        current_track = music_sources.get_current_track()

        if current_track:
            if not is_same_track(current_track, last_track):
                logger.info(
                    f"Now playing: {current_track.artist} - {current_track.name} ({current_track.source})"
                )

            discord_rpc.update(current_track)
        else:
            discord_rpc.clear()

        update_tray(icon, current_track)

        last_track = current_track

        time.sleep(1)  # todo: config this? diff services diff sleeps? (ratelimiting)


def run():
    icon = run_tray_icon()

    while not killer.kill_now:
        config = load_config()

        if not config.validate():
            logger.info("Config failed to validate")
            time.sleep(5)
            continue

        music_sources = MusicSourceManager(config)
        discord_rpc = DiscordRichPresence(config)

        try:
            discord_rpc.connect()

            run_rpc(music_sources, discord_rpc, icon)
        except pypresence.exceptions.PipeClosed:
            logger.warning("Lost connection to Discord, attempting to reconnect...")
            time.sleep(1)
        except pypresence.exceptions.DiscordNotFound:
            logger.warning("Couldn't find Discord, is it open? Trying again...")
            time.sleep(3)
        except pypresence.exceptions.DiscordError as e:
            logger.warning(e)
            time.sleep(1)
        finally:
            discord_rpc.close()
