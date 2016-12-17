import flask
from .session_manager import set_current_user

def google(app, oauth):
    google = oauth.remote_app('Google',
        base_url='https://www.googleapis.com/oauth2/v1/',
        request_token_url=None,
        access_token_url='https://accounts.google.com/o/oauth2/token',
        access_token_method='POST',
        authorize_url='https://accounts.google.com/o/oauth2/auth',
        consumer_key=app.config['GOOGLE_APP_ID'],
        consumer_secret=app.config['GOOGLE_APP_SECRET'],
        request_token_params={'scope': 'profile'}
    )

    @google.tokengetter
    def get_google_token(token=None):
        return flask.session.get('google_token')

    @app.route('/login/google')
    def login_google():
        resulting_url = flask.url_for('oauth_google', _external=True)
        return google.authorize(callback=resulting_url)

    @app.route('/oauth/google')
    def oauth_google():
        next_url = flask.url_for('root')
        resp = google.authorized_response()

        app.logger.debug('Response from google: %s', resp)

        if not resp:
            flask.flash('Failed to sign-in')
        else:
            flask.session['google_token'] = (resp['access_token'], '')
            user = google.get('userinfo')

            app.logger.debug('User information: %s', user.data)

            set_current_user(user.data['name'], user.data['picture'])

        return flask.redirect(next_url)
