import os

# only for local testing
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = "supersecret" or os.environ.get("FLASK_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///F:\\Programs\\Hackathons\\AFourathon_2.0\\data.sqlite'
    # SQLALCHEMY_DATABASE_URI = 'postgresql://aditya:Supersecret@db:5432/projectA'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class SendMailConfig(object):
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'royalenaitan@gmail.com'
    MAIL_PASSWORD = 'fhcnvibwngmpfetx'
    MAIL_DEFAULT_SENDER = 'royalenaitan@gmail.com'
    MAIL_MAX_EMAILS = None
    MAIL_ASCII_ATTACHMENTS = False
