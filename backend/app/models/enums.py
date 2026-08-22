from enum import Enum


class TruckStatus(str, Enum):
    AVAILABLE = "available"
    IN_TRANSIT = "in_transit"
    UNAVAILABLE = "unavailable"


class CargoStatus(str, Enum):
    PENDING = "pending"
    ASSIGNED = "assigned"
    DELIVERED = "delivered"


class AssignmentStatus(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
