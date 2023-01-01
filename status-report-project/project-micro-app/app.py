from flask import Flask, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from config import Config
from datetime import datetime
import json


app = Flask(__name__)
api = Api(app)
app.config.from_object(Config)
db = SQLAlchemy()
db.init_app(app)


class RegisterProject(Resource):
    def post(self):
        project_data = request.get_json()
        db.engine.execute(
                        f'''
                        INSERT INTO project_details (
                            project_id, 
                            project_name, 
                            project_start_date, 
                            project_end_date, 
                            project_manager_name, 
                            project_manager_email,
                            project_daily_report_email) 
                        VALUES (
                            '{project_data['project_id']}',
                            '{project_data['project_name']}',
                            '{datetime.strptime(project_data['project_start_date'], '%Y-%m-%d')}',
                            '{datetime.strptime(project_data['project_end_date'], '%Y-%m-%d')}',
                            '{project_data['project_manager_name']}',
                            '{project_data['project_manager_email']}',
                            '{project_data['project_daily_report_email']}'
                            );
                        '''
                        )
        return {"message": "Project registered successfully"}, 200


class DeleteProject(Resource):
    def delete(self, project_id):
        db.engine.execute(f"DELETE FROM project_details WHERE project_id = '{project_id}'")
        return {"message": "Project deleted successfully"}, 200


class UpdateProject(Resource):
    def put(self, project_id):
        project_data = request.get_json()
        try:
            project_start_date = datetime.strptime(project_data['project_start_date'], "%Y-%m-%d %H:%M:%S").date()
        except:
            project_start_date = datetime.strptime(project_data['project_start_date'], "%Y-%m-%d")
        try:
            project_end_date = datetime.strptime(project_data['project_end_date'], "%Y-%m-%d %H:%M:%S").date()
        except:
            project_end_date = datetime.strptime(project_data['project_end_date'], "%Y-%m-%d")
        
        db.engine.execute(f'''
                          UPDATE project_details 
                          SET 
                            project_name = '{project_data['project_name']}',
                            project_start_date = '{datetime.combine(project_start_date, datetime.min.time())}',
                            project_end_date = '{datetime.combine(project_end_date, datetime.min.time())}',
                            project_manager_name = '{project_data['project_manager_name']}',
                            project_manager_email = '{project_data['project_manager_email']}',
                            project_daily_report_email = '{project_data['project_daily_report_email']}'
                          WHERE
                            project_id = '{project_id}'
                          ''')
        return {"message": "Project updated successfully"}, 200


class GetProjects(Resource):
    def get(self):
        projects = db.engine.execute(f"SELECT * FROM project_details")
        all_projects = [json.dumps(dict(project), default=str) for project in projects]
        return {"projects": all_projects}, 200


class GetProjectDetails(Resource):
    def get(self, project_id):
        project_details = db.engine.execute(f"SELECT * FROM project_details WHERE project_id = '{project_id}'")
        projects = [json.dumps(dict(project), default=str) for project in project_details]
        return {"projects": projects}, 200


api.add_resource(RegisterProject, '/register-project')
api.add_resource(DeleteProject, '/delete-project/<project_id>')
api.add_resource(UpdateProject, '/edit-project/<project_id>')
api.add_resource(GetProjects, '/get-projects')
api.add_resource(GetProjectDetails, '/get-project/<project_id>')


if __name__ == '__main__':
    app.run(port=5001, debug=True)
