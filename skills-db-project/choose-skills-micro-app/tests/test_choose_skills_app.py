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


def test_register_user(client):
    user_data = {
        "user_id": "user_id",
        "user_name": "user_name",
        "full_name": "full_name",
        "password": "password"
    }
    response = client.post('/register', json=user_data)
    assert response.status_code == 200
    assert response.json == {"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoidXNlcl9pZCIsInVzZXJfbmFtZSI6InVzZXJfbmFtZSJ9.f159qjswUOoMtjtj0G50gDJ0gvbVVqAQukiyTU9YVRk"}


def test_login_user(client):
    user_data = {
        "user_name": "user_name",
        "password": "password"
    }
    response = client.post('/login', json=user_data)
    assert response.status_code == 200
    assert response.json == {"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoidXNlcl9pZCIsInVzZXJfbmFtZSI6InVzZXJfbmFtZSJ9.f159qjswUOoMtjtj0G50gDJ0gvbVVqAQukiyTU9YVRk"}


def test_add_status(client):
    project_data = {
        "skill_name": "test_skill",
        "skill_domain": "test_domain",
        "skill_level": "test_level",
        "yoe": 1
    }
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoidXNlcl9pZCIsInVzZXJfbmFtZSI6InVzZXJfbmFtZSJ9.f159qjswUOoMtjtj0G50gDJ0gvbVVqAQukiyTU9YVRk"
    header = {'Authorization': 'Bearer ' + token}
    response = client.post('/choose-skills', json=project_data, headers=header)
    assert response.status_code == 200
    assert response.json == {"message": "Skill added successfully"}


def test_update_skills(client):
    skill_data = {
        "skill_level": "test_level",
        "yoe": 2
    }
    response = client.put('/update-skill/1', json=skill_data)
    assert response.status_code == 200
    assert response.json == {"message": "Skill updated successfully"}


def test_get_skill(client):
    response = client.get('/get-skills/user_id')
    skills = [{'id': 1, 'skill_domain': 'test_domain', 'skill_level': 'test_level', 'skill_name': 'test_skill', 'user_id': 'user_id', 'yoe': 2}]
    assert response.status_code == 200
    assert response.json == {"skills": skills}


def test_delete_skill(client):
    response = client.delete('/delete-skill/1')
    assert response.status_code == 200
    assert response.json == {"message": "Skill deleted successfully"}
