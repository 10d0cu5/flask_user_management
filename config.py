import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.urandom(32)
    WTF_CSRF_SECRET_KEY = os.urandom(32)
    #DB RELATED KEYS:
    DB_TABLE = 'Users'
    SQLALCHEMY_DATABASE_URI = os.environ.get('/app/PeterPark.db') or \
        'sqlite:///' + os.path.join(basedir, 'PeterPark.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False