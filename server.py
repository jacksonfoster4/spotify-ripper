from flask import Flask, redirect
from flask import request
import requests, os
from urllib.parse import urlencode
import spotipy
from spotipy.oauth2 import SpotifyOAuth

params = {
    'client_id': os.getenv('CLIENT_ID'),
    'response_type': 'code',
    'redirect_uri': 'localhost:8888/callback'
}
SCOPE = 'user-read-currently-playing user-read-playback-state user-modify-playback-state streaming app-remote-control playlist-modify-private playlist-read-collaborative playlist-read-private playlist-modify-public user-read-recently-played user-read-playback-position user-top-read'

app = Flask(__name__)
app.spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv("SPOTIPY_CLIENT_ID"),
                                                client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
                                                redirect_uri="http://localhost:8880/callback",
                                                scope=SCOPE))
    
@app.route('/play')
def play():
    app.spotify.start_playback()
    return 'hello'

@app.route('/pause')
def pause():
    print(app.spotify.pause_playback())
    return 'hello'