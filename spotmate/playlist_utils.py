import csv
import json
from prompt_toolkit import prompt


def list_albums(sp_user):
    albums = []
    offset = 0

    while True:
        results = sp_user.current_user_saved_albums(limit=50, offset=offset)
        albums.extend(results["items"])
        if not results["next"]:
            break
        offset += 50

    return [a["album"] for a in albums]


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


def get_source_tracks(sp_user, source, source_type):
    tracks = []
    offset = 0

    # Liked Songs
    if source_type == "playlist" and source["name"] == "Liked Songs":
        while True:
            results = sp_user.current_user_saved_tracks(limit=50, offset=offset)
            items = results["items"]
            if not items:
                break

            tracks.extend(item["track"] for item in items if item.get("track"))
            offset += 50
    # Regular Playlist
    elif source_type == "playlist":
        while True:
            results = sp_user.playlist_items(
                source["id"],
                limit=100,
                offset=offset,
                additional_types=["track"],
            )
            items = results["items"]
            if not items:
                break

            tracks.extend(item["track"] for item in items if item.get("track"))
            offset += 100
    # Album
    elif source_type == "album":
        album_name = source["name"]
        while True:
            results = sp_user.album_tracks(
                source["id"],
                limit=50,
                offset=offset,
            )
            items = results["items"]
            if not items:
                break

            for track in items:
                track["album"] = {"name": album_name}
                tracks.append(track)
            offset += 50

    else:
        raise ValueError(f"Unsupported source type!")

    return tracks


def copy_songs(sp_user, source_tracks, dest_name):
    try:
        dest_playlist = next((p for p in list_playlists(sp_user) if p["name"].lower() == dest_name.lower()), None)
    except Exception as e:
        print(f"Error finding destination playlist: {e}")
        return
    
    try:
        existing_uris = {t["uri"] for t in get_source_tracks(sp_user, dest_playlist, source_type="playlist") if t.get("uri")}
    except Exception as e:
        print(f"Error fetching destination playlist tracks: {e}")
        return

    dedupe = set()
    new_uris = [
        t["uri"]
        for t in source_tracks
        if t.get("uri")
        and t["uri"] not in existing_uris
        and not (t["uri"] in dedupe or dedupe.add(t["uri"]))
    ]
    if not new_uris:
        print("No new songs to add — all tracks already exist!")
        return

    for i in range(0, len(new_uris), 100):
        sp_user.playlist_add_items(dest_playlist["id"], new_uris[i : i + 100])

    print(f"Added {len(new_uris)} songs to '{dest_name}'")


def remove_source(sp_user, source, source_type):
    if source_type == "playlist":
        sp_user.current_user_unfollow_playlist(source["id"])
        print(f"Removed playlist '{source['name']}' from your library?")

    else:
        sp_user.current_user_saved_albums_delete([source["id"]])
        print(f"Removed album '{source['name']}' from your library?")


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


def get_writable_playlists_names(sp_user, user_id):
    try:
        all_playlists = list_playlists(sp_user)
    except Exception as e:
        print(f"Error fetching playlists: {e}")
        return []

    writable_playlists = [p for p in all_playlists if p.get("owner", {}).get("id") == user_id]
    return [p["name"] for p in writable_playlists] + ["Create new playlist", "Cancel"]
