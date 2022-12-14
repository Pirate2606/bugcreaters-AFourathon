import os

# only for local testing
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = "supersecret" or os.environ.get("FLASK_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///F:\\Programs\\Hackathons\\AFourathon_2.0\\status-report-project\\data.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True


class DeploymentConfig(object):
    SECRET_KEY = "supersecret" or os.environ.get("FLASK_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = 'postgresql://aditya:Supersecret@db:5432/projectA'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
