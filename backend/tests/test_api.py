from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_list_trucks():
    response = client.get("/api/trucks")
    assert response.status_code == 200
    trucks = response.json()
    assert len(trucks) >= 1
    assert trucks[0]["id"] == "TRUCK-01"


def test_list_cargo():
    response = client.get("/api/cargo")
    assert response.status_code == 200
    cargo = response.json()
    assert len(cargo) >= 1
    assert cargo[0]["id"] == "CARGO-001"


def test_list_assignments():
    response = client.get("/api/assignments")
    assert response.status_code == 200
    assignments = response.json()
    assert len(assignments) >= 1
    assert assignments[0]["truck_id"] == "TRUCK-01"


def test_create_cargo():
    payload = {
        "company": "Company D",
        "origin": "Warehouse A",
        "destination": "Warehouse B",
        "quantity": 15,
    }
    response = client.post("/api/cargo", json=payload)
    assert response.status_code == 201
    created = response.json()
    assert created["company"] == "Company D"
    assert created["status"] == "pending"
    assert created["id"].startswith("CARGO-")

    # confirm it shows up in the list afterwards
    list_response = client.get("/api/cargo")
    ids = [c["id"] for c in list_response.json()]
    assert created["id"] in ids


def test_create_cargo_rejects_invalid_quantity():
    payload = {
        "company": "Company D",
        "origin": "Warehouse A",
        "destination": "Warehouse B",
        "quantity": 0,
    }
    response = client.post("/api/cargo", json=payload)
    assert response.status_code == 422
