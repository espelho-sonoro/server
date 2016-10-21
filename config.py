import os

def str_config(key, default):
    return str(os.environ.get(key, default))

class Config(object):
    DEBUG                   = str_config('DEBUG', 'True') == 'True'
    SQLALCHEMY_DATABASE_URI = str_config("DATABASE_URL", 'sqlite:///espelhos.db')

    SECRET_KEY              = str_config('SECRET_KEY', '1')
    SERVER_NAME             = str_config('SERVER_NAME', 'localhost:5000')
    PREFERRED_URL_SCHEME    = str_config('PREFERRED_URL_SCHEME', 'http')

    FACEBOOK_APP_ID         = str_config('FACEBOOK_APP_ID', '1')
    FACEBOOK_APP_SECRET     = str_config('FACEBOOK_APP_SECRET', '1')

    GOOGLE_APP_ID           = str_config('GOOGLE_APP_ID', '1')
    GOOGLE_APP_SECRET       = str_config('GOOGLE_APP_SECRET', '1')

    LOGGER_HANDLER_POLICY   = 'always'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
