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
        return {"message": "Skill added successfully"}, 200


api.add_resource(AddSkill, '/add-skill')


if __name__ == '__main__':
    app.run(port=5004, debug=True)
