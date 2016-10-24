from sqlalchemy.exc import IntegrityError
import flask

def queue(app, socketio, controller):
    from collections import namedtuple
    from flask import request, jsonify

    QueueElement = namedtuple('QueueElement', ['id', 'name'])

    def change_controlling_user(user_id):
        socketio.emit('controlling', room=user_id)

    controller.change_controll_callback = change_controlling_user

    @socketio.on('join', namespace='/queue')
    def join_queue():
        app.logger.debug('Current session: %s', flask.session)
        new_element = QueueElement(
                    id=flask.session['user_id'],
                    name=flask.session['user_name']
                )
        app.logger.debug('Joining queue - %s', new_element)
        try:
            controller.append_queue(new_element)
        except IntegrityError:
            app.logger.error('Failed to insert element in queue - %s', new_element)
        else:
            flask.session['in_queue'] = True
            socketio.emit('updateList', controller.queue(), namespace='/queue', broadcast=True)

    @socketio.on('list', namespace='/queue')
    def list_queue_socket():
        socketio.emit('updateList', controller.queue(), namespace='/queue')

    @app.route('/queue', methods=['GET'])
    def list_queue():
        return jsonify(controller.queue())

    @app.route('/queue', methods=['POST'])
    def append_queue():
        app.logger.debug('Request received: %s', request)

        payload = request.json

        if not payload:
            return 'Could not parse request', 400

        new_element = QueueElement(**request.json)

        app.logger.debug('Adding new element to queue: %s', new_element)

        try:
            controller.append_queue(new_element)
        except IntegrityError:
            return 'User already in queue', 409
        else:
            return list_queue()
