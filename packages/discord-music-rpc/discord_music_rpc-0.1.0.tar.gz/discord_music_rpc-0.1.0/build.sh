uv run python -m nuitka --onefile --follow-imports --python-flag=no_site --output-dir=dist --output-filename=discord-music-rpc --include-data-dir=discord_music_rpc/resources=discord_music_rpc/resources --windows-console-mode=disable --assume-yes-for-downloads --python-flag=-m discord_music_rpc
echo done
