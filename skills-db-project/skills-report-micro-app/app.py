from flask import Flask, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from config import Config


app = Flask(__name__)
api = Api(app)
app.config.from_object(Config)
db = SQLAlchemy()
db.init_app(app)


class FilterSkills(Resource):
    def get(self):
        skills = request.get_json()["skills"]
        users = db.session.execute(
            f"""
                SELECT *
                FROM users_skills;
            """
        )
        
        d = {}
        temp = []
        for user in users:
            if user.user_id not in d:
                d[user.user_id] = []
            d[user.user_id].append(user.skill_name)
        
        for i in d:
            if set(skills) <= set(d[i]):
                temp.append(i)
        
        all_users = []
        for user in temp:
            temp = db.session.execute(
                f"""
                    SELECT full_name, user_name
                    FROM users
                    WHERE user_id = '{user}'
                """
            )
            all_users.append([dict(t) for t in temp][0])
        
        return {"users": all_users}, 200


api.add_resource(FilterSkills, '/filter-skills')


if __name__ == '__main__':
    app.run(port=5006, debug=True)
