import os

# only for local testing
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = "supersecret" or os.environ.get("FLASK_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite') or os.environ.get('DATABASE_URL')
    # SQLALCHEMY_DATABASE_URI = 'postgresql://aditya:Supersecret@db:5432/projectB'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PARENT_FOLDER = 'skills-report-micro-app'
