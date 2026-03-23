from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

from app.core.exceptions import AppException, register_exception_handlers
from app.core.middleware import register_middlewares
from app.main import app


client = TestClient(app)


def test_request_id_and_latency_headers_exist() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.headers.get("X-Request-ID")
    assert response.headers.get("X-Process-Time-MS")


def test_request_id_is_propagated_from_header() -> None:
    response = client.get("/health", headers={"X-Request-ID": "req-123"})

    assert response.status_code == 200
    assert response.headers["X-Request-ID"] == "req-123"


def test_app_exception_returns_standard_error_response() -> None:
    test_app = FastAPI()
    register_middlewares(test_app)
    register_exception_handlers(test_app)

    @test_app.get("/app-error")
    async def app_error() -> None:
        raise AppException(code="TOOL_TIMEOUT", message="Tool execution timed out.", status_code=504)

    local_client = TestClient(test_app, raise_server_exceptions=False)
    response = local_client.get("/app-error", headers={"X-Request-ID": "req-app"})

    assert response.status_code == 504
    assert response.json() == {
        "success": False,
        "error": {
            "code": "TOOL_TIMEOUT",
            "message": "Tool execution timed out.",
            "request_id": "req-app",
        },
    }


def test_http_exception_returns_standard_error_response() -> None:
    test_app = FastAPI()
    register_middlewares(test_app)
    register_exception_handlers(test_app)

    @test_app.get("/http-error")
    async def http_error() -> None:
        raise HTTPException(status_code=404, detail="Not found.")

    local_client = TestClient(test_app, raise_server_exceptions=False)
    response = local_client.get("/http-error", headers={"X-Request-ID": "req-http"})

    assert response.status_code == 404
    assert response.json() == {
        "success": False,
        "error": {
            "code": "HTTP_ERROR",
            "message": "Not found.",
            "request_id": "req-http",
        },
    }


def test_unhandled_exception_returns_standard_error_response() -> None:
    test_app = FastAPI()
    register_middlewares(test_app)
    register_exception_handlers(test_app)

    @test_app.get("/crash")
    async def crash() -> None:
        raise RuntimeError("unexpected")

    local_client = TestClient(test_app, raise_server_exceptions=False)
    response = local_client.get("/crash", headers={"X-Request-ID": "req-crash"})

    assert response.status_code == 500
    assert response.json() == {
        "success": False,
        "error": {
            "code": "INTERNAL_SERVER_ERROR",
            "message": "Unexpected server error.",
            "request_id": "req-crash",
        },
    }


def test_validation_exception_returns_standard_error_response() -> None:
    test_app = FastAPI()
    register_middlewares(test_app)
    register_exception_handlers(test_app)

    @test_app.get("/validation")
    async def validation(num: int) -> dict[str, int]:
        return {"num": num}

    local_client = TestClient(test_app, raise_server_exceptions=False)
    response = local_client.get("/validation?num=bad", headers={"X-Request-ID": "req-422"})

    assert response.status_code == 422
    assert response.json() == {
        "success": False,
        "error": {
            "code": "VALIDATION_ERROR",
            "message": "Request validation failed.",
            "request_id": "req-422",
        },
    }
