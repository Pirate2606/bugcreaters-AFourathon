from flask_mail import Mail, Message
from flask import render_template
from flask import Flask
from config import SendMailConfig


app = Flask(__name__)
app.config.from_object(SendMailConfig)
mail = Mail(app)


def send_project_status_mail(mail_list):
    msg = Message(f'''Status of {mail_list[1]['project_name']} for week ending {mail_list[0]['week_ending_date'].strftime("%d %b, %Y")}''')
    address = mail_list[1]['project_daily_report_email'].split(",")
    for email in address:
        if '@' in email:
            msg.recipients.append(str(email))
    msg.html = render_template("project_status_mail.html", project=mail_list[1], status=mail_list[0])
    mail.send(msg)
    return "Mail sent successfully"
