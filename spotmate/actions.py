import csv
import json
import os
import requests
from packaging import version
from spotmate.playlist_utils import create_new_playlist, get_writable_playlists_names
from spotmate.ui import select_from_list


CURRENT_VERSION = "2.0.0"
PACKAGE_NAME = "spotmate"


def check_for_update():
    try:
        response = requests.get(f"https://pypi.org/pypi/{PACKAGE_NAME}/json", timeout=5)
        response.raise_for_status()
        latest_ver = response.json()["info"]["version"]

        if version.parse(latest_ver) > version.parse(CURRENT_VERSION):
            print(f"A newer version of SpotMate is available: {latest_ver} (you have {CURRENT_VERSION})")
            print(f"Upgrade with: pip install --upgrade {PACKAGE_NAME}\n")
    except Exception:
        pass


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def get_playlist_type(user_id, source_playlist):
    if source_playlist["name"] == "Liked Songs":
        return "liked"
    elif source_playlist.get("owner", {}).get("id") == user_id:
        return "private"
    else:
        return "public"


def get_actions_for_playlist(playlist_type):
    if playlist_type == "liked":
        return [
            "Copy ALL songs",
            "Copy a range of songs",
            "Export to JSON/CSV",
            "Export a range of songs",
            "Remove ALL songs",
            "Remove a range of songs",
            "Back",
        ]
    elif playlist_type == "private":
        return [
            "Copy ALL songs",
            "Copy a range of songs",
            "Export to JSON/CSV",
            "Export a range of songs",
            "Remove ALL songs",
            "Remove a range of songs",
            "Delete playlist",
            "Back",
        ]
    else:  # public
        return [
            "Copy ALL songs",
            "Copy a range of songs",
            "Export to JSON/CSV",
            "Export a range of songs",
            "Unfollow playlist",
            "Back",
        ]


def get_actions_for_album():
    return [
        "Copy ALL songs",
        "Copy a range of songs",
        "Export to JSON/CSV",
        "Export a range of songs",
        "Unfollow album",
        "Back",
    ]


def get_destination(sp_user, user_id):
    writable_names = get_writable_playlists_names(sp_user, user_id)

    dest_playlist = select_from_list(
            title="Destination Playlist",
            text="Select the playlist to copy songs into:",
            options=writable_names
        )
    clear_screen()
    if dest_playlist == "Create new playlist":
        try:
            dest_playlist = create_new_playlist(sp_user, user_id)
        except Exception as e:
            print(f"Error creating a new playlist: {e}")
            return None

    return dest_playlist


def serialize_tracks(tracks):
    return {
        "name": tracks["name"],
        "artists": ", ".join(item["name"] for item in tracks["artists"]),
        "album": tracks["album"]["name"],
        "uri": tracks["uri"],
    }


def select_source_type():
    return select_from_list(
        title="What would you like to manage?",
        text="",
        options=["Playlists", "Albums", "Exit"],
    )


def get_source_meta(user_id, source, source_type):
    return {
        "name": source["name"],
        "type": source_type.upper(),
        "playlist_type": (
            get_playlist_type(user_id, source)
            if source_type == "playlist"
            else None
        ),
    }


def get_actions_for_source(source_type, playlist_type=None):
    if source_type == "playlist":
        return get_actions_for_playlist(playlist_type)

    if source_type == "album":
        return get_actions_for_album()

    raise ValueError("Unknown source type!")


def get_file_tracks(file_path):
    if file_path.suffix.lower() == ".json":
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [t["uri"] for t in data if "uri" in t]
    elif file_path.suffix.lower() == ".csv":
        with open(file_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return [row["uri"] for row in reader if "uri" in row]
    else:
        print("Unsupported file format! Use JSON or CSV.")
        return None
