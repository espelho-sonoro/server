from espelhos_sonoros import *
import espelhos_sonoros.services

import os

port = int(os.environ.get("PORT", 5000))
database = str(os.environ.get("DATABASE_URL", 'sqlite:///espelhos.db'))

app.config['SQLALCHEMY_DATABASE_URI'] = database

db.create_all()

socketio.run(app, host='0.0.0.0', port=port, debug=True)
