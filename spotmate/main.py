import time
from prompt_toolkit import prompt
from spotmate.spotify_auth import create_spotify_client
from spotmate.manager import (
    import_playlist,
    manage_source,
)
from spotmate.ui import (
    select_from_list,
)
from spotmate.playlist_utils import (
    create_new_playlist,
    list_albums,
    list_playlists,
)
from spotmate.actions import (
    check_for_update,
    clear_screen,
    select_source_type,
)


def manage_album(sp_user, user_id):
    while True:
        try:
            albums = list_albums(sp_user)
        except Exception as e:
            print(f"Error fetching albums: {e}")
            return

        options = ["Back"] + [a["name"] for a in albums]
        choice = select_from_list(
            title="Your Albums",
            text="Choose an album:",
            options=options,
        )
        clear_screen()
        if choice in (None, "Back"):
            return

        album = next(a for a in albums if a["name"] == choice)
        manage_source(sp_user, user_id, album, source_type="album")
        clear_screen()


def manage_playlist(sp_user, user_id):
    while True:
        try:
            playlists = list_playlists(sp_user)
        except Exception as e:
            print(f"Error fetching playlists: {e}")
            return

        options = ["Back", "Create new playlist", "Import from JSON/CSV"] + [p["name"] for p in playlists]
        choice = select_from_list(
            title="Your Playlists",
            text="Choose a playlist:",
            options=options,
        )
        clear_screen()
        if choice in (None, "Back"):
            return
        elif choice == "Create new playlist":
            create_new_playlist(sp_user, user_id)
        elif choice == "Import from JSON/CSV":
            import_playlist(sp_user, user_id)
        else:
            playlist = next(p for p in playlists if p["name"] == choice)
            manage_source(sp_user, user_id, playlist, source_type="playlist")
        time.sleep(1)
        clear_screen()


def main():
    print("SpotMate — Spotify Manager\n")
    print("Documentation & Source Code: https://github.com/riAssinstAr/Spot-Mate\n")
    check_for_update()

    client_id = prompt("Enter your Spotify Client ID: ").strip()
    client_secret = prompt("Enter your Spotify Client Secret: ").strip()
    if not client_id or not client_secret:
        print("Client ID and Secret are required!")
        return

    print("Authenticating with Spotify...")
    try:
        sp_user = create_spotify_client(client_id, client_secret)
        user_id = sp_user.current_user()["id"]
    except Exception as e:
        print(f"Authentication failed: {e}")
        print("Please check your Client ID and Secret and try again.")
        return

    clear_screen()
    while True:
        source_type = select_source_type()
        clear_screen()
        if source_type in (None, "Exit"):
            break

        if source_type == "Playlists":
            manage_playlist(sp_user, user_id)
        elif source_type == "Albums":
            manage_album(sp_user, user_id)


if __name__ == "__main__": main()