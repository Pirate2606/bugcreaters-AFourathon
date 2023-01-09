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


def test_add_status(client):
    skill_data = {
        "skill_name": "skill_name",
        "skill_domain": "skill_domain"
    }
    response = client.post('/add-skill', json=skill_data)
    assert response.status_code == 200
    assert response.json == {"message": "Skill added successfully"}


def test_get_all_skills(client):
    response = client.get('/get-skills')
    skills = [{'id': 1, 'skill_domain': 'skill_domain', 'skill_name': 'skill_name'}]
    assert response.status_code == 200
    assert response.json == {"skills": skills}


def test_update_skills(client):
    skill_data = {
        "skill_name": "skill_name_2",
        "skill_domain": "skill_domain"
    }
    response = client.put('/update-skill/1', json=skill_data)
    assert response.status_code == 200
    assert response.json == {"message": "Skill updated successfully"}


def test_get_skill(client):
    response = client.get('/get-skill/1')
    skills = [{'id': 1, 'skill_domain': 'skill_domain', 'skill_name': 'skill_name_2'}]
    assert response.status_code == 200
    assert response.json == {"skill": skills}



def test_delete_skill(client):
    response = client.delete('/delete-skill/1')
    assert response.status_code == 200
    assert response.json == {"message": "Skill deleted successfully"}
