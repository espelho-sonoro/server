def queue_element(db):
    class QueueElement(db.Model):
        user_id = db.Column(db.String, primary_key=True)
        user_name = db.Column(db.String)
        timestamp = db.Column(db.DateTime)

        def __init__(self, user_id, user_name, timestamp):
            self.user_id = user_id
            self.user_name = user_name
            self.timestamp = timestamp

        def __json__(self):
            return {
                    'id': self.user_id,
                    'name': self.user_name,
                    'timestamp': self.timestamp.isoformat()
                    }

    return QueueElement

class QueueDAO(object):

    def __init__(self, db):
        self.clazz = queue_element(db)
        self.db = db

    def save(self, user_id, user_name, timestamp):
        element = self.clazz(user_id, user_name, timestamp)
        self.db.session.add(element)
        self.db.session.commit()


    def list(self, limit=10):
        queue = self.clazz.query \
            .order_by(self.clazz.timestamp) \
            .limit(limit) \
            .all()
        return [ qe.__json__() for qe in queue ]
