"""Tests for the Flask frontend/API (target.py coverage is measured separately)."""

import pytest

from app import app, parse_arg


@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()


def test_index_lists_all_16_functions(client):
    html = client.get("/").get_data(as_text=True)
    assert html.count('class="card"') == 16


def test_health_returns_sha(client):
    data = client.get("/health").get_json()
    assert data["status"] == "ok"
    assert "sha" in data


def test_run_success(client):
    data = client.post("/api/run/is_adult", json={"args": ["18"]}).get_json()
    assert data == {"ok": True, "result": "True", "type": "bool"}


def test_run_error_is_shown(client):
    data = client.post("/api/run/divide", json={"args": ["1", "0"]}).get_json()
    assert data["ok"] is False
    assert data["error"] == "ZeroDivisionError"


def test_run_empty_set(client):
    data = client.post("/api/run/common_items", json={"args": ["{1}", "{2}"]}).get_json()
    assert data["result"] == "set()"


def test_run_unknown_function(client):
    assert client.post("/api/run/nope", json={"args": []}).status_code == 404


@pytest.mark.parametrize(
    "raw, expected",
    [("18", 18), ("2.5", 2.5), ("None", None), ("[1, 2]", [1, 2]), ("hello", "hello"), ("", "")],
)
def test_parse_arg(raw, expected):
    assert parse_arg(raw) == expected
