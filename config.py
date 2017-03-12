import os
from distutils.util import strtobool

def str_config(key, default):
    return str(os.environ.get(key, default))

def bool_config(key, default):
    return strtobool(os.environ.get(key, str(default)))

def int_config(key, default):
    return int(os.environ.get(key, str(default)))

class Config(object):
    DEBUG                           = bool_config('DEBUG', False)
    SQLALCHEMY_ECHO                 = bool_config('SQLALCHEMY_ECHO', False)
    SQLALCHEMY_TRACK_MODIFICATIONS  = bool_config('SQLALCHEMY_TRACK_MODIFICATIONS', False)

    SQLALCHEMY_DATABASE_URI         = str_config("DATABASE_URL", 'sqlite:///espelhos.db')

    SECRET_KEY                      = str_config('SECRET_KEY', '1')
    PREFERRED_URL_SCHEME            = str_config('PREFERRED_URL_SCHEME', 'http')

    FACEBOOK_APP_ID                 = str_config('FACEBOOK_APP_ID', '1')
    FACEBOOK_APP_SECRET             = str_config('FACEBOOK_APP_SECRET', '1')

    GOOGLE_APP_ID                   = str_config('GOOGLE_APP_ID', '1')
    GOOGLE_APP_SECRET               = str_config('GOOGLE_APP_SECRET', '1')

    USER_ROTATION_TIME              = int_config('USER_ROTATION_TIME', 60) # seconds
    TICK_INTERVAL                   = int_config('TICK_INTERVAL', 5) # seconds

    PORT                            = int_config('PORT', 5000)
    HOST                            = str_config('HOST', '0.0.0.0')

    SERVER_NAME                     = str_config('SERVER_NAME', '%s:%i'.format(HOST, PORT))
    LOGGER_HANDLER_POLICY           = 'always'
