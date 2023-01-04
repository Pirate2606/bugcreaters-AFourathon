from flask import Flask, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from config import Config
import json
import logging


app = Flask(__name__)
api = Api(app)
app.config.from_object(Config)
db = SQLAlchemy()
db.init_app(app)
logging.basicConfig(filename='logs/update_status_m_a.log', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')


class ProjectStatus(Resource):
    def post(self, project_id):
        project_data = request.get_json()
        db.engine.execute(
                        f'''
                        INSERT INTO project_status (
                            project_id,
                            project_status,
                            project_risk,
                            project_highlights,
                            week_ending_date) 
                        VALUES (
                            '{project_id}',
                            '{project_data['project_status']}',
                            '{project_data['project_risk']}',
                            '{project_data['project_highlights']}',
                            '{project_data['week_ending_date']}'
                            );
                        '''
                        )
        return {"message": "Project registered successfully"}, 200
    
    def delete(self, project_id):
        week_ending_date = request.args.get('w')
        db.engine.execute(f"DELETE FROM project_status WHERE project_id = '{project_id}' AND week_ending_date = '{week_ending_date}'")
        return {"message": "Project deleted successfully"}, 200
    
    def put(self, project_id):
        project_data = request.get_json()
        db.engine.execute(f'''
                          UPDATE project_status
                          SET 
                            project_status = '{project_data['project_status']}',
                            project_risk = '{project_data['project_risk']}',
                            project_highlights = '{project_data['project_highlights']}',
                            week_ending_date = '{project_data['week_ending_date']}'
                          WHERE
                            project_id = '{project_id}' AND
                            week_ending_date = '{project_data['week_ending_date']}'
                          ''')
        return {"message": "Project updated successfully"}, 200
    
    def get(self, project_id):
        week_ending_date = request.args.get('w')
        results = db.engine.execute(f'''
                                    SELECT * FROM project_status WHERE project_id = '{project_id}' AND week_ending_date = '{week_ending_date}'
                                    ''')
        status = [json.dumps(dict(result), default=str) for result in results]
        return {"status": status}, 200


class GetProjectStatusWeekly(Resource):
    def get(self, week_ending_date):
        results = db.engine.execute(f'''
                                    SELECT * FROM project_status WHERE week_ending_date = '{week_ending_date.split("<")[1].split(">")[0]}'
                                    ''')
        status = [json.dumps(dict(result), default=str) for result in results]
        return {"status": status}, 200
        

api.add_resource(ProjectStatus, '/project-status/<project_id>')
api.add_resource(GetProjectStatusWeekly, '/get-status/<week_ending_date>')


if __name__ == '__main__':
    app.run(port=5050)
