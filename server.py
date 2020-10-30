from flask import Flask, redirect
from flask import request
import os, re
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
    return 'play'

@app.route('/pause')
def pause():
    app.spotify.pause_playback()
    return 'pause'

@app.route('/now-playing')
def now_playing():
    print(app.spotify.current_playback())
    return 'now playing'

@app.route('/playlist-items')
def playlist_items():
    app.spotify.playlist_items('7bzrB54qTMgvLbeuusJlOJ')
    return 'playlist items'

@app.route('/album-tracks')
def album_tracks():
    app.spotify.album_tracks('4EPQtdq6vvwxuYeQTrwDVY')
    format_url('https://open.spotify.com/album/4EPQtdq6vvwxuYeQTrwDVY?si=YqyoZK1VTpqNkU0cOIZEog')
    return 'album items'

        
def get_tracks(url):
    """
    takes in playlist/album url, uses the appropriate method to get response object
    """
    obj_id: tuple
    if url[:4] == 'http':
        obj_id = get_id_from_url(url) 
    elif url[:7] == 'spotify':
        obj_id = get_id_from_spotify_uri(url) 

    if obj_id[0] == 'album':
        return app.spotify.album_tracks(obj_id[1])
    elif obj_id[0] == 'playlist':
        return app.spotify.playlist_items(obj_id[1])


def format_response(url):
    """
    returns track name, track artist, track duration, track art, track album, misc info
    """
    pass

def get_id_from_url(url):
    if 'album' in url:
        return ('album', re.search('album/(.*?)\?', url).group(1)) 
    elif 'playlist' in url:
        return ('playlist', re.search('playlist/(.*?)\?', url).group(1)) 

def get_id_from_spotify_uri(url):
    if 'album' in url:
        return ('album', url.split(':')[2]) 
    elif 'playlist' in url:
        return ('playlist', url.split(':')[2]) 

if __name__ == "__main__":
    app.run()

# algorithm
    # need web interface to add playlists/albums to queue
    # need to record audio output and then trim each individual track from stream
        # i need to use spotify api to start playing an album/playlist, get list of tracks in album/playlist, 
        # get track info, get track length
        # record audio input to .wav
        # using the track lengths, split the .wav file into individual tracks
        # update individual track info (artist, album, art, etc...)
        # spotify:playlist:7bzrB54qTMgvLbeuusJlOJ
        # spotify:album:4EPQtdq6vvwxuYeQTrwDVY
    # need to upload files to cloud, then delete
