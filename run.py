import os
from app import socketio,app

port = int(os.environ.get("PORT", 5000))

socketio.run(app, host='0.0.0.0', port=port, debug=True)
