"""
Pytest configuration and fixtures for FastAPI tests.

This module provides reusable fixtures for testing the FastAPI application,
including the test client and sample data fixtures.
"""

import sys
from copy import deepcopy
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app import app, activities


@pytest.fixture
def client():
    """Provide a TestClient instance for making requests to the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """
    Reset activities to initial state before each test to ensure test isolation.
    
    Yields the activities dictionary and restores it after the test.
    """
    # Store original activities (using deepcopy to preserve nested structure)
    original_activities = deepcopy(activities)
    
    yield activities
    
    # Restore to original state
    activities.clear()
    activities.update(deepcopy(original_activities))


@pytest.fixture
def sample_email():
    """Provide a sample email for testing."""
    return "test@mergington.edu"


@pytest.fixture
def sample_activity_name():
    """Provide a sample activity name for testing."""
    return "Chess Club"
