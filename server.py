import time
from flask import Flask, redirect 
from flask import request
import os, re
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from audio import Audio


load_dotenv()


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
    app.spotify.album_tracks('3kEtdS2pH6hKcMU9Wioob1')
    format_url('https://open.spotify.com/album/4EPQtdq6vvwxuYeQTrwDVY?si=YqyoZK1VTpqNkU0cOIZEog')
    return 'album items'

@app.route('/convert')
def convert():
    # get list of collections from front end
    # for collection in collections:
    #   music = get_tracks(url/uri)
    #   add_to_queue(music)
    #   start on track not in queue
    #   skip to first track in queue
        ## this ensures that recording starts at the same time
        ## as playback. 
        #   wait 3 seconds
        #   pause track
        #   rewind
    #   play and begin recording
    list_of_collections = [
        'spotify:album:3kEtdS2pH6hKcMU9Wioob1',
    ]
    for collection_link in list_of_collections:
        music = get_tracks(collection_link)
        add_to_queue(music)
    
    
    app.spotify.next_track()
    time.sleep(4)
    app.spotify.pause_playback()
    app.spotify.seek_track(0)

    print('begin recording', app.spotify.start_playback())

    return 'convert'

def get_runtime(tracks):
    runtime = 0
    for track in tracks:
        runtime += track['duration_ms']
    return runtime
        

def add_to_queue(collection):
    for track in collection['tracks']['items']:
        uri = track['uri']
        #  app.spotify.add_to_queue(uri) 



def get_tracks(url) -> dict:
    """
    takes in playlist/album url, uses the appropriate method to get and return response object
    """
    obj_id: tuple
    if url[:4] == 'http':
        obj_id = get_id_from_url(url) 
    elif url[:7] == 'spotify':
        obj_id = get_id_from_spotify_uri(url) 

    if obj_id[0] == 'album':
        tracks = app.spotify.album_tracks(obj_id[1])
        album = app.spotify.album(obj_id[1])
        return {
            'runtime': get_runtime(tracks['items']),
            'album': album,
            'tracks': tracks
        }
    elif obj_id[0] == 'playlist':
        tracks = app.spotify.playlist_items(obj_id[1])
        playlist = app.spotify.playlist(obj_id[1])
        return {
            'runtime': get_runtime(tracks['items']),
            'playlist': playlist,
            'tracks': tracks,
        }

def format_response(obj):
    """
    returns track name, track artist, track duration, track art, track album, misc info
    """
    final = {

    }
    type_of_collection: str
    # album obj
    if 'album' in obj:
        type_of_collection = 'album'
        final['main_image'] = obj['album']['images'][0]['url']
        final['name'] = obj['album']['name']
        final['release_date'] = obj['album']['release_date']
        final['label'] = obj['album']['label']
        final['artist'] = obj['album']['artists'][0]['name']
        final['tracks'] = obj['tracks']
    elif 'playlist' in obj:
        type_of_collection = 'playlist'
        final['main_image'] = obj['playlist']['images'][0]['url']
        final['name'] = obj['playlist']['name']
        final['tracks'] = obj['tracks']

    return final

def get_id_from_url(url) -> tuple:
    if 'album' in url:
        return ('album', re.search('album/(.*?)\?', url).group(1)) 
    elif 'playlist' in url:
        return ('playlist', re.search('playlist/(.*?)\?', url).group(1)) 

def get_id_from_spotify_uri(url) -> tuple:
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
        # flag to get playlist art
        # test album spotify:album:3kEtdS2pH6hKcMU9Wioob1
    # need to upload files to cloud, then delete
    # open first albumii
