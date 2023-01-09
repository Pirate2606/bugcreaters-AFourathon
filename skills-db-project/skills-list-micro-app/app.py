from flask import Flask, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from config import Config, DeploymentConfig
import logging


app = Flask(__name__)
api = Api(app)
# app.config.from_object(Config)
app.config.from_object(DeploymentConfig)
db = SQLAlchemy()
db.init_app(app)
logging.basicConfig(filename='skill_list_m_a.log', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')


class AddSkill(Resource):
    def post(self):
        project_data = request.get_json()
        prev_skills = db.engine.execute('SELECT * FROM skills;')
        for skill in prev_skills:
            if skill.skill_name == project_data['skill_name'] and skill.skill_domain == project_data['skill_domain']:
                return {"message": "Skill already exists"}, 400
        db.engine.execute(
                        f'''
                        INSERT INTO skills (
                            skill_name,
                            skill_domain) 
                        VALUES (
                            '{project_data['skill_name']}',
                            '{project_data['skill_domain']}'
                            );
                        '''
                        )
        return {"message": "Skill added successfully"}


class GetSkills(Resource):
    def get(self):
        skills = []
        results = db.engine.execute('SELECT * FROM skills;')
        for result in results:
            skills.append(dict(result))
        return {"skills": skills}


class GetSkill(Resource):
    def get(self, skill_id):
        results = db.engine.execute(f"SELECT * FROM skills WHERE id = '{skill_id}';")
        for result in results:
            return {"skill": [dict(result)]}


class UpdateSkill(Resource):
    def put(self, skill_id):
        data = request.get_json()
        db.engine.execute(
            f'''
                UPDATE skills 
                SET skill_name = '{data['skill_name']}', skill_domain = '{data['skill_domain']}'
                WHERE id = '{skill_id}';
            '''
        )
        return {"message": "Skill updated successfully"}


class DeleteSkill(Resource):
    def delete(self, skill_id):
        db.engine.execute(f"DELETE FROM skills WHERE id = '{skill_id}';")
        return {"message": "Skill deleted successfully"}, 200


api.add_resource(AddSkill, '/add-skill')
api.add_resource(GetSkills, '/get-skills')
api.add_resource(GetSkill, '/get-skill/<skill_id>')
api.add_resource(UpdateSkill, '/update-skill/<skill_id>')
api.add_resource(DeleteSkill, '/delete-skill/<skill_id>')


if __name__ == '__main__':
    app.run(port=5004)
