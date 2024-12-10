import yaml

from .sources import Track


def is_same_track(track1: Track | None, track2: Track | None) -> bool:
    if not track1 or not track2:
        return False

    return (
        track1.name == track2.name
        and track1.artist == track2.artist
        and track1.album == track2.album
        and track1.source == track2.source
    )


class PrettyDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super().increase_indent(flow, False)
