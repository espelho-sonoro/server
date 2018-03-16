def video_info(db):
    class VideoInfo(db.Model):
        video_id = db.Column(db.String, primary_key=True)
        bandcamp_track_id = db.Column(db.String)
        bandcamp_album_id = db.Column(db.String)
        rec_latitude = db.Column(db.String)
        rec_longitude = db.Column(db.String)

    def __init__(self, video_id, bandcamp_track_id, bandcamp_album_id, rec_latitude, rec_longitude):
        self.video_id = video_id
        self.bandcamp_track_id = bandcamp_track_id
        self.bandcamp_album_id = bandcamp_album_id
        self.rec_latitude = rec_latitude
        self.rec_longitude = rec_longitude

    return VideoInfo

class VideoInfoDAO(object):

    def __init__(self, db):
        self.clazz = video_info(db)
        self.db = db

    def save(self, video_id, bandcamp_track_id, bandcamp_album_id, rec_latitude, rec_longitude):
        element = self.clazz(video_id, bandcamp_album_id, bandcamp_track_id, rec_latitude, rec_longitude)
        self.db.session.add(element)
        self.db.session.commit()

    def get(self, video_id):
        return self.clazz.query.get(video_id)

