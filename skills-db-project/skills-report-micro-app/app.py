import os
from flask import Flask, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from config import Config, DeploymentConfig
import pandas as pd
from google.cloud import storage
import logging


app = Flask(__name__)
api = Api(app)
# app.config.from_object(Config)
app.config.from_object(DeploymentConfig)
db = SQLAlchemy()
db.init_app(app)
logging.basicConfig(filename='skills_report_m_a.log', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')


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
        
        user_names = []
        full_names = []
        for user in all_users:
            user_names.append(user["user_name"])
            full_names.append(user["full_name"])
        
        pd.DataFrame({"Username": user_names, "FullName": full_names}).to_excel("users.xlsx", index=False)
        
        client = storage.Client.from_service_account_json(json_credentials_path='afourathon-3edec2aa3eac.json')
        bucket = client.get_bucket('afourathon')
        object_name_in_gcs_bucket = bucket.blob('users.xlsx')
        object_name_in_gcs_bucket.upload_from_filename('users.xlsx')
        
        os.remove("users.xlsx")
        return {"users": all_users}, 200


class DownloadFile(Resource):
    def get(self):
        client = storage.Client.from_service_account_json(json_credentials_path='afourathon-3edec2aa3eac.json')
        bucket = client.get_bucket('afourathon')
        blob = bucket.blob('users.xlsx')
        filename = os.path.join(os.getcwd(), 'static')
        blob.download_to_filename(os.path.join(filename, 'users.xlsx'))
        return {"message": "File downloaded successfully"}, 200

 
api.add_resource(FilterSkills, '/filter-skills')
api.add_resource(DownloadFile, '/get-file')


if __name__ == '__main__':
    app.run(port=5006)
