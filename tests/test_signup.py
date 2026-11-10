from src.app import activities


def test_signup_with_new_email_adds_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    initial_count = len(activities[activity]["participants"])

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity}"}
    assert email in activities[activity]["participants"]
    assert len(activities[activity]["participants"]) == initial_count + 1


def test_signup_unknown_activity_returns_404(client):
    # Arrange
    activity = "Underwater Basket Weaving"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_duplicate_email_returns_400(client):
    # Arrange
    activity = "Chess Club"
    email = activities[activity]["participants"][0]
    initial_participants = list(activities[activity]["participants"])

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"
    assert activities[activity]["participants"] == initial_participants


def test_signup_when_activity_full_returns_400(client):
    # Arrange
    activity = "Chess Club"
    details = activities[activity]
    details["participants"] = [
        f"student{i}@mergington.edu" for i in range(details["max_participants"])
    ]
    email = "late@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is full"
    assert email not in details["participants"]
    assert len(details["participants"]) == details["max_participants"]


def test_signup_missing_email_returns_422(client):
    # Arrange
    activity = "Chess Club"
    initial_participants = list(activities[activity]["participants"])

    # Act
    response = client.post(f"/activities/{activity}/signup")

    # Assert
    assert response.status_code == 422
    assert activities[activity]["participants"] == initial_participants
