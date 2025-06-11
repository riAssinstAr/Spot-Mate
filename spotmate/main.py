import argparse
import spotipy
import warnings
from spotipy.oauth2 import SpotifyOAuth

warnings.filterwarnings("ignore", category=DeprecationWarning)
# Spotify OAuth setup
def create_spotify_oauth(client_id, client_secret):
    return SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri='http://127.0.0.1:8888/callback',  # Needed for Spotipy
        scope='user-library-read playlist-modify-public playlist-modify-private'
    )

def get_token(client_id, client_secret):
    sp_oauth = create_spotify_oauth(client_id, client_secret)
    token_info = sp_oauth.get_cached_token()

    if not token_info:
        print("Opening browser for Spotify authorization...")
        token_info = sp_oauth.get_access_token()

    return token_info


def transfer_liked_songs_to_playlist(playlist_name='Save', client_id=None, client_secret=None):
    token_info = get_token(client_id, client_secret)
    sp = spotipy.Spotify(auth=token_info['access_token'])
    print("Please wait while processing.....")

    # Get all liked songs URIs
    liked_track_uris = []
    offset = 0
    while True: #Limited to 50 tracks per request
        results = sp.current_user_saved_tracks(limit=50, offset=offset)
        if not results['items']:
            break
        liked_track_uris.extend([item['track']['uri'] for item in results['items']])
        offset += 50

    print(f"Found {len(liked_track_uris)} liked songs.")

    # Find or create the playlist
    playlists = sp.current_user_playlists()['items']
    playlist_id = None

    for playlist in playlists:
        if playlist['name'].lower() == playlist_name.lower():
            playlist_id = playlist['id']
            break

    if not playlist_id:
        print(f"Playlist '{playlist_name}' not found. Creating it...")
        user_id = sp.current_user()['id']
        playlist = sp.user_playlist_create(user_id, playlist_name, public=True)
        playlist_id = playlist['id']

    # Get all track URIs already in the destination playlist
    existing_track_uris = []
    offset = 0
    while True:
        results = sp.playlist_items(playlist_id, offset=offset, fields='items.track.uri,total', additional_types=['track'])
        if not results['items']:
            break
        existing_track_uris.extend([item['track']['uri'] for item in results['items'] if item['track']])
        offset += len(results['items'])

    print(f"Playlist '{playlist_name}' currently has {len(existing_track_uris)} songs.")

    # Only add tracks not already in the playlist
    new_tracks_to_add = list(set(liked_track_uris) - set(existing_track_uris))
    print(f"{len(new_tracks_to_add)} new songs will be added to playlist '{playlist_name}'.")

    if not new_tracks_to_add:
        print("No new songs to add.")
        return

    # Add new tracks to playlist
    for i in range(0, len(new_tracks_to_add), 100):
        sp.playlist_add_items(playlist_id, new_tracks_to_add[i:i+100])

    print(f"Successfully added {len(new_tracks_to_add)} new songs to playlist '{playlist_name}'.")

def main():
    print("** Welcome to the Spotify CLI tool **")

    parser = argparse.ArgumentParser(description="Spotify CLI Tool - Transfer Liked Songs to Playlist")
    parser.add_argument('--transfer', action='store_true', help="Transfer liked Spotify songs to a playlist")
    parser.add_argument('--playlist', nargs='?', type=str, help="Destination playlist name (default: 'Transfer')")
    parser.add_argument('--Client_ID', nargs='?', type=str, help='Client ID for Spotify API authentication.')
    parser.add_argument('--Client_Secret', nargs='?', type=str, help='Client Secret for Spotify API authentication.')

    args = parser.parse_args()

    # Prompt for Playlist Name, Client ID and Client Secret
    if args.playlist is None:
        args.playlist = str(input("Enter the destination playlist name (default: 'Transfer'): ") or 'Transfer')
    if args.Client_ID is None:
        args.Client_ID = str(input("Enter your Client ID: "))
        if not args.Client_ID:
            print("Client ID is required. Exiting.")
            exit(1)
    if args.Client_Secret is None:
        args.Client_Secret = str(input("Enter your Client Secret: "))
        if not args.Client_Secret:
            print("Client Secret is required. Exiting.")
            exit(1)

    if args.transfer:
        transfer_liked_songs_to_playlist(args.playlist, args.Client_ID, args.Client_Secret)
    else:
        print("No valid argument provided. Use --help to see available options.")

if __name__ == "__main__":
    main()