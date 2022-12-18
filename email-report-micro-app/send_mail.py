from flask_mail import Mail, Message
from flask import render_template
from flask import Flask
from config import SendMailConfig


app = Flask(__name__)
app.config.from_object(SendMailConfig)
mail = Mail(app)


def send_project_status_mail(project):
    msg = Message(f'Status of {project.project_name} for week ending {project.week_ending_date.strftime("%d %b, %Y")}')
    address = project.project_daily_report_email.split(",")
    for email in address:
        if '@' in email:
            msg.recipients.append(str(email))
    msg.html = render_template("project_status_mail.html", project=project)
    mail.send(msg)
