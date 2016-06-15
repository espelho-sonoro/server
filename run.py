from espelhos_sonoros import *

import flask
import flask_socketio as socket
import flask_sqlalchemy as sql

def main():

    app = flask.Flask('espelhos_sonoros')
    socketio = socket.SocketIO(app)
    db = sql.SQLAlchemy(app)
    app.config.from_object('config.Config')

    print('debug: ' + str(app.config['DEBUG']))
    print('server_name: ' + app.config['SERVER_NAME'])

    espelhos_sonoros(app, socketio, db)
    socketio.run(app, host='0.0.0.0')

if __name__ == '__main__':
    import os
    print('Fuck: ' + str(os.environ.get('DEBUG')))
    print('What the: '+ os.environ.get('SERVER_NAME'))
    main()
