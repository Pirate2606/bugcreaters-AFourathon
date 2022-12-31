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


class ProjectStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.String(8))
    project_status = db.Column(db.String(256), default="")
    project_risk = db.Column(db.String(256), default="")
    project_highlights = db.Column(db.String(256), default="")
    week_ending_date = db.Column(db.DateTime)
