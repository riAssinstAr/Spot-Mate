from pathlib import Path
import time
from prompt_toolkit import prompt
from spotmate.actions import (
    clear_screen,
    get_actions_for_source,
    get_destination,
    get_file_tracks,
    get_source_meta,
    serialize_tracks,
)
from spotmate.playlist_utils import (
    copy_songs,
    delete_songs_range,
    export_tracks,
    get_source_tracks,
    remove_source,
)
from spotmate.ui import (
    choose_range,
    confirm,
    select_from_list,
)

def copy_all(sp_user, user_id, source_tracks):
    if not source_tracks:
        print("No tracks to copy!")
        return

    dest_playlist = get_destination(sp_user, user_id)
    if dest_playlist is None or dest_playlist == "Cancel":
        print("\nOperation cancelled!")
        return

    print()
    if confirm(f"Copy {len(source_tracks)} songs to '{dest_playlist}'?"):
        try:
            copy_songs(sp_user, source_tracks, dest_playlist)
        except Exception as e:
            print(f"Error copying songs: {e}")


def copy_range(sp_user, user_id, source_tracks):
    source_tracks = choose_range(source_tracks)
    copy_all(sp_user, user_id, source_tracks)


def remove_playlist_album(sp_user, source, source_type):
    if confirm(f"Remove '{source['name']}' from your library?"):
        try:
            remove_source(sp_user, source, source_type)
        except Exception as e:
            print(f"Error removing playlist: {e}")


def remove_all(sp_user, source_playlist, source_tracks):
    if not source_tracks:
        print("No tracks to remove!")
        return

    print()
    if confirm(f"Remove {len(source_tracks)} songs from {source_playlist['name']}?"):
        try:
            delete_songs_range(sp_user, source_playlist, source_tracks)
        except Exception as e:
            print(f"Error deleting songs: {e}")


def remove_range(sp_user, source_playlist, source_tracks):
    source_tracks = choose_range(source_tracks)
    remove_all(sp_user, source_playlist, source_tracks)


def export_playlist(source_playlist, source_tracks, output_dir="."):
    if not source_tracks:
        print("No tracks to export!")
        return

    file_format = select_from_list(
        title="Export Playlist",
        text="Choose export format:",
        options=["JSON", "CSV", "Cancel"],
    )
    clear_screen()
    if file_format in (None, "Cancel"):
        print("Export cancelled!")
        return

    tracks = [serialize_tracks(t) for t in source_tracks]
    filename = source_playlist["name"].replace("/", "_").replace("\\", "_")
    path = Path(output_dir) / f"{filename}.{file_format}"
    try:
        export_tracks(tracks, path, file_format)
        print(f"\nExported {len(tracks)} tracks to {path}")
    except Exception as e:
        print(f"Error exporting tracks: {e}")


def export_playlist_range(source_playlist, source_tracks, output_dir="."):
    source_tracks = choose_range(source_tracks)
    export_playlist(source_playlist, source_tracks, output_dir)


def import_playlist(sp_user, user_id):
    file_path = Path(prompt("Path to JSON/CSV file (can drag and drop): ").strip().strip('"').strip("'")).expanduser().resolve()
    if not file_path.exists():
        print("File not found!")
        return
    
    tracks = get_file_tracks(file_path)
    if not tracks:
        print("No tracks found in file!")
        return
    else:
        copy_all(sp_user, user_id, [{"uri": uri} for uri in tracks])    


def manage_source(sp_user, user_id, source, source_type):
    meta = get_source_meta(user_id, source, source_type)
    while True:
        try:
            source_tracks = get_source_tracks(sp_user, source, source_type)
        except Exception as e:
            print(f"Error fetching tracks: {e}")
            return

        action = select_from_list(
            title=f"Selected {source_type}: {meta['name']} ({meta['type']})",
            text="Choose an action:",
            options=get_actions_for_source(source_type, meta["playlist_type"]),
        )
        clear_screen()
        if action in (None, "Back"):
            return

        # COPY
        if action == "Copy ALL songs":
            copy_all(sp_user, user_id, source_tracks)
        elif action == "Copy a range of songs":
            copy_range(sp_user, user_id, source_tracks)

        # EXPORT
        elif action == "Export to JSON/CSV":
            export_playlist(source, source_tracks, output_dir=".")
        elif action == "Export a range of songs":
            export_playlist_range(source, source_tracks, output_dir=".")

        # REMOVE
        elif action in ("Delete playlist", "Unfollow playlist", "Unfollow album"):
            remove_playlist_album(sp_user, source, meta["type"].lower())
            return
        elif action == "Remove ALL songs":
            remove_all(sp_user, source, source_tracks)
        elif action == "Remove a range of songs":
            remove_range(sp_user, source, source_tracks)
        
        time.sleep(1)
        clear_screen()
