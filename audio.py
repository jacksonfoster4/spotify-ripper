import eyed3
from pathlib import Path
from pydub import AudioSegment

# once a list of albums is submitted, every track is individually added to
# the player queue since i can't actually control what plays next using the api
# then i use the api to play the tracks and record the output at the same time

# multiple albums/playlists will be in the same .mp3/stream so
# i need a way to split the albums from each other
# get total runtime of album/playlist
# split stream into multiple audio segments
# process individual segments
# save

def split_collections(audio_file_path, collections):
    final = []
    audio_file = AudioSegment.from_mp3(audio_file_path)
    last_endpoint = 0
    for collection in collections:
        runtime = collection['runtime']
        audio_segment = audio_file[last_endpoint:last_endpoint+runtime] 
        collection['audio'] = audio_segment
        final.append(collection)
        last_endpoint += runtime
    return final

def split_songs(collection, playlist=False):
    audio_file = collection['audio']
    individual_tracks = []
    last_endpoint = 0
    for track in collection['tracks']:

        end = track['duration_ms'] + last_endpoint
        newAudio = audio_file[last_endpoint:end]

        if playlist:
            cover_art = collection['playlist']['images'][0]['url']
        else:
            cover_art = collection['album']['images'][0]['url']

        formatted_track = {
            'audio': newAudio,
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'album': self.collection['name'],
            'explicit': track['explicit'],
            'cover_art': cover_art,
        }

        individual_tracks.append(formatted_track) 
        last_endpoint += track['duration_ms']

    return individual_tracks



class Audio():
    def __init__(self, collection, tracks):
        # collection is playlist or album
        file_path = 'Illmatic (Full Album).mp3'
        directory_path = 'music'
        self.path = "{}/{}/{}".format(directory_path, collection['artists'][0]['name'], collection['name'])
        Path(self.path).mkdir(parents=True, exist_ok=True)
        self.audio_file = AudioSegment.from_mp3(file_path)
        self.directory_path = directory_path
        self.tracks = tracks['items']
        self.collection = collection
        self.individual_tracks = self.split_collection()
        self.save()

    def save(self):
        for track in self.individual_tracks:

            audio = track['audio']
            final_path = "{}/{}.mp3".format(self.path, track['name'])

            audio.export(final_path, format="mp3")

    def split_collection(self):
        individual_tracks = []
        last_endpoint = 0
        cover_art = self.collection['images'][0]['url']
        for track in self.tracks:

            end = track['duration_ms'] + last_endpoint
            newAudio = self.audio_file[last_endpoint:end]

            formatted_track = {
                'audio': newAudio,
                'name': track['name'],
                'artist': track['artists'][0]['name'],
                'album': self.collection['name'],
                'explicit': track['explicit'],
                'cover_art': cover_art,
            }

            individual_tracks.append(formatted_track) 
            last_endpoint += track['duration_ms']

        return individual_tracks
    

    def upload(self):
        # upload directory to s3
        pass
    
    def record(self):
        pass


