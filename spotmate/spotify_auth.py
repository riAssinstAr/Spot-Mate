import spotipy
from spotipy.oauth2 import SpotifyOAuth

def create_spotify_client(client_id, client_secret):
    sp_oauth = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri="http://127.0.0.1:8888/callback",
        scope="user-library-read user-library-modify playlist-read-private playlist-modify-private playlist-modify-public"
    )

    token_info = sp_oauth.get_cached_token()
    if not token_info:
        print("Opening browser for Spotify authorization...")
        token_info = sp_oauth.get_access_token()

    return spotipy.Spotify(auth=token_info["access_token"])
