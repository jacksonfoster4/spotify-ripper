from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests, os

load_dotenv()

    
SCOPE = 'user-read-currently-playing user-read-playback-state user-modify-playback-state streaming app-remote-control playlist-modify-private playlist-read-collaborative playlist-read-private playlist-modify-public user-read-recently-played user-read-playback-position user-top-read'

def main():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv("SPOTIPY_CLIENT_ID"),
                                               client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
                                               redirect_uri="localhost:8888/",
                                               scope=SCOPE))
    sp.current_user()



if __name__ == '__main__':
    main()

