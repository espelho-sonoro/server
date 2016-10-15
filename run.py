from espelhos_sonoros import *

import flask
import flask_socketio as socket
import flask_sqlalchemy as sql

def main():
    app = flask.Flask('espelhos_sonoros')
    socketio = socket.SocketIO(app)
    db = sql.SQLAlchemy(app)
    app.config.from_object('config.Config')

    espelhos_sonoros(app, socketio, db)
    socketio.run(app, host='0.0.0.0')

if __name__ == '__main__':
    main()
