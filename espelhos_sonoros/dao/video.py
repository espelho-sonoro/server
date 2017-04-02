from apiclient import discovery
from collections import namedtuple

VideoInfo = namedtuple('VideoInfo', ['id', 'title', 'desc', 'url', 'lat', 'lng'])

class VideoDAO(object):

    def __init__(self, config):
        self.youtube = discovery.build("youtube", "v3", developerKey=config['GOOGLE_APIKEY'])
        self.playlist_id = config['YOUTUBE_PLAYLIST']

    def __youtube_2_video__(self, youtube_video):
        video_id = youtube_video['id']
        video_url = 'https://youtube.com/watch?v=' + video_id

        title = youtube_video['snippet'].get('title')
        video_desc = youtube_video['snippet'].get('description')

        recording_details = youtube_video.get('recordingDetails') or {}
        location = recording_details.get('location') or {}
        latitude = location.get('latitude')
        longitude = location.get('longitude')

        return VideoInfo(video_id, title, video_desc, video_url, latitude, longitude)


    def list(self):
        playlist_uploads = self.youtube.playlistItems() \
                .list(part='contentDetails', playlistId=self.playlist_id) \
                .execute()

        video_ids = map(lambda v: v['contentDetails']['videoId'], playlist_uploads['items'])

        youtube_videos = self.youtube.videos() \
            .list(part='snippet,recordingDetails', id=','.join(video_ids)) \
            .execute()

        return map(lambda v: self.__youtube_2_video__(v), youtube_videos['items'])

