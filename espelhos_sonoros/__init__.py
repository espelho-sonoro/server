from .controllers import *
from .dao import *
from .services import *
from .workers import *
from .utils import *

def espelhos_sonoros(app, socketio, db):
    app.logger.info('Creating application.')
    queue_dao = QueueDAO(db)
    video_dao = VideoDAO(app.config)

    app.logger.info('Created models')
    db.create_all()

    app.logger.info('Created database')
    queue_controller = QueueController(app, socketio, queue_dao)
    camera_controller = object()

    app.logger.info('Created controllers')
    queue_worker = QueueWorker(app, socketio, queue_controller)

    app.logger.info('Created workers')
    templates_service(app)
    oauth_service(app)
    queue_service(app, socketio, queue_controller)
    control_service(app, socketio, queue_controller, camera_controller)
    video_service(app, socketio, video_dao)

    app.logger.info('Created services')

    queue_worker.start_dequeing()

    app.logger.info('Started workers')
