from flask import session, redirect

def oauth(app):
    from flask_oauthlib.client import OAuth
    from .facebook import facebook
    from .google import google

    oauth = OAuth()

    facebook(app, oauth)
    google(app, oauth)

    @app.route('/logout')
    def logout():
        session.clear()
        return redirect('/')
