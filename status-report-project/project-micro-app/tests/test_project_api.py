import pytest
import os, sys

# Addind parent directory to path so that app.py can be imported
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from app import app

# Setting up micro-apps
@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["DEBUG"] = False
    with app.test_client() as client:
        yield client


def test_register_project(client):
    project_data = {
        "project_id": 'abcd1234',
        "project_name": "project_name", 
        "project_start_date": '2021-01-01',
        "project_end_date": '2021-01-01',
        "project_manager_name": "project_manager_name", 
        "project_manager_email": "email@gmail.com", 
        "project_daily_report_email": "mail@abc.com"
    }
    response = client.post('/register-project', json=project_data)
    assert response.status_code == 200
    assert response.json == {"message": "Project registered successfully"}


def test_edit_project(client):
    project_data = {
        "project_id": 'abcd1234',
        "project_name": "New name", 
        "project_start_date": '2021-01-01',
        "project_end_date": '2021-01-01',
        "project_manager_name": "project_manager_name",
        "project_manager_email": "email@gmail.com", 
        "project_daily_report_email": "mail@abc.com"
    }
    response = client.put('/edit-project/abcd1234', json=project_data)
    assert response.status_code == 200
    assert response.json == {"message": "Project updated successfully"}


def test_get_project_by_id(client):
    response = client.get('/get-project/abcd1234')
    projects = ['{"id": 1, "project_id": "abcd1234", "project_name": "New name", "project_start_date": "2021-01-01 00:00:00", "project_end_date": "2021-01-01 00:00:00", "project_manager_name": "project_manager_name", "project_manager_email": "email@gmail.com", "project_daily_report_email": "mail@abc.com"}']
    assert response.status_code == 200
    assert response.json == {"projects": projects}


def test_get_all_projects(client):
    response = client.get('/get-projects')
    projects = ['{"id": 1, "project_id": "abcd1234", "project_name": "New name", "project_start_date": "2021-01-01 00:00:00", "project_end_date": "2021-01-01 00:00:00", "project_manager_name": "project_manager_name", "project_manager_email": "email@gmail.com", "project_daily_report_email": "mail@abc.com"}']
    assert response.status_code == 200
    assert response.json == {'projects': projects}


def test_delete_project(client):
    response = client.delete('/delete-project/abcd1234')
    assert response.status_code == 200
    assert response.json == {"message": "Project deleted successfully"}
