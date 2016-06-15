from .services import *
from .dao import *

def espelhos_sonoros(app, socketio, db):
    root(app)
    oauth(app)

    chat_dao = ChatMessageDAO(db)
    video_dao = VideoPositionDAO(db)

    db.create_all()

    chat(app, socketio, chat_dao, chat_dao.chat_class)
    video(app, socketio, video_dao)
