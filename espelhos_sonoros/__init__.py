from .controllers import *
from .dao import *
from .services import *

def espelhos_sonoros(app, socketio, db):
    root(app)
    oauth(app)

    chat_dao = ChatMessageDAO(db)
    video_dao = VideoPositionDAO(db)
    queue_dao = QueueDAO(db)

    queue_controller = QueueController(app, socketio, queue_dao)
    queue_controller.start_dequeing()

    db.create_all()

    chat(app, socketio, chat_dao, chat_dao.chat_class)
    video(app, socketio, video_dao)
    queue(app, queue_controller)
