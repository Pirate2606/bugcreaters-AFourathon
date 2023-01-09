import os

# only for local testing
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = "supersecret" or os.environ.get("FLASK_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite') or os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PARENT_FOLDER = 'skills-report-micro-app'
    DEBUG = True
    SKILLS_LIST_MICRO_APP_URL = 'http://127.0.0.1:5004'
    CHOOSE_SKILLS_MICRO_APP_URL = 'http://127.0.0.1:5005'
    SKILLS_REPORT_MICRO_APP_URL = 'http://127.0.0.1:5006'

    
class DeploymentConfig(object):
    SECRET_KEY = "supersecret" or os.environ.get("FLASK_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = 'postgresql://aditya:Supersecret@db:5432/projectB'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PARENT_FOLDER = 'skills-report-micro-app'
    DEBUG = True
    SKILLS_LIST_MICRO_APP_URL = 'http://skills-list-micro-app:5004'
    CHOOSE_SKILLS_MICRO_APP_URL = 'http://choose-skills-micro-app:5005'
    SKILLS_REPORT_MICRO_APP_URL = 'http://skills-report-micro-app:5006'
