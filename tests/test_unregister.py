from src.app import activities


def test_unregister_registered_email_removes_participant(client):
    # Arrange
    activity = "Chess Club"
    email = activities[activity]["participants"][0]
    initial_count = len(activities[activity]["participants"])

    # Act
    response = client.delete(
        f"/activities/{activity}/unregister", params={"email": email}
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity}"}
    assert email not in activities[activity]["participants"]
    assert len(activities[activity]["participants"]) == initial_count - 1


def test_unregister_unknown_activity_returns_404(client):
    # Arrange
    activity = "Underwater Basket Weaving"
    email = "student@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity}/unregister", params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_unregistered_email_returns_404(client):
    # Arrange
    activity = "Chess Club"
    email = "nobody@mergington.edu"
    initial_participants = list(activities[activity]["participants"])

    # Act
    response = client.delete(
        f"/activities/{activity}/unregister", params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"
    assert activities[activity]["participants"] == initial_participants


def test_signup_after_unregister_succeeds(client):
    # Arrange
    activity = "Chess Club"
    email = activities[activity]["participants"][0]
    client.delete(f"/activities/{activity}/unregister", params={"email": email})
    assert email not in activities[activity]["participants"]

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert email in activities[activity]["participants"]
