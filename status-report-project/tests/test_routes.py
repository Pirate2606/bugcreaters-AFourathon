import pytest
from mockito import when, mock
import requests
import uuid
import os, sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from app import app


# Setting up micro-apps LOCAL
PROJECT_MICRO_APP_URL = 'http://127.0.0.1:5001'
EMAIL_REPORT_MICRO_APP_URL = 'http://127.0.0.1:5002'
UPDATE_STATUS_MICRO_APP = 'http://127.0.0.1:5050'

# Setting up micro-apps DOCKER
# PROJECT_MICRO_APP_URL = 'http://project-micro-app:5001'
# EMAIL_REPORT_MICRO_APP_URL = 'http://email-report-micro-app:5002'
# UPDATE_STATUS_MICRO_APP = 'http://update-status-micro-app:5050'

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["DEBUG"] = False
    with app.test_client() as client:
        yield client

def test_home_route(client):
    projects = ['{"id": 1, "project_id": "abcd1234", "project_name": "New name", "project_start_date": "2021-01-01 00:00:00", "project_end_date": "2021-01-01 00:00:00", "project_manager_name": "project_manager_name", "project_manager_email": "email@gmail.com", "project_daily_report_email": "mail@abc.com"}']
    response = mock({
        'status_code': 200,
        'json': lambda: {'projects': projects}
    }, spec=requests.Response)
    when(requests).get(f"{PROJECT_MICRO_APP_URL}/get-projects").thenReturn(response)

    response = client.get('/')
    assert response.status_code == 200


def test_register_project_get(client):
    response = client.get('/register-project')
    assert response.status_code == 200


def test_edit_project_get(client):
    projects = ['{"id": 1, "project_id": "abcd1234", "project_name": "New name", "project_start_date": "2021-01-01 00:00:00", "project_end_date": "2021-01-01 00:00:00", "project_manager_name": "project_manager_name", "project_manager_email": "email@gmail.com", "project_daily_report_email": "mail@abc.com"}']
    response = mock({
        'status_code': 200,
        'json': lambda: {'projects': projects}
    }, spec=requests.Response)
    when(requests).get(f"{PROJECT_MICRO_APP_URL}/get-project/abcd1234").thenReturn(response)
    response = client.get('/edit-project/abcd1234')
    assert response.status_code == 200


def test_edit_project_post(client):
    project_data = {
        "project_id": 'abcd1234',
        "project_name": "project_name", 
        "project_start_date": '2021-01-01',
        "project_end_date": '2021-01-01',
        "project_manager_name": "project_manager_name", 
        "project_manager_email": "email@gmail.com", 
        "project_daily_report_email": "mail@abc.com"
    }
    response = mock({
        'status_code': 200,
        'json': lambda: {"message": "Project updated successfully"}
    }, spec=requests.Response)
    when(requests).put(f"{PROJECT_MICRO_APP_URL}/edit-project/abcd1234", json=project_data).thenReturn(response)
    response = client.post("/edit-project/abcd1234", data=project_data)
    assert response.status_code == 302


def test_delete_project(client):
    response = mock({
        'status_code': 200,
        'json': lambda: {"message": "Project deleted successfully"}
    }, spec=requests.Response)
    when(requests).delete(f"{PROJECT_MICRO_APP_URL}/delete-project/abcd1234").thenReturn(response)
    response = client.post('/delete-project/abcd1234')
    assert response.status_code == 302
