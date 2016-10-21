from datetime import datetime, timedelta

def queue_element(db):
    class QueueElement(db.Model):
        user_id = db.Column(db.String, primary_key=True)
        user_name = db.Column(db.String)
        entered_queue = db.Column(db.DateTime)
        started_control = db.Column(db.DateTime)

        def __init__(self, user_id, user_name, entered_queue):
            self.user_id = user_id
            self.user_name = user_name
            self.entered_queue = entered_queue
            self.started_control = None

        def __json__(self):
            started_control = self.started_control.isoformat() if self.started_control else None
            return {
                    'id': self.user_id,
                    'name': self.user_name,
                    'entered_queue': self.entered_queue.isoformat(),
                    'started_control': started_control
                    }

    return QueueElement

class QueueDAO(object):

    def __init__(self, db):
        self.clazz = queue_element(db)
        self.db = db

    def save(self, user_id, user_name, entered_queue):
        element = self.clazz(user_id, user_name, entered_queue)
        self.db.session.add(element)
        self.db.session.commit()

    def clear_done(self, minutes):
        limit_time = datetime.now() - timedelta(minutes=minutes)
        dones = self.clazz.query \
            .filter(self.clazz.started_control < limit_time) \
            .all()
        for done in dones:
            self.db.session.delete(done)
        self.db.session.commit()
        return dones

    def head(self):
        return self.clazz.query \
            .order_by(self.clazz.entered_queue) \
            .first()

    def dequeue(self):
        head = self.head()
        if head:
            self.db.session.delete(head)
            self.db.session.commit()
        return head

    def list(self, limit=10):
        return self.clazz.query \
            .order_by(self.clazz.entered_queue) \
            .limit(limit) \
            .all()
