from urllib.parse import quote

from src.app import activities


def test_unregister_removes_an_existing_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "daniel@mergington.edu"
    encoded_activity_name = quote(activity_name, safe="")
    assert email in activities[activity_name]["participants"]

    # Act
    response = client.delete(f"/activities/{encoded_activity_name}/participants", params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert payload == {"message": f"Unregistered {email} from {activity_name}"}
    assert email not in activities[activity_name]["participants"]


def test_unregister_missing_participant_returns_not_found(client):
    # Arrange
    activity_name = "Chess Club"
    email = "ghost@mergington.edu"
    encoded_activity_name = quote(activity_name, safe="")
    assert email not in activities[activity_name]["participants"]

    # Act
    response = client.delete(f"/activities/{encoded_activity_name}/participants", params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Participant not found for this activity"


def test_unregister_unknown_activity_returns_not_found(client):
    # Arrange
    activity_name = "Robotics Club"
    email = "student@mergington.edu"
    encoded_activity_name = quote(activity_name, safe="")

    # Act
    response = client.delete(f"/activities/{encoded_activity_name}/participants", params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Activity not found"
