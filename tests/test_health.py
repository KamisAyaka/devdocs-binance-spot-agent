from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_check_returns_success_response() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "message": "Service is healthy.",
        "data": {
            "status": "ok",
            "service": "devdocs-binance-spot-agent",
        },
    }
