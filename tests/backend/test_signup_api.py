"""Backend tests for FastAPI signup behavior."""

import pytest


class TestSignupApi:
    def test_signup_successful_adds_participant(self, client, reset_activities, sample_email, sample_activity_name):
        response = client.post(f"/activities/{sample_activity_name}/signup?email={sample_email}")

        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert sample_email in data["message"]

        activities = client.get("/activities").json()
        assert sample_email in activities[sample_activity_name]["participants"]

    def test_signup_duplicate_returns_400(self, client, reset_activities, sample_email, sample_activity_name):
        client.post(f"/activities/{sample_activity_name}/signup?email={sample_email}")
        response = client.post(f"/activities/{sample_activity_name}/signup?email={sample_email}")

        assert response.status_code == 400
        assert response.json()["detail"] == "Student is already registered for this activity"

    def test_signup_nonexistent_activity_returns_404(self, client, reset_activities, sample_email):
        response = client.post(f"/activities/NotAnActivity/signup?email={sample_email}")

        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_signup_multiple_different_participants(self, client, reset_activities, sample_activity_name):
        emails = ["student1@mergington.edu", "student2@mergington.edu"]

        for email in emails:
            response = client.post(f"/activities/{sample_activity_name}/signup?email={email}")
            assert response.status_code == 200

        activities = client.get("/activities").json()
        for email in emails:
            assert email in activities[sample_activity_name]["participants"]
