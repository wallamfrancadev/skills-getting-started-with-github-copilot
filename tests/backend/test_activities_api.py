"""Backend tests for FastAPI activity endpoints."""

def test_get_activities_returns_activity_map(client):
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]
    assert isinstance(data["Chess Club"]["participants"], list)


def test_root_redirects_to_static_index(client):
    response = client.get("/", allow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"
