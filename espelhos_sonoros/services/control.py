import flask

def control(app, socketio, queue_controller, camera_controller):

    @socketio.on('LEFT', namespace='/control')
    def move_left():
        user_id = flask.session['user_id']
        if queue_controller.current_controller_id() == user_id:
            app.logger.debug('Moving camera left')
            # controller.move_left()
        else:
            raise ValueError('User not currenlty assigned to control')


    @socketio.on('RIGHT', namespace='/control')
    def move_left():
        user_id = flask.session['user_id']
        if queue_controller.current_controller_id() == user_id:
            app.logger.debug('Moving camera right')
            # controller.move_right()
        else:
            raise ValueError('User not currenlty assigned to control')

