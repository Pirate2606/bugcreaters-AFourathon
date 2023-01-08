import pytest
import os, sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["DEBUG"] = False
    with app.test_client() as client:
        yield client


def test_register_status(client):
    status_data = {
        "project_id": 'abcd1234',
        "project_status": "Completed", 
        "project_risk": "Low", 
        "project_highlights": "Comments", 
        "week_ending_date": "2021-01-01"
    }
    response = client.post('/project-status/abcd1234', json=status_data)
    assert response.status_code == 200
    assert response.json == {"message": "Status registered successfully"}


def test_edit_status(client):
    status_data = {
        "project_status": "Completed", 
        "project_risk": "Very Low", 
        "project_highlights": "Comments", 
        "week_ending_date": "2021-01-01"
    }
    response = client.put('/project-status/abcd1234', json=status_data)
    assert response.status_code == 200
    assert response.json == {"message": "Status updated successfully"}


def test_get_status(client):
    response = client.get('/project-status/abcd1234?w=2021-01-01')
    status = ['{"id": 1, "project_id": "abcd1234", "project_status": "Completed", "project_risk": "Very Low", "project_highlights": "Comments", "week_ending_date": "2021-01-01"}']
    assert response.status_code == 200
    assert response.json == {"status": status}


def test_all_weekly_status(client):
    response = client.get('/get-status/<2021-01-01>')
    status = ['{"id": 1, "project_id": "abcd1234", "project_status": "Completed", "project_risk": "Very Low", "project_highlights": "Comments", "week_ending_date": "2021-01-01"}']
    assert response.status_code == 200
    assert response.json == {"status": status}


def test_delete_status(client):
    response = client.delete('/project-status/abcd1234?w=2021-01-01')
    assert response.status_code == 200
    assert response.json == {"message": "Status deleted successfully"}
