"""
Tests for the DELETE /activities/{activity_name}/participants endpoint.

Tests verify participant removal functionality including success cases and error handling
using the AAA (Arrange-Act-Assert) pattern.
"""

import pytest


class TestRemoveParticipant:
    """Tests for removing a participant from an activity."""

    def test_remove_participant_successful(self, client, reset_activities, sample_email, sample_activity_name):
        """
        Test successful removal of a participant.
        
        Arrange: Sign up a participant first
        Act: Make DELETE request to remove participant
        Assert: Response status is 200 and success message is returned
        """
        # Arrange
        email = sample_email
        activity_name = sample_activity_name
        # Sign up the participant first
        client.post(f"/activities/{activity_name}/signup?email={email}")
        
        # Act
        response = client.delete(f"/activities/{activity_name}/participants?email={email}")
        
        # Assert
        assert response.status_code == 200
        assert "message" in response.json()

    def test_remove_participant_removes_from_list(self, client, reset_activities, sample_email, sample_activity_name):
        """
        Test that removing a participant removes them from the participants list.
        
        Arrange: Sign up a participant first
        Act: Make DELETE request to remove participant
        Assert: Participant is no longer in activity's participants list
        """
        # Arrange
        email = sample_email
        activity_name = sample_activity_name
        # Sign up the participant first
        client.post(f"/activities/{activity_name}/signup?email={email}")
        
        # Act
        response = client.delete(f"/activities/{activity_name}/participants?email={email}")
        activities_response = client.get("/activities").json()
        
        # Assert
        assert response.status_code == 200
        assert email not in activities_response[activity_name]["participants"]

    def test_remove_participant_returns_success_message(self, client, reset_activities, sample_email, sample_activity_name):
        """
        Test that removal returns appropriate success message.
        
        Arrange: Sign up a participant first
        Act: Make DELETE request to remove participant
        Assert: Response contains email and activity name in message
        """
        # Arrange
        email = sample_email
        activity_name = sample_activity_name
        # Sign up the participant first
        client.post(f"/activities/{activity_name}/signup?email={email}")
        
        # Act
        response = client.delete(f"/activities/{activity_name}/participants?email={email}")
        data = response.json()
        
        # Assert
        assert response.status_code == 200
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_remove_from_nonexistent_activity_returns_404(self, client, reset_activities, sample_email):
        """
        Test that removing from nonexistent activity returns 404.
        
        Arrange: Prepare email and nonexistent activity name
        Act: Make DELETE request for activity that doesn't exist
        Assert: Response status is 404
        """
        # Arrange
        email = sample_email
        nonexistent_activity = "Nonexistent Activity"
        
        # Act
        response = client.delete(f"/activities/{nonexistent_activity}/participants?email={email}")
        
        # Assert
        assert response.status_code == 404

    def test_remove_from_nonexistent_activity_returns_error_detail(self, client, reset_activities, sample_email):
        """
        Test that removing from nonexistent activity returns error detail.
        
        Arrange: Prepare email and nonexistent activity name
        Act: Make DELETE request for activity that doesn't exist
        Assert: Response contains error detail message
        """
        # Arrange
        email = sample_email
        nonexistent_activity = "Nonexistent Activity"
        
        # Act
        response = client.delete(f"/activities/{nonexistent_activity}/participants?email={email}")
        data = response.json()
        
        # Assert
        assert response.status_code == 404
        assert "detail" in data

    def test_remove_nonexistent_participant_returns_404(self, client, reset_activities, sample_activity_name):
        """
        Test that removing nonexistent participant returns 404.
        
        Arrange: Prepare email that is not signed up for the activity
        Act: Make DELETE request to remove participant that doesn't exist
        Assert: Response status is 404
        """
        # Arrange
        email = "nonexistent@mergington.edu"
        activity_name = sample_activity_name
        
        # Act
        response = client.delete(f"/activities/{activity_name}/participants?email={email}")
        
        # Assert
        assert response.status_code == 404

    def test_remove_nonexistent_participant_returns_error_detail(self, client, reset_activities, sample_activity_name):
        """
        Test that removing nonexistent participant returns error detail.
        
        Arrange: Prepare email that is not signed up for the activity
        Act: Make DELETE request to remove participant that doesn't exist
        Assert: Response contains error detail message
        """
        # Arrange
        email = "nonexistent@mergington.edu"
        activity_name = sample_activity_name
        
        # Act
        response = client.delete(f"/activities/{activity_name}/participants?email={email}")
        data = response.json()
        
        # Assert
        assert response.status_code == 404
        assert "detail" in data

    def test_remove_does_not_affect_other_participants(self, client, reset_activities, sample_activity_name):
        """
        Test that removing one participant doesn't affect others.
        
        Arrange: Sign up multiple participants
        Act: Remove one participant
        Assert: Other participants remain in the activity
        """
        # Arrange
        email_to_remove = "participant1@mergington.edu"
        email_to_keep = "participant2@mergington.edu"
        activity_name = sample_activity_name
        
        client.post(f"/activities/{activity_name}/signup?email={email_to_remove}")
        client.post(f"/activities/{activity_name}/signup?email={email_to_keep}")
        
        # Act
        response = client.delete(f"/activities/{activity_name}/participants?email={email_to_remove}")
        activities_response = client.get("/activities").json()
        
        # Assert
        assert response.status_code == 200
        assert email_to_remove not in activities_response[activity_name]["participants"]
        assert email_to_keep in activities_response[activity_name]["participants"]
