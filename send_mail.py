from flask_mail import Mail, Message
from flask import render_template
from models import app
from config import SendMail

app.config.from_object(SendMail)
mail = Mail(app)


def send_project_status_mail(project, week_end_date):
    msg = Message(f'Status of {project.project_name} for week ending {week_end_date}')
    address = project.project_daily_report_email.split(",")
    for email in address:
        print(email)
        msg.recipients.append(str(email))
    msg.html = render_template("project_status_mail.html", project=project)
    mail.send(msg)
