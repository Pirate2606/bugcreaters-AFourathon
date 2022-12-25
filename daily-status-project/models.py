from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy()


class ProjectDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.String(8))
    project_name = db.Column(db.String(256))
    project_start_date = db.Column(db.DateTime)
    project_end_date = db.Column(db.DateTime)
    project_manager_name = db.Column(db.String(256))
    project_manager_email = db.Column(db.String(256))
    project_daily_report_email = db.Column(db.String(256))


class Teams(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.String(8))
    team_id = db.Column(db.String(8))
    team_name = db.Column(db.String(256))
    team_start_date = db.Column(db.DateTime)
    team_end_date = db.Column(db.DateTime)
    team_lead_name = db.Column(db.String(256))
    team_lead_email = db.Column(db.String(256))
    team_members = db.Column(db.String(256))


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(8))
    user_name = db.Column(db.String(256))
    user_email = db.Column(db.String(256))
