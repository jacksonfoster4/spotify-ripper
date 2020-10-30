from flask import Flask, redirect
from flask import request
import requests, os
from urllib.parse import urlencode
import spotipy
from spotipy.oauth2 import SpotifyOAuth

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
    app.spotify.pause_playback()
    return 'hello'

if __name__ == "__main__":
    app.run()

# algorithm
    # need to record audio output and then trim each individual track from stream
        # i need to use spotify api to start playing an album/playlist, get list of tracks in album/playlist, 
        # get track info, get track length
        # record audio input to .wav
        # using the track lengths, split the .wav file into individual tracks
        # update individual track info (artist, album, art, etc...)
