import flask
import uuid

def set_current_user(name, picture):
    flask.session['is_logged'] = True
    flask.session['user_id'] = str(uuid.uuid4())
    flask.session['user_name'] = name
    flask.session['user_picture'] = picture

