import os

SECRET_KEY = os.urandom(24)
basedir = os.path.abspath(os.path.dirname(__file__))