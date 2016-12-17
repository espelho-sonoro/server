
def control(app, socketio, controller):

    @socketio.on('LEFT', namespace='/control')
    def move_left():
        app.logger.debug('Moving camera left')
        #controller.move_left()

    @socketio.on('RIGHT', namespace='/control')
    def move_left():
        app.logger.debug('Moving camera right')
        #controller.move_right()

