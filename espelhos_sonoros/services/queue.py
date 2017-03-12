from collections import namedtuple
from flask import request, jsonify
import flask

def queue_service(app, socketio, controller):

    QueueElement = namedtuple('QueueElement', ['id', 'name', 'room'])

    def broadcast_queue():
        queue = controller.queue()
        app.logger.debug('Sending the queue: %s', queue)
        socketio.emit('updateQueue', queue, namespace='/queue', broadcast=True)

    def remove_controllers(users):
        if len(users) > 1:
            app.logger.warning('INCONSISTENT STATE, more than one controller cleaned: %s', users)
        for user in users:
            app.logger.debug('Sending stop controll to user: %s', user)
            socketio.emit('stopControl', namespace='/queue', room=user.room)

    def change_controlling_user(user):
        app.logger.info('Send controlling message to: %s', user)
        socketio.emit('startControl', namespace='/queue', room=user.room)

    controller.assign_user_callback = change_controlling_user
    controller.remove_users_callback = remove_controllers
    controller.update_queue_callback = broadcast_queue

    @socketio.on('enterQueue', namespace='/queue')
    def enter_queue():
        app.logger.debug('Current session: %s', flask.session)
        app.logger.debug('Current cookies: %s', flask.request.cookies)

        user_id = flask.session['user_id']
        name = flask.session['user_name']

        new_element = QueueElement(id=user_id, name=name, room=request.sid)

        if (controller.append_queue(new_element)):
            app.logger.info('User joined the queue: %s', user_id)
            broadcast_queue()
        else:
            app.logger.error('Failed to insert element in queue: %s', new_element)

    @socketio.on('getQueue', namespace='/queue')
    def get_queue_socket():
        broadcast_queue()
