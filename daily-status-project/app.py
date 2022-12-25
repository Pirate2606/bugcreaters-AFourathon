from flask import render_template, request, redirect, url_for
from models import app, db, ProjectDetails
from config import Config
import uuid
import requests


app.config.from_object(Config)
db.init_app(app)
PROJECT_MICRO_APP_URL = 'http://127.0.0.1:5008'
# PROJECT_MICRO_APP_URL = 'http://project-micro-app:5008'


@app.before_first_request
def before_first_request():
    db.create_all()
    db.session.commit()


@app.route('/', methods=['GET', 'POST'])
def project_home():
    return render_template('project_home.html', all_projects=ProjectDetails.query.all())


@app.route('/register-project', methods=['GET', 'POST'])
def register_project():
    if request.method == 'POST':
        project_name = request.form['project_name']
        project_start_date = request.form['project_start_date']
        project_end_date = request.form['project_end_date']
        project_manager_name = request.form['project_manager_name']
        project_manager_email = request.form['project_manager_email']
        project_daily_report_email = request.form['project_daily_report_email']
        
        project_data = {
            "project_id": uuid.uuid4().hex[:8],
            "project_name": project_name, 
            "project_start_date": project_start_date, 
            "project_end_date": project_end_date, 
            "project_manager_name": project_manager_name, 
            "project_manager_email": project_manager_email, 
            "project_daily_report_email": project_daily_report_email
        }
        
        requests.post(f"{PROJECT_MICRO_APP_URL}/register-project", json=project_data)
        return redirect(url_for('project_home'))
    return render_template('project_form.html')


@app.route('/edit-project/<project_id>', methods=['GET', 'POST'])
def edit_project(project_id):
    project = ProjectDetails.query.filter_by(project_id=project_id).first()
    if request.method == 'POST':
        project_data = {
            "project_id": project_id,
            "project_name": request.form['project_name'],
            "project_start_date": request.form['project_start_date'],
            "project_end_date": request.form['project_end_date'],
            "project_manager_name": request.form['project_manager_name'],
            "project_manager_email": request.form['project_manager_email'],
            "project_daily_report_email": request.form['project_daily_report_email']
        }
        requests.put(f"{PROJECT_MICRO_APP_URL}/edit-project/{project_id}", json=project_data)
        return redirect(url_for('project_home'))
    return render_template('project_update.html', project=project)


@app.route('/delete-project/<project_id>', methods=['GET', 'POST'])
def delete_project(project_id):
    requests.delete(f"{PROJECT_MICRO_APP_URL}/delete-project/{project_id}")
    return redirect(url_for('project_home'))


if __name__ == '__main__':
    app.run(port=5007, debug=True)
