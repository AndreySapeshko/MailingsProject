import pytest
from django.urls import reverse
from django.db import connection
from unittest.mock import patch


@pytest.mark.django_db
def test_health_live(client):
    resp = client.get("/health/live/")
    assert resp.status_code == 200
    assert resp.json() == {"status": "live"}


@pytest.mark.django_db
def test_health_ready_all_ok(client, mocker):
    # DB
    mocker.patch.object(connection, "cursor", return_value=True)

    # Redis
    mocker.patch("redis.Redis.ping", return_value=True)

    # Celery
    mocker.patch("celery_app.celery.app.control.ping", return_value=[{"ok": "pong"}])

    resp = client.get("/health/ready/")

    assert resp.status_code == 200
    assert resp.json()["status"] == "ready"
    assert resp.json()["checks"] == {
        "database": True,
        "redis": True,
        "celery": True,
    }


@pytest.mark.django_db
def test_health_ready_degraded(client, mocker):
    # Падающие зависимости
    mocker.patch.object(connection, "cursor", side_effect=Exception())
    mocker.patch("redis.Redis.ping", side_effect=Exception())
    mocker.patch("celery_app.celery.app.control.ping", side_effect=Exception())

    resp = client.get("/health/ready/")

    assert resp.status_code == 503
    assert resp.json()["status"] == "degraded"
    assert resp.json()["checks"] == {
        "database": False,
        "redis": False,
        "celery": False,
    }
