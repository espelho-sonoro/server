from flask import jsonify, request

def box(box, application):
    @application.route('/box', methods=['GET'])
    def whois():
        return jsonify(box.__dict__)

    @application.route('/box', methods=['POST'])
    def register():
        other_box = request.get_json()
        box.update(other_box)
        return jsonify(box.__dict__)

