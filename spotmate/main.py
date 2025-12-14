from prompt_toolkit import prompt
from spotmate.manager import (
    copy_all,
    copy_range,
    export_playlist,
    remove_range,
    remove_playlist,
)
from spotmate.ui import (
    select_from_list,
)
from spotmate.spotify_auth import create_spotify_client
from spotmate.playlist_utils import (
    list_playlists,
    get_playlist_tracks,
)
from spotmate.actions import (
    check_for_update,
    get_playlist_type,
    get_actions_for_type,
)


def manage_playlist(sp_user, user_id, source_playlist):
    print("\nFetching playlist tracks...")
    source_tracks = get_playlist_tracks(sp_user, source_playlist)
    playlist_type = get_playlist_type(source_playlist, user_id)

    while True:
        all_playlists = list_playlists(sp_user)
        writable_playlists = [p for p in all_playlists if p.get("owner", {}).get("id") == user_id]
        writable_names = [p["name"] for p in writable_playlists] + ["Create new playlist", "Cancel"]

        action_choice = select_from_list(
            title=f"\nSelected playlist: {source_playlist['name']} ({playlist_type.upper()})",
            text="Choose an action:",
            options=get_actions_for_type(playlist_type),
        )
        if action_choice in (None, "Back"):
            return
        # COPY ALL
        elif action_choice == "Copy all songs":
            copy_all(writable_names, sp_user, user_id, source_tracks)
        # COPY RANGE
        elif action_choice == "Copy a range of songs":
            copy_range(writable_names, sp_user, user_id, source_tracks)
        # EXPORT
        elif action_choice == "Export to JSON/CSV":
            export_playlist(source_playlist, source_tracks, output_dir=".")
        # DELETE / UNFOLLOW
        elif action_choice in ("Delete playlist", "Unfollow playlist"):
            if remove_playlist(sp_user, source_playlist):
                return
        # DELETE RANGE
        elif action_choice == "Delete a range of songs":
            remove_range(sp_user, source_playlist, source_tracks)


def main():
    print("SpotMate — Spotify Playlist Manager\n")
    print("Documentation & Source Code: https://github.com/riAssinstAr/Spot-Mate\n")
    check_for_update()

    client_id = prompt("Enter your Spotify Client ID: ").strip()
    client_secret = prompt("Enter your Spotify Client Secret: ").strip()
    if not client_id or not client_secret:
        print("Client ID and Secret are required!")
        return

    print("Authenticating with Spotify...")
    sp_user = create_spotify_client(client_id, client_secret)
    user_id = sp_user.current_user()["id"]

    while True:
        print("Fetching your playlists...")
        all_playlists = list_playlists(sp_user)
        playlist_names = [p["name"] for p in all_playlists] + ["Exit"]

        choice = select_from_list(
            title="\nYour playlists",
            text="Choose a playlist to manage:",
            options=playlist_names,
        )
        if choice in (None, "Exit"):
            print("\nGoodbye!")
            break

        playlist_choice = next(p for p in all_playlists if p["name"] == choice)
        manage_playlist(sp_user, user_id, playlist_choice)


if __name__ == "__main__": main()