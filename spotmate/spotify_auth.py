import spotipy
from spotipy.oauth2 import SpotifyOAuth


SCOPES = (
    "user-library-read "
    "user-library-modify "
    "playlist-read-private "
    "playlist-modify-private "
    "playlist-modify-public"
)


def create_spotify_client(client_id, client_secret):
    oauth = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri="http://127.0.0.1:8888/callback",
        scope=SCOPES,
        open_browser=True,
        cache_path=".spotmate_cache",
    )

    token_info = oauth.get_cached_token()
    if not token_info:
        print("\nOpening browser for Spotify authorization...\n")
        token_info = oauth.get_access_token()
    if oauth.is_token_expired(token_info):
        token_info = oauth.refresh_access_token(token_info["refresh_token"])

    return spotipy.Spotify(auth=token_info["access_token"])
