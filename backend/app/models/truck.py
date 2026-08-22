from pydantic import BaseModel, Field

from app.models.enums import TruckStatus


class Truck(BaseModel):
    """A truck with capacity that MIDAS can match cargo against."""

    id: str = Field(..., examples=["TRUCK-01"])
    company: str = Field(..., examples=["Company A"])
    location: str = Field(..., description="Current location", examples=["Warehouse A"])
    destination: str = Field(..., examples=["Warehouse C"])
    capacity: int = Field(..., gt=0, description="Total capacity in boxes")
    available_capacity: int = Field(..., ge=0, description="Unused capacity in boxes")
    status: TruckStatus = TruckStatus.AVAILABLE
