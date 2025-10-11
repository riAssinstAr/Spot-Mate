<p align="center">
  <img src="logo.png" alt="Spotify CLI Tool Logo" width="200"/>
</p>
<h1 align="center">Spotify Manager</h1>
<p align="center">
  A command line tool that helps users manage their Spotify playlists.
</p>
<br>

# IMPORTANT - Before you use the package, you'll need to do the following:

- Login to Spotify Developers [Website](https://developer.spotify.com/) with your spotify account. Go to user dashboard and create an new app.
- Fill in the required details, Redirect URIs as: http://127.0.0.1:8888/callback. Then check the Web API checkbox and save.
- After creating the app, click in the app and go to Settings. From here copy your Client ID and Client Secret. These will be needed for authentication.
- Install python and pip in your system.

### Installation

```bash
pip install spotmate
```

### Usage

```bash
spotmate
```

# Run Project Locally

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

## FAQ

- If the package doesn't work as intended or if you'd like to request a new feature to be added, please feel to contact me or create a PR.

- This script was made to allow users to share the Liked Songs playlist since it does not come with a sharing link related to it. The package adds all the songs in users Liked playlist to a new playlist.
