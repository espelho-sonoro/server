from espelhos_sonoros import *

import flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

def main():
    app = flask.Flask('espelhos_sonoros')
    app.config.from_object('config.Config')

    socketio = SocketIO(app, async_mode='threading')
    db = SQLAlchemy(app)

    espelhos_sonoros(app, socketio, db)

    app.logger.info('Started server.')
    socketio.run(app, port=app.config.PORT, host=app.config.HOST)

if __name__ == '__main__':
    main()
