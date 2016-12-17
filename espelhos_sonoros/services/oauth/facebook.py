import flask
from .session_manager import set_current_user

def facebook(app, oauth):
    facebook = oauth.remote_app('Facebook',
        base_url='https://graph.facebook.com',
        request_token_url=None,
        access_token_url='/oauth/access_token',
        access_token_method='GET',
        authorize_url='https://www.facebook.com/dialog/oauth',
        consumer_key=app.config['FACEBOOK_APP_ID'],
        consumer_secret=app.config['FACEBOOK_APP_SECRET'],
        request_token_params={'scope': 'public_profile'}
    )

    @facebook.tokengetter
    def get_facebook_token(token=None):
        return flask.session.get('facebook_token')

    @app.route('/login/facebook')
    def login_facebook():
        resulting_url = flask.url_for('oauth_facebook', _external=True)
        return facebook.authorize(callback=resulting_url)

    @app.route('/oauth/facebook')
    def oauth_facebook():
        next_url = flask.url_for('root')
        resp = facebook.authorized_response()

        app.logger.debug('Response from facebook: %s', str(resp))

        if not resp:
            flask.flash('Failed to sign-in')
        else:
            flask.session['facebook_token'] = (resp['access_token'], '')
            user = facebook.get('/me?fields=name,picture')

            app.logger.debug('User information: %s', user.data)

            set_current_user(user.data['name'], user.data['picture']['data']['url'])

        return flask.redirect(next_url)
