from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_metrics():
    r = client.get("/metrics")
    assert r.status_code == 200
    assert "requests_total" in r.json()


def test_status_echo_ok():
    r = client.get("/status?code=200")
    assert r.status_code == 200


def test_status_echo_500():
    r = client.get("/status?code=500")
    assert r.status_code == 500


def test_mock_payment_success():
    r = client.post(
        "/mock/payment",
        headers={"X-Scenario": "success"},
        json={"transactionId": "TXN1", "amount": 10, "currency": "USD"},
    )
    assert r.status_code == 200


def test_mock_payment_declined():
    r = client.post("/mock/payment", headers={"X-Scenario": "declined"}, json={})
    assert r.status_code == 402


def test_auth_missing():
    r = client.get("/auth/mock")
    assert r.status_code == 401


def test_auth_valid():
    r = client.get("/auth/mock", headers={"Authorization": "Bearer test-token-12345"})
    assert r.status_code == 200


def test_failure_random():
    r = client.get("/failure/mock?code=503")
    assert r.status_code == 503


def test_config():
    r = client.get("/config")
    assert r.status_code == 200
    assert "rate_limits" in r.json()
