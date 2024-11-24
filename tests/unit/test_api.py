from unittest.mock import patch


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json == {"status": "healthy"}


def test_import_csv_post_request(client):
    data = {"target": "http://example.com/data.csv"}
    with patch("app.stream_csv.delay") as mock_task:
        mock_task.return_value.id = "12345"
        response = client.post("/import", json=data)
        assert response.status_code == 200
        assert "task-id" in response.json
        assert response.json["task-id"] == "12345"
        mock_task.assert_called_once_with(data["target"], batch_size=100)


def test_import_csv_get_request(client):
    response = client.get("/import")
    assert response.status_code == 200
    assert "Please use a POST request" in response.json["message"]


def test_import_status(client):
    job_id = "test-job-id"
    with patch("app.AsyncResult") as mock_result:
        mock_result.return_value.state = "PROGRESS"
        mock_result.return_value.info = {"processed": 50}
        response = client.get(f"/status/{job_id}")
        assert response.status_code == 200
        assert response.json["processed"] == 50


def test_abort_import(client):
    job_id = "test-job-id"
    with patch("app.celery_app.control.revoke") as mock_revoke:
        response = client.get(f"/abort/{job_id}")
        assert response.status_code == 200
        mock_revoke.assert_called_once_with(job_id, terminate=True)
