from flask import render_template, request, redirect, url_for, Flask
from models import db, Users
from config import Config
from datetime import datetime, timedelta
import uuid
import requests
import logging
import json


# Setting up logging
logging.basicConfig(filename='logs/app.log', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

# Setting up app
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Setting up micro-apps LOCAL
PROJECT_MICRO_APP_URL = 'http://127.0.0.1:5001'
EMAIL_REPORT_MICRO_APP_URL = 'http://127.0.0.1:5002'
UPDATE_STATUS_MICRO_APP = 'http://127.0.0.1:5050'

# Setting up micro-apps DOCKER
# PROJECT_MICRO_APP_URL = 'http://project-micro-app:5001'
# EMAIL_REPORT_MICRO_APP_URL = 'http://email-report-micro-app:5002'
# UPDATE_STATUS_MICRO_APP = 'http://update-status-micro-app:5050'


# Create tables before first request
@app.before_first_request
def before_first_request():
    db.create_all()
    # populating users table
    full_names = ["Asif Habib", "Aditya Naitan", "Keshav Sharma", "Ajay Sharma"]
    user_names = ["asif_habib", "aditya_naitan", "keshav", "ajay_sharma"]
    user_emails = ["asifhabib@gmail.com", "adityanaitan@gmail.com", "keshav@gmail.com", "adityanaitanuit@gmail.com"]
    get_users = Users.query.all()
    if len(get_users) != 4:
        for i in range(len(full_names)):
            user = Users(
                full_name=full_names[i],
                user_name=user_names[i],
                user_email=user_emails[i]
            )
            db.session.add(user)
    db.session.commit()


# Home Page
@app.route('/', methods=['GET', 'POST'])
def project_home():
    # Getting all the projects registered
    projects = requests.get(f"{PROJECT_MICRO_APP_URL}/get-projects").json()['projects']
    
    # Converting to JSON
    for i in range(len(projects)):
        projects[i] = json.loads(projects[i])
    
    # Converting string to datetime object
    for project in projects:
        project['project_start_date'] = datetime.strptime(project['project_start_date'], '%Y-%m-%d %H:%M:%S')
        project['project_end_date'] = datetime.strptime(project['project_end_date'], '%Y-%m-%d %H:%M:%S')
    return render_template('project_home.html', all_projects=projects)


# Register a new project
@app.route('/register-project', methods=['GET', 'POST'])
def register_project():
    if request.method == 'POST':
        # Getting data from the form
        project_name = request.form['project_name']
        project_start_date = request.form['project_start_date']
        project_end_date = request.form['project_end_date']
        project_manager_name = request.form['project_manager_name']
        project_manager_email = request.form['project_manager_email']
        project_daily_report_email = request.form['project_daily_report_email']
        
        # Adding project to the database
        project_data = {
            "project_id": uuid.uuid4().hex[:8],
            "project_name": project_name, 
            "project_start_date": project_start_date, 
            "project_end_date": project_end_date, 
            "project_manager_name": project_manager_name, 
            "project_manager_email": project_manager_email, 
            "project_daily_report_email": project_daily_report_email
        }
        
        # Sending data to the project micro app
        requests.post(f"{PROJECT_MICRO_APP_URL}/register-project", json=project_data)
        return redirect(url_for('project_home'))
    
    # Getting all the users
    users = []
    for user in Users.query.all():
        users.append({'user_name': user.user_name, 'user_email': user.user_email})
    return render_template('project_form.html', users=users)


# Edit a project
@app.route('/edit-project/<project_id>', methods=['GET', 'POST'])
def edit_project(project_id):
    # Getting the project details
    project = requests.get(f"{PROJECT_MICRO_APP_URL}/get-project/{project_id}").json()['projects'][0]
    project = json.loads(project)
    if request.method == 'POST':
        # Getting data from the form
        project_data = {
            "project_id": project_id,
            "project_name": request.form['project_name'],
            "project_start_date": request.form['project_start_date'],
            "project_end_date": request.form['project_end_date'],
            "project_manager_name": request.form['project_manager_name'],
            "project_manager_email": request.form['project_manager_email'],
            "project_daily_report_email": request.form['project_daily_report_email']
        }
        
        # Updating the project details by sending data to the project micro app
        requests.put(f"{PROJECT_MICRO_APP_URL}/edit-project/{project_id}", json=project_data)
        return redirect(url_for('project_home'))
    
    # Getting all the user details
    users = []
    show_users = []
    emails = project['project_daily_report_email'].split(',')
    for user in Users.query.all():
        if user.user_email not in emails:
            show_users.append({'user_name': user.user_name, 'user_email': user.user_email})
        users.append({'user_name': user.user_name, 'user_email': user.user_email})
    return render_template('project_update.html', project=project, users=users, show_users=show_users)


# Delete a project
@app.route('/delete-project/<project_id>', methods=['GET', 'POST'])
def delete_project(project_id):
    requests.delete(f"{PROJECT_MICRO_APP_URL}/delete-project/{project_id}")
    return redirect(url_for('project_home'))


# Filter projects based on the week
@app.route('/filter-projects', methods=['GET', 'POST'])
def filter_projects():
    if request.method == 'POST':
        # Getting all the projects registered
        projects = requests.get(f"{PROJECT_MICRO_APP_URL}/get-projects").json()['projects']
        for i in range(len(projects)):
            projects[i] = json.loads(projects[i])
        for project in projects:
            project['project_start_date'] = datetime.strptime(project['project_start_date'], '%Y-%m-%d %H:%M:%S')
            project['project_end_date'] = datetime.strptime(project['project_end_date'], '%Y-%m-%d %H:%M:%S')
        
        # Getting the selected week from form
        week_start_date = datetime.strptime(request.form["week"] + '-1', "%Y-W%W-%w")
        week_end_date = week_start_date + timedelta(days=4)
        
        # Getting the project stats for the selected week
        project_stats = requests.get(f"{UPDATE_STATUS_MICRO_APP}/get-status/<{str(week_end_date).split(' ')[0]}>").json()['status']
        for i in range(len(project_stats)):
            project_stats[i] = json.loads(project_stats[i])
        project_ids = []
        for stat in project_stats:
            stat['week_ending_date'] = datetime.strptime(stat['week_ending_date'], '%Y-%m-%d %H:%M:%S')
            project_ids.append(stat['project_id'])
        all_projects = []
        already_projects = []
        for project in projects:
            if ((project['project_start_date'] >= week_start_date and project['project_start_date'] <= week_end_date) or 
                (project['project_start_date'] <= week_start_date and project['project_end_date'] >= week_start_date)):
                if project['project_id'] not in project_ids:
                    all_projects.append(project)
                else:
                    already_projects.append(project)
        return render_template('filter_projects.html', all_projects=all_projects, week_end_date=week_end_date, already_projects=already_projects, project_stats=project_stats)
    return render_template('filter_projects.html')


# Adding project status
@app.route('/project-status/<project_id>', methods=['GET', 'POST'])
def project_status(project_id):
    if request.method == "POST":
        # Getting the project status data from the form
        status_data = {
            "project_status": request.form['project_status'],
            "project_risk": request.form['project_risk'],
            "project_highlights": request.form['project_highlights'],
            "week_ending_date": request.form['week_ending_date']
        }
        
        # Adding the project status by sending data to the update status micro app
        requests.post(f"{UPDATE_STATUS_MICRO_APP}/project-status/{project_id}", json=status_data)
        return redirect(url_for('filter_projects'))
    project = requests.get(f"{PROJECT_MICRO_APP_URL}/get-project/{project_id}").json()['projects'][0]
    project = json.loads(project)
    return render_template('project_status.html', project=project, week_end_date=request.args.get('w').split(" ")[0])


# Update project status
@app.route('/update-status/<project_id>', methods=['GET', 'POST'])
def update_status(project_id):
    if request.method == "POST":
        status_data = {
            "project_status": request.form['project_status'],
            "project_risk": request.form['project_risk'],
            "project_highlights": request.form['project_highlights'],
            "week_ending_date": request.form['week_ending_date']
        }
        requests.put(f"{UPDATE_STATUS_MICRO_APP}/project-status/{project_id}", json=status_data)
        return redirect(url_for('filter_projects'))
    project = requests.get(f"{PROJECT_MICRO_APP_URL}/get-project/{project_id}").json()['projects'][0]
    project = json.loads(project)
    status = requests.get(f"{UPDATE_STATUS_MICRO_APP}/project-status/{project_id}?w={request.args.get('w').split(' ')[0]}").json()["status"][0]
    status = json.loads(status)
    return render_template('project_status_update.html', project=project, status=status)


# Delete project status
@app.route('/delete-satus/<project_id>')
def delete_status(project_id):
    requests.delete(f"{UPDATE_STATUS_MICRO_APP}/project-status/{project_id}?w={request.args.get('w').split(' ')[0]}")
    return redirect(url_for('filter_projects'))


# Send project status mail
@app.route('/project-status-mail/<project_id>')
def project_status_mail(project_id):
    requests.get(f"{EMAIL_REPORT_MICRO_APP_URL}/send-project-status-mail/{project_id}?w={request.args.get('w').split(' ')[0]}")
    return redirect(url_for('project_home'))


if __name__ == '__main__':
    app.run()
