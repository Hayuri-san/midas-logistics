"""In-memory shared state for the MIDAS MVP.

This is intentionally NOT a database. It's a single process-wide store that
the API layer reads from and writes to. Every team member's component
(matching, simulation, WebSocket broadcasts, etc.) is expected to go through
this module rather than holding its own copy of the data, so there is one
source of truth while the backend runs.

Not thread-safe / not multi-worker safe. Fine for a hackathon demo running
`uvicorn` with a single worker; would need a real store before that changes.
"""

import uuid

from app.models import (
    Assignment,
    AssignmentStatus,
    Cargo,
    CargoStatus,
    Route,
    RouteStatus,
    Truck,
    TruckStatus,
    Warehouse,
)


class AppState:
    def __init__(self) -> None:
        self.trucks: dict[str, Truck] = {}
        self.cargo: dict[str, Cargo] = {}
        self.assignments: dict[str, Assignment] = {}
        self.warehouses: dict[str, Warehouse] = {}
        self.routes: dict[str, Route] = {}
        self._seed()

    def _seed(self) -> None:
        for warehouse in [
            Warehouse(id="WH-A", name="Warehouse A"),
            Warehouse(id="WH-B", name="Warehouse B"),
            Warehouse(id="WH-C", name="Warehouse C"),
        ]:
            self.warehouses[warehouse.id] = warehouse

        for route in [
            Route(id="ROUTE-01", origin="WH-A", destination="WH-C", road_type="highway", traffic="low", condition="good", distance=120),
            Route(id="ROUTE-02", origin="WH-A", destination="WH-C", road_type="local", traffic="medium", condition="good", distance=110),
            Route(id="ROUTE-03", origin="WH-A", destination="WH-C", road_type="local", traffic="low", condition="bad", distance=100),
        ]:
            self.routes[route.id] = route

        seed_trucks = [
            Truck(
                id="TRUCK-01",
                company="Company A",
                location="Warehouse A",
                destination="Warehouse C",
                capacity=100,
                available_capacity=40,
                status=TruckStatus.IN_TRANSIT,
            ),
            Truck(
                id="TRUCK-02",
                company="Company A",
                location="Warehouse B",
                destination="Warehouse D",
                capacity=80,
                available_capacity=60,
                status=TruckStatus.AVAILABLE,
            ),
            Truck(
                id="TRUCK-03",
                company="Company B",
                location="Warehouse C",
                destination="Warehouse A",
                capacity=120,
                available_capacity=120,
                status=TruckStatus.AVAILABLE,
            ),
        ]
        for truck in seed_trucks:
            self.trucks[truck.id] = truck

        seed_cargo = [
            Cargo(
                id="CARGO-001",
                company="Company B",
                origin="Warehouse B",
                destination="Warehouse C",
                quantity=40,
                status=CargoStatus.ASSIGNED,
            ),
            Cargo(
                id="CARGO-002",
                company="Company C",
                origin="Warehouse A",
                destination="Warehouse D",
                quantity=25,
                status=CargoStatus.PENDING,
            ),
        ]
        for cargo in seed_cargo:
            self.cargo[cargo.id] = cargo

        seed_assignments = [
            Assignment(
                id="ASSIGN-001",
                cargo_id="CARGO-001",
                truck_id="TRUCK-01",
                status=AssignmentStatus.ACTIVE,
            ),
        ]
        for assignment in seed_assignments:
            self.assignments[assignment.id] = assignment

    def list_trucks(self) -> list[Truck]:
        return list(self.trucks.values())

    def list_cargo(self) -> list[Cargo]:
        return list(self.cargo.values())

    def list_assignments(self) -> list[Assignment]:
        return list(self.assignments.values())

    def list_warehouses(self) -> list[Warehouse]:
        return list(self.warehouses.values())

    def list_routes(self) -> list[Route]:
        return list(self.routes.values())

    def add_cargo(self, company: str, origin: str, destination: str, quantity: int) -> Cargo:
        cargo_id = f"CARGO-{uuid.uuid4().hex[:6].upper()}"
        cargo = Cargo(
            id=cargo_id,
            company=company,
            origin=origin,
            destination=destination,
            quantity=quantity,
            status=CargoStatus.PENDING,
        )
        self.cargo[cargo.id] = cargo
        return cargo

    def add_assignment(self, cargo_id: str, truck_id: str, route_id: str | None) -> Assignment:
        assignment = Assignment(
            id=f"ASSIGN-{uuid.uuid4().hex[:6].upper()}",
            cargo_id=cargo_id,
            truck_id=truck_id,
            route_id=route_id,
            status=AssignmentStatus.ACTIVE,
        )
        self.assignments[assignment.id] = assignment
        self.cargo[cargo_id].status = CargoStatus.ASSIGNED
        self.trucks[truck_id].status = TruckStatus.IN_TRANSIT
        return assignment

    def set_route_status(self, route_id: str, route_status: RouteStatus) -> Route:
        route = self.routes[route_id]
        route.status = route_status
        return route

    def break_truck(self, truck_id: str) -> Truck:
        truck = self.trucks[truck_id]
        truck.status = TruckStatus.UNAVAILABLE
        return truck


# Single process-wide instance. Import this, don't instantiate AppState directly.
state = AppState()
