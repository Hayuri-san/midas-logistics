from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_list_warehouses_and_routes():
    warehouses = client.get("/api/warehouses")
    routes = client.get("/api/routes")

    assert warehouses.status_code == 200
    assert [warehouse["id"] for warehouse in warehouses.json()] == ["WH-A", "WH-B", "WH-C"]
    assert routes.status_code == 200
    assert len(routes.json()) == 3


def test_route_selection_adapts_to_blockage_and_clear():
    find_payload = {"origin": "WH-A", "destination": "WH-C"}
    assert client.post("/api/routes/find", json=find_payload).json()["id"] == "ROUTE-01"

    blocked = client.post(
        "/api/events",
        json={"event_type": "ROAD_BLOCKED", "source": "SimulationEngine", "payload": {"route_id": "ROUTE-01"}},
    )
    assert blocked.status_code == 200
    assert client.post("/api/routes/find", json=find_payload).json()["id"] == "ROUTE-02"

    cleared = client.post(
        "/api/events",
        json={"event_type": "ROAD_CLEARED", "source": "SimulationEngine", "payload": {"route_id": "ROUTE-01"}},
    )
    assert cleared.status_code == 200
    assert client.post("/api/routes/find", json=find_payload).json()["id"] == "ROUTE-01"


def test_truck_breakdown_changes_status():
    response = client.post(
        "/api/events",
        json={"event_type": "TRUCK_BREAKDOWN", "source": "SimulationEngine", "payload": {"truck_id": "TRUCK-02"}},
    )
    assert response.status_code == 200
    truck = next(truck for truck in client.get("/api/trucks").json() if truck["id"] == "TRUCK-02")
    assert truck["status"] == "unavailable"


def test_create_assignment_updates_related_records():
    response = client.post(
        "/api/assignments",
        json={"cargo_id": "CARGO-002", "truck_id": "TRUCK-02", "route_id": "ROUTE-01"},
    )
    assert response.status_code == 201
    assert response.json()["route_id"] == "ROUTE-01"
    cargo = next(cargo for cargo in client.get("/api/cargo").json() if cargo["id"] == "CARGO-002")
    assert cargo["status"] == "assigned"


def test_invalid_references_are_handled_safely():
    assignment = client.post(
        "/api/assignments",
        json={"cargo_id": "missing", "truck_id": "TRUCK-02"},
    )
    event = client.post(
        "/api/events",
        json={"event_type": "ROAD_BLOCKED", "source": "SimulationEngine", "payload": {"route_id": "missing"}},
    )
    route = client.post("/api/routes/find", json={"origin": "WH-B", "destination": "WH-C"})

    assert assignment.status_code == 404
    assert event.status_code == 404
    assert route.status_code == 404