from flask import Flask, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from config import Config
import jwt
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
api = Api(app)
app.config.from_object(Config)
db = SQLAlchemy()
db.init_app(app)

JWT_TOKEN_SECRET = "superSecret"

class AddUserSkill(Resource):
    def post(self):
        project_data = request.get_json()
        db.engine.execute(
            f'''
            INSERT INTO users_skills (
                user_id, skill_name, skill_domain, skill_level, yoe) 
            VALUES (
                '{project_data['user_id']}',
                '{project_data['skill_name']}',
                '{project_data['skill_domain']}',
                '{project_data['skill_level']}',
                '{project_data['yoe']}'
                );
            '''
            )
        return {"message": "Skill added successfully"}, 200


class GetSkills(Resource):
    def get(self, user_id):
        skills = []
        results = db.engine.execute(f"SELECT * FROM users_skills where user_id = '{user_id}';")
        for result in results:
            d = dict(result)
            if d["skill_name"] is not None:
                skills.append(d)
        return {"skills": skills}, 200


class UpdateSkill(Resource):
    def put(self, skill_id):
        data = request.get_json()
        db.engine.execute(
            f'''
            UPDATE users_skills
            SET skill_level = '{data['skill_level']}', yoe = '{data['yoe']}'
            WHERE id = '{skill_id}';
            '''
        )
        
        return {"message": "Skill updated successfully"}, 200


class DeleteSkill(Resource):
    def delete(self, skill_id):
        db.engine.execute(f"DELETE FROM users_skills WHERE id = '{skill_id}';")
        return {"message": "Skill deleted successfully"}, 200


class Register(Resource):
    def post(self):
        payload = request.get_json()
        db.engine.execute(
            f'''
            INSERT INTO users (
                user_id, full_name, user_name, password)
            VALUES (
                '{payload['user_id']}',
                '{payload['full_name']}',
                '{payload['user_name']}',
                '{generate_password_hash(payload['password'])}'
            );
            '''
        )
        encoded_jwt = jwt.encode({"user_id": payload['user_id'], "user_name": payload['user_name']}, JWT_TOKEN_SECRET, algorithm="HS256")
        return {"token": encoded_jwt}, 200


class Login(Resource):
    def post(self):
        payload = request.get_json()
        users = db.engine.execute(
            f'''
            SELECT * FROM users WHERE user_name = '{payload['user_name']}';
            '''
        )
        for user in users:
            if check_password_hash(user.password, payload['password']):
                encoded_jwt = jwt.encode({"user_id": user.user_id, "user_name": payload['user_name']}, JWT_TOKEN_SECRET, algorithm="HS256")
                return {"token": encoded_jwt}, 200
        return {"message": "Invalid credentials"}, 401


api.add_resource(AddUserSkill, '/choose-skills')
api.add_resource(GetSkills, '/get-skills/<user_id>')
api.add_resource(UpdateSkill, '/update-skill/<skill_id>')
api.add_resource(DeleteSkill, '/delete-skill/<skill_id>')
api.add_resource(Register, '/register')
api.add_resource(Login, '/login')



if __name__ == '__main__':
    app.run(port=5005, debug=True)