import math

def video_position(db):
    class VideoPosition(db.Model):
        video_id = db.Column(db.String, primary_key=True)
        x_position = db.Column(db.Float)
        y_position = db.Column(db.Float)

        def __init__(self, video_id, x, y):
            self.video_id = str(video_id)
            self.x_position = float(x)
            self.y_position = float(y)

        def reset(self):
            self.x_position = float(0)
            self.y_position = math.PI / 2

        def __json__(self):
            return {
                'x': self.x_position,
                'y': self.y_position
            }
    return VideoPosition

class VideoPositionDAO(object):
    def __init__(self, db):
        self.video_class = video_position(db)
        self.db = db

    def default_video_position(self, video_id):
        return self.video_class(video_id, '0', '0')

    def get(self, video_id):
        return self.video_class.query.get(video_id) or self.default_video_position(video_id)

    def save(self, position):
        self.db.session.add(position)
        self.db.session.commit()

    def increment(self, video_id, movement):
        position = self.get(video_id)
        position.x_position += movement['x']
        position.y_position += movement['y']
        self.save(position)


