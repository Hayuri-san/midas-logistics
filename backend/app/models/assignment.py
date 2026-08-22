from pydantic import BaseModel, Field
from typing import Optional

from app.models.enums import AssignmentStatus


class Assignment(BaseModel):
    """A link between a Cargo request and the Truck carrying it."""

    id: str = Field(..., examples=["ASSIGN-001"])
    cargo_id: str = Field(..., examples=["CARGO-001"])
    truck_id: str = Field(..., examples=["TRUCK-01"])
    route_id: Optional[str] = Field(default=None, examples=["ROUTE-01"])
    status: AssignmentStatus = AssignmentStatus.ACTIVE
