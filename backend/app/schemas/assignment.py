from pydantic import BaseModel, Field


class AssignmentCreate(BaseModel):
    cargo_id: str = Field(..., examples=["CARGO-002"])
    truck_id: str = Field(..., examples=["TRUCK-02"])
    route_id: str | None = Field(default=None, examples=["ROUTE-01"])