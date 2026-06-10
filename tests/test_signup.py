"""
Tests for the POST /activities/{activity_name}/signup endpoint.

Tests verify signup functionality including success cases and error handling
using the AAA (Arrange-Act-Assert) pattern.
"""

import pytest


class TestSignupForActivity:
    """Tests for signing up for an activity."""

    def test_signup_successful(self, client, reset_activities, sample_email, sample_activity_name):
        """
        Test successful signup for an activity.
        
        Arrange: Prepare email and activity name
        Act: Make POST request to signup
        Assert: Response status is 200 and success message is returned
        """
        # Arrange
        email = sample_email
        activity_name = sample_activity_name
        
        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        
        # Assert
        assert response.status_code == 200
        assert "message" in response.json()

    def test_signup_adds_participant_to_activity(self, client, reset_activities, sample_email, sample_activity_name):
        """
        Test that signup adds the participant to the activity's participants list.
        
        Arrange: Prepare email and activity name
        Act: Make POST request to signup
        Assert: Participant email is in activity's participants list
        """
        # Arrange
        email = sample_email
        activity_name = sample_activity_name
        
        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        activities_response = client.get("/activities").json()
        
        # Assert
        assert response.status_code == 200
        assert email in activities_response[activity_name]["participants"]

    def test_signup_returns_success_message(self, client, reset_activities, sample_email, sample_activity_name):
        """
        Test that signup returns appropriate success message.
        
        Arrange: Prepare email and activity name
        Act: Make POST request to signup
        Assert: Response contains email and activity name in message
        """
        # Arrange
        email = sample_email
        activity_name = sample_activity_name
        
        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        data = response.json()
        
        # Assert
        assert response.status_code == 200
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_signup_nonexistent_activity_returns_404(self, client, reset_activities, sample_email):
        """
        Test that signup for nonexistent activity returns 404.
        
        Arrange: Prepare email and nonexistent activity name
        Act: Make POST request to signup for activity that doesn't exist
        Assert: Response status is 404
        """
        # Arrange
        email = sample_email
        nonexistent_activity = "Nonexistent Activity"
        
        # Act
        response = client.post(f"/activities/{nonexistent_activity}/signup?email={email}")
        
        # Assert
        assert response.status_code == 404

    def test_signup_nonexistent_activity_returns_error_detail(self, client, reset_activities, sample_email):
        """
        Test that signup for nonexistent activity returns error detail.
        
        Arrange: Prepare email and nonexistent activity name
        Act: Make POST request to signup for activity that doesn't exist
        Assert: Response contains error detail message
        """
        # Arrange
        email = sample_email
        nonexistent_activity = "Nonexistent Activity"
        
        # Act
        response = client.post(f"/activities/{nonexistent_activity}/signup?email={email}")
        data = response.json()
        
        # Assert
        assert response.status_code == 404
        assert "detail" in data

    def test_signup_duplicate_returns_400(self, client, reset_activities, sample_email, sample_activity_name):
        """
        Test that duplicate signup returns 400 (Bad Request).
        
        Arrange: Prepare email and activity name, sign up once
        Act: Attempt to sign up the same email again
        Assert: Second signup returns 400
        """
        # Arrange
        email = sample_email
        activity_name = sample_activity_name
        # First signup
        client.post(f"/activities/{activity_name}/signup?email={email}")
        
        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        
        # Assert
        assert response.status_code == 400

    def test_signup_duplicate_returns_error_message(self, client, reset_activities, sample_email, sample_activity_name):
        """
        Test that duplicate signup returns appropriate error message.
        
        Arrange: Prepare email and activity name, sign up once
        Act: Attempt to sign up the same email again
        Assert: Response contains error detail about already registered
        """
        # Arrange
        email = sample_email
        activity_name = sample_activity_name
        # First signup
        client.post(f"/activities/{activity_name}/signup?email={email}")
        
        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        data = response.json()
        
        # Assert
        assert response.status_code == 400
        assert "detail" in data
        assert "already" in data["detail"].lower()

    def test_signup_multiple_different_participants(self, client, reset_activities, sample_activity_name):
        """
        Test that multiple different participants can signup for same activity.
        
        Arrange: Prepare multiple different emails
        Act: Sign up multiple participants for the same activity
        Assert: All participants are in the activity's participants list
        """
        # Arrange
        emails = ["participant1@mergington.edu", "participant2@mergington.edu", "participant3@mergington.edu"]
        activity_name = sample_activity_name
        
        # Act
        for email in emails:
            response = client.post(f"/activities/{activity_name}/signup?email={email}")
            assert response.status_code == 200
        
        activities_response = client.get("/activities").json()
        
        # Assert
        for email in emails:
            assert email in activities_response[activity_name]["participants"]
