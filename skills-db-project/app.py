from flask import render_template, request, redirect, url_for, session
from models import app, db
from config import Config
import requests
import uuid
import jwt

app.config.from_object(Config)
db.init_app(app)
SKILLS_LIST_MICRO_APP_URL = 'http://127.0.0.1:5004'
CHOOSE_SKILLS_MICRO_APP_URL = 'http://127.0.0.1:5005'
# SKILLS_LIST_MICRO_APP_URL = 'http://skills-list-micro-app:5004'
# CHOOSE_SKILLS_MICRO_APP_URL = 'http://choose-skills-micro-app:5005'
JWT_TOKEN_SECRET = "superSecret"


@app.before_first_request
def before_first_request():
    db.create_all()
    db.session.commit()


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@app.route('/add-skills', methods=['GET', 'POST'])
def add_skills():
    if request.method == 'POST':
        skill_name = request.form['skill_name']
        skill_domain = request.form['skill_domain']
        
        project_data = {"skill_name": skill_name,
                        "skill_domain": skill_domain
                        }
        
        requests.post(f"{SKILLS_LIST_MICRO_APP_URL}/add-skill", json=project_data)
        return redirect(url_for('home'))
    return render_template('add_new_skill_form.html')


@app.route('/choose-skills', methods=['GET', 'POST'])
def choose_skills():
    if request.method == 'POST':
        user_data = jwt.decode(session['token'], JWT_TOKEN_SECRET, algorithms=["HS256"])
        project_data = {
            "skill_name": request.form['skill_name'],
            "skill_domain": request.form['skill_domain'],
            "skill_level": request.form['skill_level'],
            "yoe": request.form['yoe']
        }
    requests.post(f"{CHOOSE_SKILLS_MICRO_APP_URL}/choose-skills/{user_data['user_id']}", json=project_data)
    return render_template('choose_skills.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
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
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
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
    return render_template('login.html', flag=flag)


@app.route("/logout")
def logout():
    session.pop('token', None)
    return redirect(url_for("home"))

if __name__ == '__main__':
    app.run(port=5003, debug=True)
