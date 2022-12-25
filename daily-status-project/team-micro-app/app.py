from flask import Flask, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from config import Config
from datetime import datetime


app = Flask(__name__)
api = Api(app)
app.config.from_object(Config)
db = SQLAlchemy()
db.init_app(app)


class RegisterTeam(Resource):
    def post(self):
        team_data = request.get_json()
        db.engine.execute(
                        f'''
                        INSERT INTO teams (
                            project_id,
                            team_id,
                            team_name, 
                            team_start_date, 
                            team_end_date, 
                            team_lead_name, 
                            team_lead_email,
                            team_members
                        ) 
                        VALUES (
                            '{team_data['project_id']}',
                            '{team_data['team_id']}',
                            '{team_data['team_name']}',
                            '{datetime.strptime(team_data['team_start_date'], '%Y-%m-%d')}',
                            '{datetime.strptime(team_data['team_end_date'], '%Y-%m-%d')}',
                            '{team_data['team_lead_name']}',
                            '{team_data['team_lead_email']}',
                            '{team_data['team_members']}'
                        );
                        '''
                        )
        return {"message": "Team registered successfully"}, 200


class GetTeams(Resource):
    def get(self, project_id):
        teams = db.engine.execute(f"SELECT * FROM teams WHERE project_id = '{project_id}'")
        all_teams = [dict(team) for team in teams]
        return {"teams": all_teams}, 200


class GetTeamDetails(Resource):
    def get(self, team_id):
        team_details = db.engine.execute(f"SELECT * FROM teams WHERE team_id = '{team_id}'")
        teams = [dict(team) for team in team_details]
        return {"teams": teams}, 200


class DeleteTeam(Resource):
    def delete(self, team_id):
        db.engine.execute(f"DELETE FROM teams WHERE team_id = '{team_id}'")
        return {"message": "Team deleted successfully"}, 200


class UpdateTeam(Resource):
    def put(self):
        team_data = request.get_json()
        try:
            team_start_date = datetime.strptime(team_data['team_start_date'], "%Y-%m-%d %H:%M:%S").date()
        except:
            team_start_date = datetime.strptime(team_data['team_start_date'], "%Y-%m-%d")
        try:
            team_end_date = datetime.strptime(team_data['team_end_date'], "%Y-%m-%d %H:%M:%S").date()
        except:
            team_end_date = datetime.strptime(team_data['team_end_date'], "%Y-%m-%d")
        
        db.engine.execute(f'''
                          UPDATE teams 
                          SET 
                            team_name = '{team_data['team_name']}',
                            team_start_date = '{datetime.combine(team_start_date, datetime.min.time())}',
                            team_end_date = '{datetime.combine(team_end_date, datetime.min.time())}',
                            team_lead_name = '{team_data['team_lead_name']}',
                            team_lead_email = '{team_data['team_lead_email']}',
                            team_members = '{team_data['team_members']}'
                          WHERE
                            team_id = '{team_data['team_id']}'
                          ''')
        return {"message": "Team updated successfully"}, 200


api.add_resource(RegisterTeam, '/register-team')
api.add_resource(GetTeams, '/get-teams/<project_id>')
api.add_resource(GetTeamDetails, '/get-team/<team_id>')
api.add_resource(DeleteTeam, '/delete-team/<team_id>')
api.add_resource(UpdateTeam, '/edit-team')


if __name__ == '__main__':
    app.run(port=5009, debug=True)
