from send_mail import app, send_project_status_mail
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask import request


api = Api(app)
app.config.from_object(Config)
db = SQLAlchemy()
db.init_app(app)


class SendMail(Resource):
    def get(self, project_id):
        week_ending_date = request.args.get('w')
        status = db.engine.execute(f"SELECT * FROM project_status WHERE project_id = '{project_id}' AND week_ending_date = '{week_ending_date}'")
        project = db.engine.execute(f"SELECT * FROM project_details WHERE project_id = '{project_id}'")
        mail_list = []
        for stat in status:
            mail_list.append(dict(stat))
        for pro in project:
            mail_list.append(dict(pro))
        send_project_status_mail(mail_list)
        return {"message": "Mail sent successfully"}, 200


api.add_resource(SendMail, '/send-project-status-mail/<project_id>')


if __name__ == '__main__':
    app.run(port=5002, debug=True)