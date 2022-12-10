from flask import render_template, request, redirect, url_for
from models import app, db, ProjectDetails
from config import Config
from datetime import datetime
import uuid


app.config.from_object(Config)
db.init_app(app)


@app.before_first_request
def before_first_request():
    db.create_all()
    db.session.commit()


@app.route('/')
def project_home():
    projects = ProjectDetails.query.all()
    return render_template('project_home.html', projects=projects)


@app.route('/register-project', methods=['GET', 'POST'])
def register_project():
    if request.method == 'POST':
        project_name = request.form['project_name']
        project_start_date = request.form['project_start_date']
        project_end_date = request.form['project_end_date']
        project_manager_name = request.form['project_manager_name']
        project_manager_email = request.form['project_manager_email']
        project_daily_report_email = request.form['project_daily_report_email']
        project = ProjectDetails(project_id=uuid.uuid4().hex[:8],
                                 project_name=project_name,
                                 project_start_date=datetime.strptime(project_start_date, '%Y-%m-%d'),
                                 project_end_date=datetime.strptime(project_end_date, '%Y-%m-%d'),
                                 project_manager_name=project_manager_name,
                                 project_manager_email=project_manager_email,
                                 project_daily_report_email=project_daily_report_email)
        db.session.add(project)
        db.session.commit()
        return redirect(url_for('project_home'))
    return render_template('project_form.html')


@app.route('/edit-project/<project_id>', methods=['GET', 'POST'])
def edit_project(project_id):
    print(project_id)
    project = ProjectDetails.query.filter_by(project_id=project_id).first()
    if request.method == 'POST':
        project.project_name = request.form['project_name']
        project.project_start_date = request.form['project_start_date']
        project.project_end_date = request.form['project_end_date']
        project.project_manager_name = request.form['project_manager_name']
        project.project_manager_email = request.form['project_manager_email']
        project.project_daily_report_email = request.form['project_daily_report_email']
        db.session.commit()
        return redirect(url_for('project_home'))
    return render_template('project_form.html', project=project)


@app.route('/delete-project/<project_id>', methods=['GET', 'POST'])
def delete_project(project_id):
    project = ProjectDetails.query.filter_by(project_id=project_id).first()
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for('project_home'))


if __name__ == '__main__':
    app.run(debug=True)
