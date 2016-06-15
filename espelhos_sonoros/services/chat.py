from datetime import datetime

def chat(app, socketio, dao, ChatMessage):
    @socketio.on('new-message', namespace='/chat')
    def new_message(message):
        message = ChatMessage(message['user'], datetime.now(), message['text'])
        dao.save(message)
        socket.emit('new-message', message.__json__(), broadcast=True)
