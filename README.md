
# Spotify Download Automation

This python script helps the user export the URLs of and download all songs from their Liked Songs playlist from the website [Spotmate](https://spotmate.online/en) using Selenium automation with Firefox's Geckodriver. In this script we have also used uBlock Origin extension addon since popups and ads can hinder with the automation process.




## Run Locally

Download and install Firefox browser from [here](https://www.mozilla.org/en-US/firefox/new/)

Download and add PATH to Geckodriver, Downlaod Link [here](https://github.com/mozilla/geckodriver/releases), Youtube tutorial to add PATH for Webdrivers [here](https://www.youtube.com/watch?v=dz59GsdvUF8). Place the Geckodriver inside the 'webdrivers' folder which you have added to PATH.

Download and install Python following the instructions from [here](https://www.python.org/downloads/)

Installing Python should automatically install 'pip' but in case it does not, you can install it manually following the instructions from [here](https://pip.pypa.io/en/stable/installation/)

Clone the project

```bash
  git clone https://github.com/riAs-g/Spot-Down
```

Go to the project directory

```bash
  cd my-project
```

Install Flask Spotipy

```bash
  pip install flask spotipy
```

Install Selenium

```bash
  pip install selenium 
```

Before you start the server, you'll need to do the following:

* Login to Spotify Developers [website](https://developer.spotify.com/) with your spotify account. Go to user dashboard and create an new app. Fill in the required details, Redirect URIs as: http://127.0.0.1:5000/redirect , and check the Web API checkbox and save.

* After creating the app, click in the app and go to Settings. From here copy your Client ID and Client Secret.

Start the server

```bash
  python Spotdown.py
```

