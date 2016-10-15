def chat(app, socketio, dao, ChatMessage):
    from datetime import datetime

    @socketio.on('message', namespace='/chat')
    def new_message(message):
        message = ChatMessage(message['user'], datetime.now(), message['text'])
        dao.save(message)
        socket.emit('message', message.__json__(), broadcast=True)
