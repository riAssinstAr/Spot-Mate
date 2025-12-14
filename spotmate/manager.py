from pathlib import Path
from spotmate.actions import (
    get_destination,
    serialize_track,
)
from spotmate.playlist_utils import (
    copy_songs,
    delete_playlist,
    delete_songs_range,
    export_tracks,
)
from spotmate.ui import (
    choose_range,
    confirm,
    select_from_list,
)

def copy_all(writeable_names, sp_user, user_id, source_tracks):
    print()
    if not source_tracks:
        print("No tracks found to copy!")
        return

    dest_playlist = get_destination(writeable_names, sp_user, user_id)
    if dest_playlist is None or dest_playlist == "Cancel":
        print("\nOperation cancelled!")
        return

    print()
    if confirm(f"Copy {len(source_tracks)} songs to '{dest_playlist}'?"):
        try:
            copy_songs(sp_user, source_tracks, dest_playlist)
        except Exception as e:
            print(f"Error copying songs: {e}")


def copy_range(writable_names, sp_user, user_id, source_tracks):
    print()
    source_tracks = choose_range(source_tracks)
    copy_all(writable_names, sp_user, user_id, source_tracks)


def remove_playlist(sp_user, source_playlist):
    print()
    if confirm(f"Remove '{source_playlist['name']}' from your library?"):
        try:
            delete_playlist(sp_user, source_playlist)
            return True
        except Exception as e:
            print(f"Error removing playlist: {e}")
    return False


def remove_range(sp_user, source_playlist, source_tracks):
    print()
    source_tracks = choose_range(source_tracks)
    if not source_tracks:
        print("No tracks found to remove!")
        return

    print()
    if confirm(f"Remove {len(source_tracks)} songs from {source_playlist["name"]}?"):
        try:
            delete_songs_range(sp_user, source_playlist, source_tracks)
        except Exception as e:
            print(f"Error deleting songs: {e}")


def export_playlist(source_playlist, source_tracks, output_dir="."):
    print()
    source_tracks = choose_range(source_tracks)
    if not source_tracks:
        print("No tracks found to export!")
        return

    file_format = select_from_list(
        title="Export Playlist",
        text="Choose export format:",
        options=["JSON", "CSV", "Cancel"],
    )
    if file_format in (None, "Cancel"):
        print("Export cancelled!")
        return

    tracks = tracks = [serialize_track(t) for t in source_tracks]
    filename = source_playlist["name"].replace("/", "_").replace("\\", "_")
    path = Path(output_dir) / f"{filename}.{file_format}"
    export_tracks(tracks, path, file_format)

    print(f"\nExported {len(tracks)} tracks to {path}")
