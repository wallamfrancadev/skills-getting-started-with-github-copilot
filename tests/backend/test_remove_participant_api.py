"""Backend tests for FastAPI participant removal behavior."""


class TestRemoveParticipantApi:
    def test_remove_participant_successful(self, client, reset_activities, sample_email, sample_activity_name):
        client.post(f"/activities/{sample_activity_name}/signup?email={sample_email}")
        response = client.delete(f"/activities/{sample_activity_name}/participants?email={sample_email}")

        assert response.status_code == 200
        assert response.json()["message"] == f"Removed {sample_email} from {sample_activity_name}"

        activities = client.get("/activities").json()
        assert sample_email not in activities[sample_activity_name]["participants"]

    def test_remove_nonexistent_activity_returns_404(self, client, reset_activities, sample_email):
        response = client.delete(f"/activities/NotAnActivity/participants?email={sample_email}")

        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_remove_nonexistent_participant_returns_404(self, client, reset_activities, sample_activity_name):
        response = client.delete(f"/activities/{sample_activity_name}/participants?email=missing@mergington.edu")

        assert response.status_code == 404
        assert response.json()["detail"] == "Participant not found"
