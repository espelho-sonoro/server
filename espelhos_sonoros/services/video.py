import flask
import json

def video_service(app, socketio):
    from apiclient import discovery

    youtube = discovery.build("youtube", "v3", developerKey=app.config['GOOGLE_APIKEY'])

    UPLOADS_PLAYLIST = app.config['YOUTUBE_PLAYLIST']

    @app.route('/api/videos', methods=['GET'])
    def list_videos():
        playlist_uploads = youtube.playlistItems().list(
            part='contentDetails',
            playlistId=UPLOADS_PLAYLIST
        ).execute()

        video_ids = map(lambda v: v['contentDetails']['videoId'], playlist_uploads['items'])
        videos = youtube.videos().list(part='snippet,recordingDetails', id=','.join(video_ids)).execute()

        return flask.jsonify(videos)
