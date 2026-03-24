"""Week 1 minimal demo script."""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app


def main() -> None:
    client = TestClient(app)

    print("=== Week 1 Demo ===")

    health = client.get("/health", headers={"X-Request-ID": "demo-health"})
    print("[/health] status:", health.status_code)
    print("[/health] x-request-id:", health.headers.get("X-Request-ID"))
    print("[/health] body:", health.json())

    config = client.get("/config", headers={"X-Request-ID": "demo-config"})
    print("[/config] status:", config.status_code)
    print("[/config] x-request-id:", config.headers.get("X-Request-ID"))
    print("[/config] body keys:", sorted(config.json().keys()))
    print("[/config] data keys:", sorted(config.json()["data"].keys()))

    print("=== Demo Completed ===")


if __name__ == "__main__":
    main()
