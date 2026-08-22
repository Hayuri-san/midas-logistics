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

from app.models import Assignment, AssignmentStatus, Cargo, CargoStatus, Truck, TruckStatus


class AppState:
    def __init__(self) -> None:
        self.trucks: dict[str, Truck] = {}
        self.cargo: dict[str, Cargo] = {}
        self.assignments: dict[str, Assignment] = {}
        self._seed()

    def _seed(self) -> None:
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


# Single process-wide instance. Import this, don't instantiate AppState directly.
state = AppState()
