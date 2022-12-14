import os
from flask import Flask, render_template, request, redirect, url_for, session, send_file, flash
from models import db
from config import Config, DeploymentConfig
import requests
import uuid
import jwt
import logging


logging.basicConfig(filename='app.log', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
app = Flask(__name__)
# app.config.from_object(Config)
app.config.from_object(DeploymentConfig)
db.init_app(app)

SKILLS_LIST_MICRO_APP_URL = app.config['SKILLS_LIST_MICRO_APP_URL']
CHOOSE_SKILLS_MICRO_APP_URL = app.config['CHOOSE_SKILLS_MICRO_APP_URL']
SKILLS_REPORT_MICRO_APP_URL = app.config['SKILLS_REPORT_MICRO_APP_URL']


JWT_TOKEN_SECRET = "superSecret"


@app.before_first_request
def before_first_request():
    db.create_all()
    db.session.commit()


@app.route('/', methods=['GET', 'POST'])
def home():
    login_flag = True
    if session.get("token"):
        login_flag = False
    
    all_skills = requests.get(f"{SKILLS_LIST_MICRO_APP_URL}/get-skills")
    return render_template('home.html', login_flag=login_flag, all_skills=all_skills.json()["skills"])


@app.route('/filter-skills', methods=['GET', 'POST'])
def filter_skills():
    login_flag = True
    if session.get("token"):
        login_flag = False

    if request.method == 'POST':
        skills = request.get_json()
        skill_data = {"skills": skills}
        response = requests.get(f"{SKILLS_REPORT_MICRO_APP_URL}/filter-skills", json=skill_data)
        
        return {"users": response.json()["users"], "selected_skills": skills}
    
    return render_template('home.html', login_flag=login_flag)


@app.route('/download-users', methods=['GET', 'POST'])
def download_users():
    requests.get(f"{SKILLS_REPORT_MICRO_APP_URL}/get-file")
    parent_path = os.path.join(os.path.join(os.getcwd(), app.config['PARENT_FOLDER']), "static")
    path = os.path.join(parent_path, "users.xlsx")
    return send_file(path, as_attachment=True)


@app.route('/add-skills', methods=['GET', 'POST'])
def add_skills():
    login_flag = True
    if session.get("token"):
        login_flag = False
    if request.method == 'POST':
        skill_name = request.form['skill_name']
        skill_domain = request.form['skill_domain']
        
        skill_data = {
            "skill_name": skill_name,
            "skill_domain": skill_domain
        }
        
        response = requests.post(f"{SKILLS_LIST_MICRO_APP_URL}/add-skill", json=skill_data)
        if response.status_code == 400:
            flash("Skill already exists")
        return redirect(url_for('add_skills'))
    return render_template('add_new_skill_form.html', login_flag=login_flag)


@app.route('/skills', methods=['GET', 'POST'])
def skills():
    login_flag = True
    if session.get("token"):
        login_flag = False
    all_skills = requests.get(f"{SKILLS_LIST_MICRO_APP_URL}/get-skills")
    return render_template('skills.html', skills=all_skills.json()["skills"], login_flag=login_flag)


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    requests.delete(f"{SKILLS_LIST_MICRO_APP_URL}/delete-skill/{request.args.get('skill_id')}")
    return redirect(url_for('skills'))


@app.route('/update', methods=['GET', 'POST'])
def update():
    login_flag = True
    if session.get("token"):
        login_flag = False
    if request.method == "POST":
        skill_id = request.args.get('skill_id')
        skill_name = request.form['skill_name']
        skill_domain = request.form['skill_domain']
        
        data = {
            "skill_name": skill_name,
            "skill_domain": skill_domain
        }
        requests.put(f"{SKILLS_LIST_MICRO_APP_URL}/update-skill/{skill_id}", json=data)
        return redirect(url_for('skills'))
    skill = requests.get(f"{SKILLS_LIST_MICRO_APP_URL}/get-skill/{request.args.get('skill_id')}")
    return render_template('update_skill.html', skill=skill.json()["skill"][0], login_flag=login_flag)


@app.route('/choose-skills', methods=['GET', 'POST'])
def choose_skills():
    login_flag = True
    if session.get("token"):
        login_flag = False
    else:
        return redirect(url_for('login'))
    user_data = jwt.decode(session['token'], JWT_TOKEN_SECRET, algorithms=["HS256"])
    all_skills = requests.get(f"{SKILLS_LIST_MICRO_APP_URL}/get-skills")
    skills = requests.get(f"{CHOOSE_SKILLS_MICRO_APP_URL}/get-skills/{user_data['user_id']}")
    if request.method == 'POST':
        header = {'Authorization': 'Bearer ' + session['token']}
        project_data = {
            "skill_name": request.form['skill_name'],
            "skill_domain": request.form['skill_domain'],
            "skill_level": request.form['skill_level'],
            "yoe": request.form['yoe']
        }

        requests.post(f"{CHOOSE_SKILLS_MICRO_APP_URL}/choose-skills", json=project_data, headers=header)
        return redirect(url_for('choose_skills'))

    return render_template('choose_skills.html', all_skills=all_skills.json()["skills"], skills=skills.json()["skills"], login_flag=login_flag)


@app.route('/update-skill/<skill_id>')
def update_skill(skill_id):
    yoe = int(request.args.get('y'))
    skill_level = request.args.get('l')
    skill_data = {
        "skill_level": skill_level,
        "yoe": yoe
    }

    requests.put(f"{CHOOSE_SKILLS_MICRO_APP_URL}/update-skill/{skill_id}", json=skill_data)
    return redirect(url_for('choose_skills'))


@app.route('/delete-skill/<skill_id>')
def delete_skill(skill_id):
    requests.delete(f"{CHOOSE_SKILLS_MICRO_APP_URL}/delete-skill/{skill_id}")
    return redirect(url_for('choose_skills'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    login_flag = True
    if session.get("token"):
        login_flag = False
    password_flag = False
    if request.method == 'POST':
        user_name = request.form['user_name']
        full_name = request.form['full_name']

        # Comparing password and confirm password fields
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password != confirm_password:
            password_flag = True
        if password_flag:
            return render_template('register.html', password_flag=password_flag)

        user_id = uuid.uuid4().hex[:8]
        users_data = {
            "user_id": user_id,
            "user_name": user_name,
            "full_name": full_name,
            "password": password
        }
        # Adding data to database
        jwt_token = requests.post(f"{CHOOSE_SKILLS_MICRO_APP_URL}/register", json=users_data).json()
        session['token'] = jwt_token['token']

        return redirect(url_for('home'))
    return render_template('register.html', login_flag=login_flag)


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_flag = True
    if session.get("token"):
        return redirect(url_for('home'))
    flag = False
    if request.method == "POST":
        # Fetching user from database
        user_data = {
            "user_name": request.form['user_name'],
            "password": request.form['password']
        }
        jwt_token = requests.post(f"{CHOOSE_SKILLS_MICRO_APP_URL}/login", json=user_data)
        if jwt_token.status_code != 401:
            session['token'] = jwt_token.json()['token']
            return redirect(url_for('home'))
        else:
            flag = True
    return render_template('login.html', flag=flag, login_flag=login_flag)


@app.route("/logout")
def logout():
    session.pop('token', None)
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(port=5003)
