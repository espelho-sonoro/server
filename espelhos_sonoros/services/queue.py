from sqlalchemy.exc import IntegrityError
from flask_socketio import close_room, leave_room, join_room, rooms
import flask

def queue(app, socketio, controller):
    from collections import namedtuple
    from flask import request, jsonify

    QueueElement = namedtuple('QueueElement', ['id', 'name'])

    def update_queue():
        queue = controller.queue()
        app.logger.debug('New user list: %s', queue)
        socketio.emit('updateQueue', queue, namespace='/queue', broadcast=True)

    def remove_controllers(users):
        if len(users) > 1:
            app.logger.warning('INCONSISTENT STATE, more than one controller cleaned: %s', users)
        for user in users:
            app.logger.debug('Sending stop controll to user: %s', user)
            socketio.emit('stopControl', namespace='/queue', room=user.user_id)

    def change_controlling_user(user):
        app.logger.info('Send controlling message to: %s', user.user_id)
        socketio.emit('startControl', namespace='/queue', room=user.user_id)

    controller.assign_user_callback = change_controlling_user
    controller.remove_users_callback = remove_controllers
    controller.update_queue_callback = update_queue

    @socketio.on('enterQueue', namespace='/queue')
    def enter_queue():
        app.logger.debug('Current session: %s', flask.session)
        app.logger.debug('Current existing rooms: %s', rooms())
        app.logger.debug('Current cookies: %s', flask.request.cookies)
        user_id = flask.session['user_id']
        join_room(user_id)
        name = flask.session['user_name']

        new_element = QueueElement(id=user_id, name=name)

        if (controller.append_queue(new_element)):
            queue = controller.queue()
            app.logger.debug('Sending new queue: %s', queue)
            socketio.emit('updateQueue', queue, namespace='/queue', broadcast=True)
        else:
            app.logger.error('Failed to insert element in queue - %s', new_element)

    @socketio.on('list', namespace='/queue')
    def list_queue_socket():
        update_queue()

    @socketio.on('gainControl', namespace='/queue')
    def gain_controll():
        user_id = flask.session['user_id']
        change_controlling_user(user_id)
