from src.app import activities

REQUIRED_FIELDS = {"description", "schedule", "max_participants", "participants"}


def test_root_redirects_to_static_index(client):
    # Arrange
    expected_location = "/static/index.html"

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == expected_location


def test_get_activities_returns_200_with_dict(client):
    # Arrange
    expected_names = set(activities)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, dict)
    assert set(body) == expected_names


def test_get_activities_each_has_required_fields(client):
    # Arrange
    # (seed data only)

    # Act
    response = client.get("/activities")

    # Assert
    for name, details in response.json().items():
        assert REQUIRED_FIELDS <= set(details), f"{name} is missing fields"
        assert isinstance(details["max_participants"], int)
        assert isinstance(details["participants"], list)


def test_get_activities_seed_data_within_capacity(client):
    # Arrange
    # (seed data only)

    # Act
    response = client.get("/activities")

    # Assert
    for name, details in response.json().items():
        assert len(details["participants"]) <= details["max_participants"], (
            f"{name} is over capacity"
        )
