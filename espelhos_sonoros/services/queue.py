from sqlalchemy.exc import IntegrityError

def queue(app, controller):
    from collections import namedtuple
    from flask import request, jsonify

    QueueElement = namedtuple('QueueElement', ['id', 'name'])

    @app.route('/queue', methods=['GET'])
    def list_queue():
        return jsonify(controller.queue())

    @app.route('/queue', methods=['POST'])
    def append_queue():
        payload = request.json

        if not payload:
            return 'Could not parse request', 400

        new_element = QueueElement(**request.json)

        try:
            controller.append_queue(new_element)
        except IntegrityError:
            return 'User already in queue', 409
        else:
            return jsonify(controller.queue())

