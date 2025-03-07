# import necessary modules
import json
import time

import spotipy
from flask import Flask, request, url_for, session, redirect
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support.wait import WebDriverWait
from spotipy.oauth2 import SpotifyOAuth

# initialize Flask app
app = Flask(__name__)

# set the name of the session cookie
app.config['SESSION_COOKIE_NAME'] = 'Spotify Cookie'

# set a random secret key to sign the cookie
app.secret_key = 'YOUR_SECRET_KEY'

# set the key for the token info in the session dictionary
TOKEN_INFO = 'token_info'

# Setup Firefox WebDriver
firefox_options = Options()
firefox_options.add_argument("--headless")  # Comment this line out to see the UI
firefox_options.set_preference("dom.webdriver.enabled", False)  # Hide WebDriver
firefox_options.set_preference("useAutomationExtension", False)
service = FirefoxService(executable_path="PATH_TO_GECKODRIVER")  # Path to GeckoDriver
driver = webdriver.Firefox(service=service, options=firefox_options)

# Install uBlock Origin
driver.install_addon("./uBlock0.firefox.signed.xpi", temporary=True) # Path to uBlock Origin

# Open the website SpotMate
driver.get('https://spotmate.online/en')

# route to handle logging in
@app.route('/')
def login():
    # create a SpotifyOAuth instance and get the authorization URL
    auth_url = create_spotify_oauth().get_authorize_url()
    # redirect the user to the authorization URL
    return redirect(auth_url)


# route to handle the redirect URI after authorization
@app.route('/redirect')
def redirect_page():
    # clear the session
    session.clear()
    # get the authorization code from the request parameters
    code = request.args.get('code')
    # exchange the authorization code for an access token and refresh token
    token_info = create_spotify_oauth().get_access_token(code)
    # save the token info in the session
    session[TOKEN_INFO] = token_info
    # redirect the user to the save_discover_weekly route
    return redirect(url_for('save_liked_songs', _external=True))


# route to save the Discover Weekly songs to a playlist
@app.route('/saveLikedSongs')
def save_liked_songs():
    try:
        # get the token info from the session
        token_info = get_token()
    except:
        # if the token info is not found, redirect the user to the login route
        print('User not logged in')
        return redirect("/")

    # create a Spotipy instance with the access token
    sp = spotipy.Spotify(auth=token_info['access_token'])

    # get the songs
    response = {}
    i = 0
    try:
        if sp:
            while i < 1000:
                j = i
                sp = spotipy.Spotify(auth=token_info['access_token'])
                # Spotify Web API only allows for a max of 50 items at a time
                results = sp.current_user_saved_tracks(offset=i, limit=50)
                for item in results["items"]:
                    # This line only saves track URLs, to save other details please refer to Spotify Web API
                    response[j] = item["track"]["external_urls"]["spotify"]
                    j += 1
                i += 50

    except Exception as e:
        print(f"There was an error: {str(e)}")
        return 'There was am error. Check console.'

    # dump to json
    with open('data.json', 'w') as fp:
        json.dump(response, fp)

    v = ""
    try:
        # Send data to the search box, press Enter to submit the search, then Download
        for key,value in response.items():
            print(f"Working on song index: {key}")
            v = value
            search_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "trackUrl"))
            )
            search_box.click()
            search_box.send_keys(value)
            search_box.send_keys(Keys.RETURN)
            #
            button1 = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "btn-success"))
            )
            time.sleep(5)
            driver.execute_script("arguments[0].scrollIntoView();", button1)  # Scroll to button
            time.sleep(5)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "btn-success"))).click()
            time.sleep(5)
            #
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[text()='Download']"))
            )
            time.sleep(5)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Download']"))).click()
            time.sleep(5)
            #
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[text()='Download Another Song']"))
            )
            time.sleep(5)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Download Another Song']"))).click()
            time.sleep(5)

    except Exception as e:
        print(f"There was an error: {str(e)}")
        k = [key for key, val in response.items() if val == v]
        print(f"The index of the song the threw error: {k}")
        return 'There was am error. Check console.'

    # return a success message
    return 'Liked Songs downloaded successfully.'


# function to get the token info from the session
def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        # if the token info is not found, redirect the user to the login route
        redirect(url_for('login', _external=False))

    # check if the token is expired and refresh it if necessary
    now = int(time.time())

    is_expired = token_info['expires_at'] - now < 60
    if is_expired:
        spotify_oauth = create_spotify_oauth()
        token_info = spotify_oauth.refresh_access_token(token_info['refresh_token'])

    return token_info


def create_spotify_oauth():
    return SpotifyOAuth(
        client_id='YOUR_CLIENT_ID',
        client_secret='YOUR_CLIENT_SECRET',
        redirect_uri=url_for('redirect_page', _external=True),
        scope='user-library-read'
    )


app.run(debug=True)