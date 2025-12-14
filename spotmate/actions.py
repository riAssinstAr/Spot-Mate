import requests
from packaging import version
from spotmate.playlist_utils import create_new_playlist
from spotmate.ui import select_from_list

CURRENT_VERSION = "2.0.0"
PACKAGE_NAME = "spotmate"


def check_for_update():
    try:
        resp = requests.get(f"https://pypi.org/pypi/{PACKAGE_NAME}/json", timeout=5)
        resp.raise_for_status()
        latest = resp.json()["info"]["version"]

        if version.parse(latest) > version.parse(CURRENT_VERSION):
            print(f"A newer version of SpotMate is available: {latest} (you have {CURRENT_VERSION})")
            print(f"Upgrade with: pip install --upgrade {PACKAGE_NAME}\n")
    except Exception:
        pass


def get_playlist_type(playlist, user_id):
    if playlist["name"] == "Liked Songs":
        return "liked"
    elif playlist.get("owner", {}).get("id") == user_id:
        return "private"
    else:
        return "public"


def get_actions_for_type(playlist_type):
    if playlist_type == "liked":
        return [
            "Copy all songs",
            "Copy a range of songs",
            "Delete a range of songs",
            "Export to JSON/CSV",
            "Back",
        ]
    elif playlist_type == "private":
        return [
            "Copy all songs",
            "Copy a range of songs",
            "Delete playlist",
            "Delete a range of songs",
            "Export to JSON/CSV",
            "Back",
        ]
    else:  # public
        return [
            "Copy all songs",
            "Copy a range of songs",
            "Export to JSON/CSV",
            "Unfollow playlist",
            "Back",
        ]


def get_destination(writeable_names, sp_user, user_id):
    dest_playlist = select_from_list(
            title="Destination Playlist",
            text="Select the playlist to copy songs into:",
            options=writeable_names
        )
    if dest_playlist == "Create new playlist":
        dest_playlist = create_new_playlist(sp_user, user_id)

    return dest_playlist


def serialize_track(track):
    return {
        "name": track["name"],
        "artists": ", ".join(a["name"] for a in track["artists"]),
        "album": track["album"]["name"],
        "uri": track["uri"],
    }
