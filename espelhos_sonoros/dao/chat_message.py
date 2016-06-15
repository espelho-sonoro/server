import uuid
from datetime import datetime

def chat_message(db):
    class ChatMessage(db.Model):
        uuid = db.Column(db.String, primary_key=True)
        user_id = db.Column(db.String)
        date = db.Column(db.DateTime)
        message = db.Column(db.Text)

        def __init__(self, user_id, date, message):
            self.uuid = str(uuid.uuid4())
            self.user_id = user_id
            self.date = date
            self.message = message

        def __json__(self):
            return {
                'user': self.user_id,
                'date': self.date.isoformat(),
                'text': self.message
            }

    return ChatMessage

class ChatMessageDAO(object):
    def __init__(self, db):
        self.chat_class = chat_message(db)
        self.db = db

    def save(self, chat_message):
        self.db.session.add(chat_message)
        self.db.session.commit()

    def list(self, limit=10):
        return self.chat_class.query.limit(limit).all()
