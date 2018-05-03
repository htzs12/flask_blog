import os

basedir=os.path.abspath(os.path.dirname(__file__))

DEBUG=True

SECRET_KEY='hard to guess string'

SQLALCHEMY_DATABASE_URI='sqlite:///'+os.path.join(basedir,'data.sqlite')

SQLALCHEMY_COMMIT_ON_TEARDOWN=True

SQLALCHEMY_TRACK_MODIFICATIONS = False
