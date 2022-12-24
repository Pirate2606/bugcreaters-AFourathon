from flask import Flask, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from config import Config


app = Flask(__name__)
api = Api(app)
app.config.from_object(Config)
db = SQLAlchemy()
db.init_app(app)


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


api.add_resource(AddSkill, '/add-skill')
api.add_resource(GetSkills, '/get-skills')


if __name__ == '__main__':
    app.run(port=5004, debug=True)
