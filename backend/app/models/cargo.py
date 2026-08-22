from pydantic import BaseModel, Field

from app.models.enums import CargoStatus


class Cargo(BaseModel):
    """A cargo request waiting to be matched with a truck."""

    id: str = Field(..., examples=["CARGO-001"])
    company: str = Field(..., examples=["Company B"])
    origin: str = Field(..., examples=["Warehouse B"])
    destination: str = Field(..., examples=["Warehouse C"])
    quantity: int = Field(..., gt=0, description="Quantity in boxes")
    status: CargoStatus = CargoStatus.PENDING
