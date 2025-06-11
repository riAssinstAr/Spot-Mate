# Spotify CLI Tool

This python script helps the user export all the songs from their Liked Songs playlist into another playlist using Spotify's Web API.

NOTE: You need to have Python and pip installed in your system.

## Installation

```bash
pip install spotmate
```

## IMPORTANT - Before you use the package, you'll need to do the following:

- Login to Spotify Developers [Website](https://developer.spotify.com/) with your spotify account. Go to user dashboard and create an new app. Fill in the required details, Redirect URIs as: http://127.0.0.1:8888/callback , and check the Web API checkbox and save.

- After creating the app, click in the app and go to Settings. From here copy your Client ID and Client Secret. These will be needed for authentication.

## Run Spotmate

```bash
spotmate --transfer --playlist "<playlist_name>"
```

## Run Project Locally

Clone the project

```bash
  git clone https://github.com/riAssinstAr/Spot-Mate.git Spotmate
```

Go to the project directory

```bash
  cd Spotmate
```

Install dependencies

```bash
  pip install setuptools spotipy pytest build twine
```

Build the project

```bash
  python -m build
```

## Acknowledgements

- [Medium](https://medium.com/@luca.pasquarelli.villa/spotify-api-get-your-liked-songs-with-python-and-spotipy-175c2310f0c3)
- [Katia Gilligan Tutorial](https://www.youtube.com/watch?v=mBycigbJQzA&t=1298s)
- [Katia Gilligan Repo](https://github.com/katiagilligan888/Spotify-Discover-Weekly)

## FAQ

- If the package doesn't work as intended or if you'd like to request a new feature to be added, please feel to contact me.

- The main reason for creating this script is to be able to download songs from the Liked Songs since it does not come with a sharing link related to it. The package adds all the songs in users Liked playlist to a new playlist with the name 'Transfer' being the default name. After that the users can use the sharing link of this new playlist to download songs from third-party applications like [Spotify Downloader](https://github.com/WilliamSchack/Spotify-Downloader/releases).
