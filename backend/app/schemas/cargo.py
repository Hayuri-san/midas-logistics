from pydantic import BaseModel, Field


class CargoCreate(BaseModel):
    """Request body for POST /api/cargo.

    id and status are server-assigned, so they are deliberately excluded here.
    """

    company: str = Field(..., examples=["Company C"])
    origin: str = Field(..., examples=["Warehouse A"])
    destination: str = Field(..., examples=["Warehouse D"])
    quantity: int = Field(..., gt=0, examples=[25])
