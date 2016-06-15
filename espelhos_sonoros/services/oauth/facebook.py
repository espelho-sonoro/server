import flask

def facebook(app, oauth):
    facebook = oauth.remote_app('Facebook',
            base_url='https://graph.facebook.com',
            request_token_url=None,
            access_token_url='/oauth/access_token',
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
        next_url = flask.url_for('index')
        resp = facebook.authorized_response()

        app.logger.info('Response from facebook: %s', resp)

        if resp is None:
            flask.flash(u'You denied the request sign in.')
            return flask.redirect(next_url)

        flask.session['facebook_token'] = (resp['access_token'], '')

        user = facebook.get('/me')
        app.logger.info('User information: %s', user.data)

        flask.session['username'] = user.data['name']

        flask.flash(u'You signed in as %s.' % user.data['name'])
        return flask.redirect(next_url)

