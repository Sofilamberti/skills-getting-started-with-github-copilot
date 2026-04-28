def test_root_redirect(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.url.path == "/static/index.html"


def test_get_activities(client):
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]


def test_signup_success(client):
    response = client.post("/activities/Chess Club/signup?email=newstudent@mergington.edu")
    assert response.status_code == 200
    data = response.json()
    assert "Signed up" in data["message"]


def test_signup_duplicate(client):
    # First signup
    client.post("/activities/Chess Club/signup?email=duplicate@mergington.edu")
    # Second signup should fail
    response = client.post("/activities/Chess Club/signup?email=duplicate@mergington.edu")
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"]


def test_signup_invalid_activity(client):
    response = client.post("/activities/Invalid Activity/signup?email=test@mergington.edu")
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_unregister_success(client):
    # First signup
    client.post("/activities/Chess Club/signup?email=unregister@mergington.edu")
    # Then unregister
    response = client.delete("/activities/Chess Club/unregister?email=unregister@mergington.edu")
    assert response.status_code == 200
    data = response.json()
    assert "Unregistered" in data["message"]


def test_unregister_not_registered(client):
    response = client.delete("/activities/Chess Club/unregister?email=notregistered@mergington.edu")
    assert response.status_code == 404
    data = response.json()
    assert "not registered" in data["detail"]


def test_unregister_invalid_activity(client):
    response = client.delete("/activities/Invalid Activity/unregister?email=test@mergington.edu")
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]
