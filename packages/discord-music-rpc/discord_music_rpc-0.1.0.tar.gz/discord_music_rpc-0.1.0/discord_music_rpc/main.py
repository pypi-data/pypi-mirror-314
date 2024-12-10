import threading
import time

import pypresence

from .config import Config, load_config
from .sources.sources import MusicSourceManager
from .discord_rpc import DiscordRichPresence
from .utils import is_same_track
from .tray import run_tray_icon, update_tray
from . import killer, logger


def main():
    config = load_config()
    config.validate()

    music_sources = MusicSourceManager(config)
    discord_rpc = DiscordRichPresence(config)

    icon = run_tray_icon()

    last_track = None

    while not killer.kill_now:
        try:
            # Connect to Discord RPC
            discord_rpc.connect()

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

                time.sleep(
                    1
                )  # todo: config this? diff services diff sleeps? (ratelimiting)
        except pypresence.exceptions.PipeClosed:
            logger.warning("Lost connection to Discord, attempting to reconnect...")
            time.sleep(1)
        except pypresence.exceptions.DiscordNotFound:
            logger.warning("Couldn't find Discord, is it open? Trying again...")
            time.sleep(3)
        except pypresence.exceptions.DiscordError as e:
            logger.warning(e)
            time.sleep(1)

    discord_rpc.close()


if __name__ == "__main__":
    main()
