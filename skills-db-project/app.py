from flask import render_template, request, redirect, url_for
from models import app, db
from config import Config
import requests


app.config.from_object(Config)
db.init_app(app)
SKILLS_LIST_MICRO_APP_URL = 'http://127.0.0.1:5004'
# SKILLS_LIST_MICRO_APP_URL = 'http://skills-list-micro-app:5004'

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


if __name__ == '__main__':
    app.run(port=5003, debug=True)
