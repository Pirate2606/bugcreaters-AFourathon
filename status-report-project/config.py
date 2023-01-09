import os

# only for local testing
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = "supersecret" or os.environ.get("FLASK_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite') or os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    PROJECT_MICRO_APP_URL = 'http://127.0.0.1:5001'
    EMAIL_REPORT_MICRO_APP_URL = 'http://127.0.0.1:5002'
    UPDATE_STATUS_MICRO_APP = 'http://127.0.0.1:5050'


class DeploymentConfig(object):
    SECRET_KEY = "supersecret" or os.environ.get("FLASK_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = 'postgresql://aditya:Supersecret@db:5432/projectA'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    PROJECT_MICRO_APP_URL = 'http://project-micro-app:5001'
    EMAIL_REPORT_MICRO_APP_URL = 'http://email-report-micro-app:5002'
    UPDATE_STATUS_MICRO_APP = 'http://update-status-micro-app:5050'
