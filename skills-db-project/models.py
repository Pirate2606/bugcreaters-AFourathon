from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy()


class Skills(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    skill_name = db.Column(db.String(256))
    skill_domain = db.Column(db.String(256))


class UsersSkills(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(8))
    skill_domain = db.Column(db.String(15))
    skill_name = db.Column(db.String(256))
    skill_level = db.Column(db.String(15))
    yoe = db.Column(db.Integer)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(8))
    full_name = db.Column(db.String(256))
    user_name = db.Column(db.String(256), unique=True)
    password = db.Column(db.String(256))
