from send_mail import app, send_project_status_mail
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from config import Config, DeploymentConfig
from flask import request
import logging


api = Api(app)
# app.config.from_object(Config)
app.config.from_object(DeploymentConfig)
db = SQLAlchemy()
db.init_app(app)
logging.basicConfig(filename='logs/email_report_m_a.log', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')


class SendMail(Resource):
    def get(self, project_id):
        message = "Mail send error"
        week_ending_date = request.args.get('w')
        status = db.engine.execute(f"SELECT * FROM project_status WHERE project_id = '{project_id}' AND week_ending_date = '{week_ending_date}'")
        project = db.engine.execute(f"SELECT * FROM project_details WHERE project_id = '{project_id}'")
        mail_list = []
        for stat in status:
            mail_list.append(dict(stat))
        for pro in project:
            mail_list.append(dict(pro))
        if len(mail_list) > 0:
            message = send_project_status_mail(mail_list)
        else:
            return {"message": message}, 200
        return {"message": message}, 200


api.add_resource(SendMail, '/send-project-status-mail/<project_id>')


if __name__ == '__main__':
    app.run(port=5002)