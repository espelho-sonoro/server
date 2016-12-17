import os
from distutils.util import strtobool

def str_config(key, default):
    return str(os.environ.get(key, default))

def bool_config(key, default):
    return strtobool(os.environ.get(key, str(default)))

class Config(object):
    DEBUG                   = bool_config('DEBUG', True)
    SQLALCHEMY_DATABASE_URI = str_config("DATABASE_URL", 'sqlite:///espelhos.db')
    SQLALCHEMY_ECHO         = bool_config('SQLALCHEMY_ECHO', False)

    SECRET_KEY              = str_config('SECRET_KEY', '1')
    SERVER_NAME             = str_config('SERVER_NAME', 'localhost:5000')
    PREFERRED_URL_SCHEME    = str_config('PREFERRED_URL_SCHEME', 'http')

    FACEBOOK_APP_ID         = str_config('FACEBOOK_APP_ID', '1')
    FACEBOOK_APP_SECRET     = str_config('FACEBOOK_APP_SECRET', '1')

    GOOGLE_APP_ID           = str_config('GOOGLE_APP_ID', '1')
    GOOGLE_APP_SECRET       = str_config('GOOGLE_APP_SECRET', '1')

    LOGGER_HANDLER_POLICY   = 'always'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
