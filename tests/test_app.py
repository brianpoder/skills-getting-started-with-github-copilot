import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"], dict)

def test_signup_for_activity_success():
    response = client.post("/activities/Chess Club/signup", params={"email": "testuser@mergington.edu"})
    assert response.status_code == 200
    assert "Signed up testuser@mergington.edu for Chess Club" in response.json()["message"]

    # Clean up: unregister
    client.delete("/activities/Chess Club/unregister", params={"email": "testuser@mergington.edu"})

def test_signup_for_activity_already_signed_up():
    email = "daniel@mergington.edu"
    response = client.post("/activities/Chess Club/signup", params={"email": email})
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"

def test_signup_for_activity_not_found():
    response = client.post("/activities/Nonexistent/signup", params={"email": "nobody@mergington.edu"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

def test_unregister_from_activity_success():
    # First, sign up
    email = "tempuser@mergington.edu"
    client.post("/activities/Chess Club/signup", params={"email": email})
    # Now, unregister
    response = client.delete("/activities/Chess Club/unregister", params={"email": email})
    assert response.status_code == 200
    assert "Unregistered tempuser@mergington.edu from Chess Club" in response.json()["message"]

def test_unregister_from_activity_not_registered():
    response = client.delete("/activities/Chess Club/unregister", params={"email": "notregistered@mergington.edu"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Student not registered"

def test_unregister_from_activity_not_found():
    response = client.delete("/activities/Nonexistent/unregister", params={"email": "nobody@mergington.edu"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
