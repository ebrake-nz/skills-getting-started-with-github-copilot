from src import app as app_module


def test_get_activities_returns_all_activities(client):
    # Arrange
    expected_keys = set(app_module.activities.keys())

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert set(response.json().keys()) == expected_keys


def test_signup_for_activity_adds_new_participant(client):
    # Arrange
    activity_name = "Science Club"
    email = "new.student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert email in app_module.activities[activity_name]["participants"]


def test_signup_for_activity_rejects_duplicate_participant(client):
    # Arrange
    activity_name = "Science Club"
    duplicate_email = "harper@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": duplicate_email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_participant_is_case_insensitive(client):
    # Arrange
    activity_name = "Science Club"
    email_with_different_case = "HARPER@MERGINGTON.EDU"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants", params={"email": email_with_different_case}
    )

    # Assert
    assert response.status_code == 200
    assert "harper@mergington.edu" not in app_module.activities[activity_name]["participants"]
