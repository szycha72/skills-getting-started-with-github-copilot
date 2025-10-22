from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def setup_function():
    # Reset activities to a known state before each test
    activities.clear()
    activities.update({
        "Test Club": {
            "description": "A test activity",
            "schedule": "Now",
            "max_participants": 5,
            "participants": ["alice@example.com"]
        }
    })


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert "Test Club" in data
    assert data["Test Club"]["description"] == "A test activity"


def test_signup_success():
    resp = client.post("/activities/Test%20Club/signup?email=bob%40example.com")
    assert resp.status_code == 200
    data = resp.json()
    assert "Signed up bob@example.com for Test Club" in data.get("message", "")
    assert "bob@example.com" in activities["Test Club"]["participants"]


def test_signup_duplicate_fails():
    # alice is already registered in setup
    resp = client.post("/activities/Test%20Club/signup?email=alice%40example.com")
    assert resp.status_code == 400


def test_unregister_success():
    resp = client.delete("/activities/Test%20Club/unregister?email=alice%40example.com")
    assert resp.status_code == 200
    data = resp.json()
    assert "Unregistered alice@example.com from Test Club" in data.get("message", "")
    assert "alice@example.com" not in activities["Test Club"]["participants"]


def test_unregister_nonexistent_fails():
    resp = client.delete("/activities/Test%20Club/unregister?email=charlie%40example.com")
    assert resp.status_code == 400
