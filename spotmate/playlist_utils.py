import csv
import json
from prompt_toolkit import prompt


def list_playlists(sp_user):
    playlists = []
    offset = 0

    while True:
        results = sp_user.current_user_playlists(limit=50, offset=offset)
        playlists.extend(results["items"])
        if not results["next"]:
            break
        offset += 50

    liked = {"name": "Liked Songs", "id": None, "owner": {"id": sp_user.current_user()["id"]}}
    return [liked] + playlists


def get_playlist_tracks(sp_user, playlist):
    tracks = []
    offset = 0

    if playlist["name"] == "Liked Songs":
        while True:
            results = sp_user.current_user_saved_tracks(limit=50, offset=offset)
            if not results["items"]:
                break

            tracks.extend(t["track"] for t in results["items"] if t["track"])
            offset += 50
    else:
        while True:
            results = sp_user.playlist_items(playlist["id"], limit=100, offset=offset)
            if not results["items"]:
                break

            tracks.extend(t["track"] for t in results["items"] if t["track"])
            offset += 100

    return tracks


def copy_songs(sp_user, source_tracks, dest_name):
    all_playlists = list_playlists(sp_user)
    dest = next((p for p in all_playlists if p["name"].lower() == dest_name.lower()), None)
    if not dest:
        print("Destination playlist not found!")
        return

    # Fetch destination playlist tracks
    dest_tracks = get_playlist_tracks(sp_user, dest)
    existing_uris = {track["uri"] for track in dest_tracks}
    source_uris = [track["uri"] for track in source_tracks if track.get("uri")]

    # Remove duplicates
    unique_source_uris = list(dict.fromkeys(source_uris))
    new_uris = [uri for uri in unique_source_uris if uri not in existing_uris]
    if not new_uris:
        print("No new songs to add — all tracks already exist!")
        return

    for i in range(0, len(new_uris), 100):
        sp_user.playlist_add_items(dest["id"], new_uris[i : i + 100])

    print(f"Added {len(new_uris)} songs to '{dest_name}'")


def delete_playlist(sp_user, playlist):
    sp_user.current_user_unfollow_playlist(playlist["id"])
    print(f"Removed playlist '{playlist['name']}' from your library")


def delete_songs_range(sp_user, source_playlist, source_tracks):
    uris = [t["uri"] for t in source_tracks if t.get("uri")]

    # Liked Songs
    if source_playlist["name"] == "Liked Songs":
        for i in range(0, len(uris), 50):
            sp_user.current_user_saved_tracks_delete(uris[i : i + 50])

        print(f"Removed {len(uris)} songs from Liked Songs")
        return
    # Regular playlist
    else:
        for i in range(0, len(uris), 100):
            sp_user.playlist_remove_all_occurrences_of_items(source_playlist["id"], uris[i : i + 100])

        print(f"Removed {len(uris)} songs from '{source_playlist['name']}'")
        return


def export_tracks(tracks, path, file_format):
    if file_format == "JSON":
        with open(path, "w", encoding="utf-8") as f:
            json.dump(tracks, f, indent=2, ensure_ascii=False)
    elif file_format == "CSV":
        with open(path, "w", encoding="utf-8", newline="") as f:
            fieldnames = ["name", "artists", "album", "uri"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(tracks)


def create_new_playlist(sp_user, user_id):
    print()
    playlist_name = prompt("New playlist name: ").strip()
    if not playlist_name:
        print("Playlist name cannot be empty!")
        return None

    try:
        sp_user.user_playlist_create(user_id, playlist_name, public=True)
        print(f"Created playlist '{playlist_name}'")
        return playlist_name
    except Exception as e:
        print(f"Error creating playlist: {e}")
        return None
