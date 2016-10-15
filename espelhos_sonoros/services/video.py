def video(app, socketio, dao):
    import flask_socketio as socket

    DEFAULT_VIDEO_ID = '1'

    def anounce_position(video_id):
        position = dao.get(video_id).__json__()
        socket.emit('position', position, broadcast=True, namespace='/video')

    @socketio.on('rotate', namespace='/video')
    def rotate(movement):
        dao.increment(DEFAULT_VIDEO_ID, movement)
        anounce_position(DEFAULT_VIDEO_ID)

    @socketio.on('position', namespace='/video')
    def force_position(content):
        position = dao.get(DEFAULT_VIDEO_ID)
        position.x_position = float(content['x'])
        position.y_position = float(content['y'])
        dao.save(position)
        anounce_position(DEFAULT_VIDEO_ID)
