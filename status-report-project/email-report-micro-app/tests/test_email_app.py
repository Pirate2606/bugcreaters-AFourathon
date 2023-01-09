import pytest
import os, sys

# Addind parent directory to path so that app.py can be imported
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from app import app
from send_mail import send_project_status_mail
from datetime import datetime


# Initial setup for testing
@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["DEBUG"] = False
    with app.test_client() as client:
        yield client


# Testing the send mail function
def test_send_mail_function(client):
    with app.app_context():
        mail_list = [
            {
                "project_status": "Completed",
                "project_risk": "High",
                "project_highlights": "Project is completed",
                "week_ending_date": datetime.now(),
            },
            {
                "project_name": "Test Project", 
                "project_manager_name": "Aditya Naitan",
                "project_daily_report_email": "adityanaitan@gmail.com,adityanaitanuit@gmail.com"
            }
        ]
        response = send_project_status_mail(mail_list)
        assert response == "Mail sent successfully"
