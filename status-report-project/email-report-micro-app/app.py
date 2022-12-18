from send_mail import app, send_project_status_mail
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from config import Config


api = Api(app)
app.config.from_object(Config)
db = SQLAlchemy()
db.init_app(app)


class SendMail(Resource):
    def get(self, project_id):
        projects = db.engine.execute(f"SELECT * FROM project_details WHERE project_id = '{project_id}'")
        for project in projects:
            send_project_status_mail(project)
        return {"message": "Mail sent successfully"}, 200


api.add_resource(SendMail, '/send-project-status-mail/<project_id>')


if __name__ == '__main__':
    app.run(port=5002, debug=True)