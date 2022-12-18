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
    def post(self, user_id):
        project_data = request.get_json()
        db.engine.execute(
                        f'''
                        INSERT INTO users_skills (
                            skill_name, skill_domain, skill_level, yoe) 
                        VALUES (
                            '{project_data['skill_name']}',
                            '{project_data['skill_domain']}',
                            '{project_data['skill_level']}',
                            '{project_data['yoe']}'
                            )
                        WHERE user_id = {user_id};
                        '''
                        )
        return {"message": "Skill added successfully"}, 200


class Register(Resource):
    def post(self):
        payload = request.get_json()
        db.engine.execute(
            f'''
            INSERT INTO users_skills (
                user_id, full_name, user_name, password)
            VALUES (
                "{payload['user_id']}",
                "{payload['full_name']}",
                "{payload['user_name']}",
                "{generate_password_hash(payload['password'])}"
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
            SELECT * FROM users_skills WHERE user_name = "{payload['user_name']}";
            '''
        )
        for user in users:
            if check_password_hash(user.password, payload['password']):
                encoded_jwt = jwt.encode({"user_id": user.user_id, "user_name": payload['user_name']}, JWT_TOKEN_SECRET, algorithm="HS256")
                return {"token": encoded_jwt}, 200
        return {"message": "Invalid credentials"}, 401

api.add_resource(AddUserSkill, '/choose-skills/<user_id>')
api.add_resource(Register, '/register')
api.add_resource(Login, '/login')


if __name__ == '__main__':
    app.run(port=5005, debug=True)
