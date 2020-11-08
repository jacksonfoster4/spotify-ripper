import eyed3
from pydub import AudioSegment

class Audio():
    def __init__(self, collection, tracks):
        # collection is playlist or album
        file_path = 'Illmatic (Full Album).mp3'
        directory_path = 'music'
        self.audio_file = AudioSegment.from_mp3(file_path)
        self.directory_path = directory_path

    def create_new_track(self, title, artist, album, duration, explicit=False):
        # takes snippet from self.audio_file using `duration`
        # export mp3
        # sets id3 data (title, artist, album, album art)
        pass
    
    def upload(self):
        # upload directory to s3
        pass
    
    def record(self):
        pass


