from spotmate.spotify_auth import create_spotify_client
from spotmate.actions import confirm_action, choose_from_list
from spotmate.playlist_utils import (
    list_playlists, get_playlist_tracks,
    copy_songs, delete_playlist, delete_songs_range
)

def get_playlist_type(playlist, user_id):
    if playlist['name'] == "Liked Songs":
        return "liked"
    elif playlist.get('owner', {}).get('id') == user_id:
        return "private"
    else:
        return "public"


def get_actions_for_type(playlist_type):
    if playlist_type == "liked":
        return [
            "Copy all songs to another playlist",
            "Copy a range of songs to another playlist",
            "Delete a range of songs from this playlist",
            "Go back to playlists"
        ]
    elif playlist_type == "private":
        return [
            "Copy all songs to another playlist",
            "Copy a range of songs to another playlist",
            "Delete this playlist",
            "Delete a range of songs from this playlist",
            "Go back to playlists"
        ]
    elif playlist_type == "public":
        return [
            "Copy all songs to another playlist",
            "Copy a range of songs to another playlist",
            "Unfollow this playlist",
            "Go back to playlists"
        ]


def manage_playlist(sp, playlist, user_id):
    name = playlist["name"]
    ptype = get_playlist_type(playlist, user_id)
    actions = get_actions_for_type(ptype)

    print(f"\nManaging: {name}  |  Type: {ptype.upper()}")
    action = choose_from_list(actions)

    if "Go back to playlists" in action:
        return
    # ---- COPY ALL SONGS ----
    elif "Copy all" in action:
        dest = input("Enter destination playlist name: ")
        if confirm_action(f"Copy ALL songs from '{name}' to '{dest}'?"):
            tracks = get_playlist_tracks(sp, playlist)
            copy_songs(sp, tracks, dest)
    # ---- COPY RANGE ----
    elif "Copy a range" in action:
        start = int(input("Start index: "))
        end = int(input("End index: "))
        dest = input("Enter destination playlist name: ")
        if confirm_action(f"Copy songs {start}-{end} from '{name}' to '{dest}'?"):
            tracks = get_playlist_tracks(sp, playlist)
            copy_songs(sp, tracks, dest, start, end)
    # ---- DELETE PLAYLIST ----
    elif "Delete this playlist" or "Unfollow this playlist" in action:
        if confirm_action(f"Delete playlist '{name}' from your library?"):
            delete_playlist(sp, name)
    # ---- DELETE SONG RANGE ----
    elif "Delete a range of songs" in action and ptype in ["private", "liked"]:
        start = int(input("Start index: "))
        end = int(input("End index: "))
        if confirm_action(f"Delete songs {start}-{end} from '{name}'?"):
            delete_songs_range(sp, playlist, start, end)

    print("Action complete. Returning to playlist menu...")


def main():
    print("🎵 ** Welcome to SpotMate - Your Spotify CLI Companion ** 🎵\n")

    client_id = input("Enter your Spotify Client ID: ").strip()
    client_secret = input("Enter your Spotify Client Secret: ").strip()

    if not client_id or not client_secret:
        print("Client ID and Secret are required. Exiting.")
        return

    sp = create_spotify_client(client_id, client_secret)
    user = sp.current_user()
    user_id = user['id']

    while True:
        print("\nFetching your playlists...")
        playlists = list_playlists(sp)
        playlist_names = [p['name'] for p in playlists] + ["Exit"]

        name_choice = choose_from_list(playlist_names)
        if name_choice == "Exit":
            print("Goodbye!")
            break

        playlist_choice = next((p for p in playlists if p['name'] == name_choice), None)
        if not playlist_choice:
            print("Invalid selection.")
            continue

        manage_playlist(sp, playlist_choice, user_id)


if __name__ == "__main__":
    main()