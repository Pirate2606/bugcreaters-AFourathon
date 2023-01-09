import pytest
from mockito import when, mock
import requests
import uuid
import os, sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from app import app


SKILLS_LIST_MICRO_APP_URL = app.config['SKILLS_LIST_MICRO_APP_URL']
CHOOSE_SKILLS_MICRO_APP_URL = app.config['CHOOSE_SKILLS_MICRO_APP_URL']
SKILLS_REPORT_MICRO_APP_URL = app.config['SKILLS_REPORT_MICRO_APP_URL']


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["DEBUG"] = False
    with app.test_client() as client:
        yield client


def test_home_route(client):
    skills = [{'id': 1, 'skill_domain': 'skill_domain', 'skill_name': 'skill_name'}]
    response = mock({
        'status_code': 200,
        'json': lambda: {'skills': skills}
    }, spec=requests.Response)
    when(requests).get(f"{SKILLS_LIST_MICRO_APP_URL}/get-skills").thenReturn(response)

    response = client.get('/')
    assert response.status_code == 200


def test_add_skills_route(client):
    skill_data = {
        "skill_name": "skill_name",
        "skill_domain": "skill_domain"
    }
    response = mock({
        'status_code': 200,
        'json': lambda: {"message": "Skill added successfully"}
    }, spec=requests.Response)
    when(requests).post(f"{SKILLS_LIST_MICRO_APP_URL}/add-skill", json=skill_data).thenReturn(response)

    response = client.post('/add-skills', data=skill_data)
    assert response.status_code == 302


def test_skills_route(client):
    skills = [{'id': 1, 'skill_domain': 'skill_domain', 'skill_name': 'skill_name'}]
    response = mock({
        'status_code': 200,
        'json': lambda: {'skills': skills}
    }, spec=requests.Response)
    when(requests).get(f"{SKILLS_LIST_MICRO_APP_URL}/get-skills").thenReturn(response)

    response = client.get('/skills')
    assert response.status_code == 200


def test_delete_route(client):
    response = mock({
        'status_code': 200,
        'json': lambda: {"message": "Skill deleted successfully"}
    }, spec=requests.Response)
    when(requests).delete(f"{SKILLS_LIST_MICRO_APP_URL}/delete-skill/1").thenReturn(response)

    response = client.post('/delete?skill_id=1')
    assert response.status_code == 302


def test_update_route(client):
    skill_data = {
        "skill_id": 1,
        "skill_name": "skills_name",
        "skill_domain": "skill_domain"
    }
    data = {
        "skill_name": "skill_name",
        "skill_domain": "skill_domain"
    }
    response = mock({
        'status_code': 200,
        'json': lambda: {"message": "Skill updated successfully"}
    }, spec=requests.Response)
    when(requests).post(f"{SKILLS_LIST_MICRO_APP_URL}/update-skill/1", json=data).thenReturn(response)

    response = client.post('/update', data=skill_data)
    assert response.status_code == 302


def test_update_skill_route(client):
    data = {
        "skill_level": "expert",
        "yoe": 5
    }
    response = mock({
        'status_code': 200,
        'json': lambda: {"message": "Skill updated successfully"}
    }, spec=requests.Response)
    when(requests).put(f"{CHOOSE_SKILLS_MICRO_APP_URL}/update-skill/1", json=data).thenReturn(response)

    response = client.get('/update-skill/1?y=5&l=expert')
    assert response.status_code == 302
