import flask

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

        app.logger.info('Response from google: %s', resp)

        if resp is None:
            flask.flash(u'You denied the request sign in.')
            return flask.redirect(next_url)

        flask.session['google_token'] = (resp['access_token'], '')
        me = google.get('userinfo')

        user = facebook.get('/me')
        app.logger.info('User information: %s', user.data)

        flask.session['google_user'] = user.data['name']

        flask.flash(u'You signed in as %s.' % user.data['name'])
        return flask.redirect(next_url)
