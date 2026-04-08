from urllib.parse import quote

from src.app import activities


def test_root_redirects_to_static_index(client):
    # Arrange
    path = "/"

    # Act
    response = client.get(path, follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_available_activities(client):
    # Arrange
    expected_activity = "Chess Club"

    # Act
    response = client.get("/activities")
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert expected_activity in payload
    assert payload[expected_activity]["description"]
    assert payload[expected_activity]["schedule"]
    assert isinstance(payload[expected_activity]["max_participants"], int)
    assert isinstance(payload[expected_activity]["participants"], list)


def test_signup_for_activity_adds_a_new_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    encoded_activity_name = quote(activity_name, safe="")
    assert email not in activities[activity_name]["participants"]

    # Act
    response = client.post(f"/activities/{encoded_activity_name}/signup", params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert payload == {"message": f"Signed up {email} for {activity_name}"}
    assert email in activities[activity_name]["participants"]


def test_signup_for_activity_rejects_duplicate_registration(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    encoded_activity_name = quote(activity_name, safe="")

    # Act
    response = client.post(f"/activities/{encoded_activity_name}/signup", params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 400
    assert payload["detail"] == "Student already signed up for this activity"


def test_signup_for_unknown_activity_returns_not_found(client):
    # Arrange
    activity_name = "Robotics Club"
    email = "student@mergington.edu"
    encoded_activity_name = quote(activity_name, safe="")

    # Act
    response = client.post(f"/activities/{encoded_activity_name}/signup", params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Activity not found"
