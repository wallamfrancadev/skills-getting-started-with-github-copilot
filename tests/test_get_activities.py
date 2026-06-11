"""
Tests for the GET /activities endpoint.

Tests verify that the endpoint returns all activities with the correct structure
and data using the AAA (Arrange-Act-Assert) pattern.
"""

import pytest


class TestGetActivities:
    """Tests for retrieving all activities."""

    def test_get_all_activities_returns_success(self, client, reset_activities):
        """
        Test that GET /activities returns a 200 status code.
        
        Arrange: Setup is handled by fixtures
        Act: Make GET request to /activities
        Assert: Response status is 200
        """
        # Arrange
        # Fixtures provide the test client
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200

    def test_get_all_activities_returns_dict(self, client, reset_activities):
        """
        Test that GET /activities returns a dictionary.
        
        Arrange: Setup is handled by fixtures
        Act: Make GET request to /activities
        Assert: Response is a dictionary
        """
        # Arrange
        # Fixtures provide the test client
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        assert isinstance(data, dict)

    def test_get_all_activities_contains_expected_activities(self, client, reset_activities):
        """
        Test that GET /activities contains all expected activity names.
        
        Arrange: Setup is handled by fixtures
        Act: Make GET request to /activities
        Assert: Response contains expected activity names
        """
        # Arrange
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Soccer Team",
            "Swimming Club",
            "Basketball Practice",
            "Art Studio",
            "Drama Club",
            "Photography Workshop",
            "Debate Team",
            "Math Club",
            "Science Olympiad"
        ]
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        assert all(activity in data for activity in expected_activities)

    def test_activity_has_required_fields(self, client, reset_activities):
        """
        Test that each activity has required fields.
        
        Arrange: Setup is handled by fixtures
        Act: Make GET request to /activities
        Assert: Each activity has description, schedule, max_participants, participants
        """
        # Arrange
        required_fields = ["description", "schedule", "max_participants", "participants"]
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        for activity_name, activity_data in data.items():
            assert all(field in activity_data for field in required_fields)

    def test_activity_participants_is_list(self, client, reset_activities):
        """
        Test that each activity's participants field is a list.
        
        Arrange: Setup is handled by fixtures
        Act: Make GET request to /activities
        Assert: Participants field is a list for all activities
        """
        # Arrange
        # Fixtures provide the test client
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        for activity_name, activity_data in data.items():
            assert isinstance(activity_data["participants"], list)

    def test_activity_max_participants_is_integer(self, client, reset_activities):
        """
        Test that each activity's max_participants is an integer.
        
        Arrange: Setup is handled by fixtures
        Act: Make GET request to /activities
        Assert: max_participants is an integer for all activities
        """
        # Arrange
        # Fixtures provide the test client
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        for activity_name, activity_data in data.items():
            assert isinstance(activity_data["max_participants"], int)
