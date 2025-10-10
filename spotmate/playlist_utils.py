def list_playlists(sp):
    playlists = sp.current_user_playlists(limit=50)['items']
    liked_songs = {"name": "Liked Songs", "id": None, "owner": {"id": sp.current_user()['id']}}
    return [liked_songs] + playlists

def get_playlist_tracks(sp, playlist):
    track_uris = []
    offset = 0

    if playlist['name'] == "Liked Songs":
        while True:
            results = sp.current_user_saved_tracks(limit=50, offset=offset)
            if not results['items']:
                break
            track_uris.extend([t['track']['uri'] for t in results['items']])
            offset += 50
    else:
        pid = playlist['id']
        while True:
            results = sp.playlist_items(pid, limit=100, offset=offset)
            if not results['items']:
                break
            track_uris.extend([item['track']['uri'] for item in results['items'] if item['track']])
            offset += 100

    return track_uris

def copy_songs(sp, source_tracks, dest_name, range_start=None, range_end=None):
    user_id = sp.current_user()['id']
    playlists = sp.current_user_playlists(limit=50)['items']

    dest_playlist = next((p for p in playlists if p['name'].lower() == dest_name.lower()), None)
    if not dest_playlist:
        print(f"Creating playlist '{dest_name}'...")
        dest_playlist = sp.user_playlist_create(user_id, dest_name, public=True)
    pid = dest_playlist['id']

    # Handle range
    if range_start and range_end:
        source_tracks = source_tracks[range_start - 1:range_end]

    for i in range(0, len(source_tracks), 100):
        sp.playlist_add_items(pid, source_tracks[i:i+100])
    print(f"Added {len(source_tracks)} songs to '{dest_name}'.")

def delete_playlist(sp, playlist_name):
    playlists = sp.current_user_playlists(limit=50)['items']
    pl = next((p for p in playlists if p['name'] == playlist_name), None)
    if not pl:
        print("Playlist not found.")
        return
    sp.current_user_unfollow_playlist(pl['id'])
    print(f"Deleted playlist '{playlist_name}'.")

def delete_songs_range(sp, playlist, start, end):
     # Liked Songs have no playlist ID
    if playlist['name'] == "Liked Songs":
        tracks = get_playlist_tracks(sp, playlist)
        if start < 1 or end > len(tracks):
            print("Invalid range.")
            return
        uris_to_remove = tracks[start - 1:end]
        for uri in uris_to_remove:
            sp.current_user_saved_tracks_delete([uri])
        print(f"Removed {len(uris_to_remove)} songs from Liked Songs.")
        return

    # Regular playlists
    pid = playlist['id']
    tracks = get_playlist_tracks(sp, playlist)
    if start < 1 or end > len(tracks):
        print("Invalid range.")
        return

    uris_to_remove = tracks[start - 1:end]
    sp.playlist_remove_all_occurrences_of_items(pid, uris_to_remove)
    print(f"Removed {len(uris_to_remove)} songs from '{playlist['name']}'.")