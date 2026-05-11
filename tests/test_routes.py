from unittest.mock import MagicMock


def test_missing_required_field_returns_400(client):
    r = client.get("/weatherstation/updateweatherstation.php?ID=ST1")
    assert r.status_code == 400
    assert "dateutc" in r.get_json()["error"].lower()


def test_forwards_wu_response_status_and_body(client, mocker):
    mock_get = mocker.patch("app.routes.requests.get")
    mock_get.return_value = MagicMock(
        status_code=418,
        content=b"teapot",
        headers={"Content-Type": "application/x-teapot"},
    )
    r = client.get("/weatherstation/updateweatherstation.php?ID=S&dateutc=now")
    assert r.status_code == 418
    assert r.data == b"teapot"
    assert r.content_type.startswith("application/x-teapot")


def test_forward_failure_returns_502(client, mocker):
    mock_get = mocker.patch("app.routes.requests.get")
    mock_get.side_effect = OSError("network down")

    r = client.get("/weatherstation/updateweatherstation.php?ID=S&dateutc=now")

    assert r.status_code == 502
    assert "error" in r.get_json()


def test_station_row_persisted_after_success(client, app, mocker):
    mock_get = mocker.patch("app.routes.requests.get")
    mock_get.return_value = MagicMock(
        status_code=200,
        content=b"ok",
        headers={"Content-Type": "text/plain"},
    )

    client.get(
        "/weatherstation/updateweatherstation.php"
        "?ID=MINE&dateutc=2020-06-01%2010:00:00&tempf=55&humidity=60"
    )

    with app.app_context():
        from sqlalchemy import select

        from app.models import VevorWeatherData
        from app import db

        rows = db.session.scalars(select(VevorWeatherData)).all()
        assert len(rows) == 1
        assert rows[0].station_id == "MINE"
        assert rows[0].temperature_f == 55.0
        assert rows[0].humidity == 60
