import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    CSRF_ENABLED = True

    # DATABASE_URL='postgresql://postgres:1234@localhost/gs'
