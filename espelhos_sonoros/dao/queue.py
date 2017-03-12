from datetime import datetime

def queue_element(db):
    class QueueElement(db.Model):
        user_id = db.Column(db.String, primary_key=True)
        user_name = db.Column(db.String)
        room = db.Column(db.String)
        entered_queue = db.Column(db.DateTime)
        started_control = db.Column(db.DateTime)

        def __init__(self, user_id, user_name, room, entered_queue):
            self.user_id = user_id
            self.user_name = user_name
            self.entered_queue = entered_queue
            self.room = room
            self.started_control = None

        @property
        def is_controlling(self):
            return self.started_control is not None

        def __str__(self):
            return '<%s.QueueElement - %s>' % (__name__, self.__json__())

        def __repr__(self):
            return self.__str__()

        def __json__(self):
            started_control = self.started_control.isoformat() if self.started_control else None
            return {
                        'id': self.user_id,
                        'name': self.user_name,
                        'room': self.room,
                        'entered_queue': self.entered_queue.isoformat(),
                        'started_control': started_control
                    }

    return QueueElement

class QueueDAO(object):

    def __init__(self, db):
        self.clazz = queue_element(db)
        self.db = db

    def save(self, user_id, user_name, room, entered_queue):
        element = self.clazz(user_id, user_name, room, entered_queue)
        self.db.session.add(element)
        self.db.session.commit()

    def remove(self, user):
        session_user = self.clazz.query.get(user.user_id)
        self.db.session.delete(session_user)
        self.db.session.commit()

    def list_done(self, limit_time):
        dones = self.clazz.query \
            .filter(self.clazz.started_control < limit_time) \
            .all()
        return dones

    def next_candidate(self):
        return self.clazz.query \
            .order_by(self.clazz.entered_queue) \
            .first()

    def list(self, limit):
        return self.clazz.query \
            .order_by(self.clazz.entered_queue) \
            .limit(limit) \
            .all()
