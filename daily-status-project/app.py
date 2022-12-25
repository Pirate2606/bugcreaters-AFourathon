from flask import render_template, request, redirect, url_for
from models import app, db, ProjectDetails
from config import Config
import uuid
import requests
from datetime import datetime

app.config.from_object(Config)
db.init_app(app)
PROJECT_MICRO_APP_URL = 'http://127.0.0.1:5008'
TEAM_MICRO_APP_URL = 'http://127.0.0.1:5009'
# PROJECT_MICRO_APP_URL = 'http://project-micro-app:5008'
# TEAM_MICRO_APP_URL = 'http://team-micro-app:5009'


@app.before_first_request
def before_first_request():
    db.create_all()
    db.session.commit()


@app.route('/', methods=['GET', 'POST'])
def project_home():
    all_projects = requests.get(f"{PROJECT_MICRO_APP_URL}/get-projects").json()['projects']
    for project in all_projects:
            project['project_start_date'] = datetime.strptime(project['project_start_date'], '%Y-%m-%d %H:%M:%S')
            project['project_end_date'] = datetime.strptime(project['project_end_date'], '%Y-%m-%d %H:%M:%S')
    return render_template('project_home.html', all_projects=all_projects)


@app.route('/add-team/<project_id>', methods=['GET', 'POST'])
def add_team(project_id):
    all_teams = requests.get(f"{TEAM_MICRO_APP_URL}/get-teams/{project_id}").json()['teams']
    project = requests.get(f"{PROJECT_MICRO_APP_URL}/get-project/{project_id}").json()['projects'][0]
    if len(all_teams) > 0 and request.args.get('t') is None:
        for team in all_teams:
            team['team_start_date'] = datetime.strptime(team['team_start_date'], '%Y-%m-%d %H:%M:%S')
            team['team_end_date'] = datetime.strptime(team['team_end_date'], '%Y-%m-%d %H:%M:%S')
        return render_template('teams.html', project_id=project_id, all_teams=all_teams, project_name=project['project_name'])
    if request.method == "POST":
        team_data = {
            "project_id": project_id,
            "team_id": uuid.uuid4().hex[:8],
            "team_name": request.form['team_name'],
            "team_start_date": request.form['team_start_date'],
            "team_end_date": request.form['team_end_date'],
            "team_lead_name": request.form['team_lead_name'],
            "team_lead_email": request.form['team_lead_email'],
            "team_members": request.form['team_members']
        }
        
        requests.post(f"{TEAM_MICRO_APP_URL}/register-team", json=team_data)
        return redirect(url_for('add_team', project_id=project_id))
    return render_template('add_team.html', edit=False)
 
 
@app.route('/edit-team/<project_id>/<team_id>', methods=['GET', 'POST'])
def edit_team(project_id, team_id):
    team = requests.get(f"{TEAM_MICRO_APP_URL}/get-team/{team_id}").json()['teams'][0]
    if request.method == "POST":
        team_data = {
            "project_id": project_id,
            "team_id": team_id,
            "team_name": request.form['team_name'],
            "team_start_date": request.form['team_start_date'],
            "team_end_date": request.form['team_end_date'],
            "team_lead_name": request.form['team_lead_name'],
            "team_lead_email": request.form['team_lead_email'],
            "team_members": request.form['team_members']
        }
        
        requests.put(f"{TEAM_MICRO_APP_URL}/edit-team", json=team_data)
        return redirect(url_for('add_team', project_id=project_id))
    return render_template('add_team.html', team=team, edit=True)
 
 
@app.route('/delete-team/<project_id>/<team_id>', methods=['GET', 'POST'])
def delete_team(project_id, team_id):
    requests.delete(f"{TEAM_MICRO_APP_URL}/delete-team/{team_id}")
    return redirect(url_for('add_team', project_id=project_id))
        

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
